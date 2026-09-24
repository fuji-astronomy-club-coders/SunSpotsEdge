"""画像上のおおよその黒点位置から、微分によって厳密な黒点位置を決定し、バウンドする"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def BoundingBoxStat(
    filename: str | Path,
    row_start: int,
    row_end: int,
    col_start: int,
    col_end: int,
    derivatives_times: int,
) -> tuple[float, float, float, float, float]:
    """TIFF画像内の指定矩形領域に対して微分を行い、外接矩形の座標と面積を計算・描画します。

    Parameters
    ----------
    filename : str | Path
        フォルダの中に入っているTIFF画像のファイル名またはパス。
    row_start : int
        矩形領域の左端のx座標。
    row_end : int
        矩形領域の右端のx座標。
    col_start : int
        矩形領域の上端のy座標。
    col_end : int
        矩形領域の下端のy座標。
    derivatives_times : int
        微分を行う回数（1回または2回）。

    Returns
    -------
    tuple[float, float, float, float, float]
        以下の値を含むタプル:
        - row_result_start (float): 求めた外接矩形の左端のx座標。
        - col_result_start (float): 求めた外接矩形の上端のy座標。
        - w_result (float): 求めた外接矩形の横の長さ。
        - h_result (float): 求めた外接矩形の縦の長さ。
        - area (float): 外接矩形の面積。

    Raises
    ------
    ValueError
        指定されたファイルがTIFF形式（.tif または .tiff）でない場合。
    """
    if str(filename).lower().endswith((".tif", ".tiff")):
        # 画像を読み込む
        path = Path(folder) / filename
        img = Image.open(path)

        # NumPy配列に変換
        data = np.array(img)

        # 矩形領域の真ん中の列と行を取りだす
        row = (row_start + row_end) // 2
        col = (col_start + col_end) // 2
        row_selected = data[col, row_start : row_end + 1].astype(int)
        col_selected = data[col_start : col_end + 1, row].astype(int)

        # 微分から座標検出までべっこに関数を設けた
        row_result_start, row_result_end = Differentiation(
            row_selected, row_start, derivatives_times
        )
        col_result_start, col_result_end = Differentiation(
            col_selected, col_start, derivatives_times
        )

        w_result = row_result_end - row_result_start
        h_result = col_result_end - col_result_start
        area = w_result * h_result

        print(
            f"{filename} : "
            f"x = {row_result_start}  "
            f"y = {col_result_start}  "
            f"w = {w_result}  "
            f"h = {h_result}  "
            f"area = {area}"
        )

        # 描画
        bbox_stat = (row_result_start, row_result_end, col_result_start, col_result_end)
        DrawResult(data, row, col, bbox_stat)

        return row_result_start, col_result_start, w_result, h_result, area

    # 画像がTIFFじゃなかった場合の例外処理
    else:
        raise ValueError(
            f"無効な画像フォーマットです。TIFFファイルを指定してください。現在の入力: {filename}"
        )


def Differentiation(
    selected: np.ndarray, start: int, derivatives_times: int
) -> tuple[float, float]:
    """選択された1次元配列に対して1階または2階微分を行い、極値に対応する座標を特定します。

    Parameters
    ----------
    selected : np.ndarray
        抽出された1次元データ配列。
    start : int
        元画像上での開始座標オフセット。
    derivatives_times : int
        微分を行う回数（1または2）。

    Returns
    -------
    tuple[float, float]
        検出された開始座標および終了座標のタプル (min_coordinate, max_coordinate)。
    """
    if derivatives_times == 1:
        # 左→右に1回微分
        derivative = np.diff(selected)

        # 最小となる場所
        min_index = np.argmin(derivative)

        # 元画像上の座標に戻す。差分を1回とっているため+0.5するのが妥当
        min_coordinate = start + min_index + 0.5

        # 最大となる場所
        max_index = np.argmax(derivative)

        # 元画像上の座標に戻す。差分を1回とっているため+0.5するのが妥当
        max_coordinate = start + max_index + 0.5

        return float(min_coordinate), float(max_coordinate)

    else:
        # 左→右に2回微分
        derivative = np.diff(np.diff(selected))

        # 最大となる場所。
        max_index = np.argmax(derivative)

        # 最大を起点に左右（縦方向なら上下）の最小をとる
        derivative_left = derivative[:max_index]
        derivative_right = derivative[max_index:]

        # 左で最小となる場所
        min_index_left = np.argmin(derivative_left)

        # 右で最小となる場所
        min_index_right = np.argmin(derivative_right)

        # 元画像上の列番号に戻す。差分を2回とっているため+1するのが妥当
        min_coordinate_left = start + min_index_left + 1

        # 元画像上の列番号に戻す。差分を2回とっているため+1するのが妥当
        min_coordinate_right = start + min_index_right + max_index + 1

        return float(min_coordinate_left), float(min_coordinate_right)


def DrawResult(
    data: np.ndarray, row: int, col: int, bbox_stat: tuple[float, float, float, float]
) -> None:
    """検出された端点座標を画像上にプロットして表示します。

    Parameters
    ----------
    data : np.ndarray
        表示対象の画像データ（2次元配列）。
    row : int
        中心のx座標（列番号）。
    col : int
        中心のy座標（行番号）。
    bbox_stat : tuple[float, float, float, float]
        検出された境界座標 (row_result_start, row_result_end, col_result_start, col_result_end)。
    """
    row_result_start, row_result_end, col_result_start, col_result_end = bbox_stat

    print(
        f"左の座標 = ({row_result_start}, {col})  "
        f"右の座標 = ({row_result_end}, {col})  "
        f"上の座標 = ({row}, {col_result_start})  "
        f"下の座標 = ({row}, {col_result_end})  "
    )

    plt.figure(figsize=(10, 8))

    plt.imshow(data, cmap="gray")

    # 赤い点で表示
    plt.scatter(row, col_result_start, color="red", s=50)

    plt.scatter(row, col_result_end, color="red", s=50)

    plt.scatter(row_result_start, col, color="red", s=50)

    plt.scatter(row_result_end, col, color="red", s=50)

    plt.title(str(filename))
    plt.xlabel("x (column)")
    plt.ylabel("y (row)")

    plt.show()


# ここは人によって変える
folder = r"C:\Users\seigo\Downloads\2025-08-30-0437_9-CapObj - コピー"
folder = Path(folder)
# 試しに呼んでみる
for filename in sorted(folder.iterdir()):
    x, y, w, h, area = BoundingBoxStat(filename, 955, 975, 460, 480, 2)
