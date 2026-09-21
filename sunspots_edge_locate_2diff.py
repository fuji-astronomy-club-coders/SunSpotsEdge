from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

# 設定

# TIFF画像が入っているフォルダ
folder = r"C:\Users\sakil\Downloads\2025-08-30-0437_9-CapObj - コピー\2025-08-30-0437_9-CapObj - コピー"

select = 2 #1=横バージョン　2=縦バージョン

if select ==1:
    # 調べる列(縦方向)の範囲 ここは黒点ごとに変えてください
    row_start = 580
    row_end = 592
    row = (row_start + row_end) // 2

    # 調べる行(横方向)の範囲
    col_start = 691
    col_end = 715
    col = (col_start + col_end) // 2


    # =========================
    # TIFF画像を処理
    # =========================

    for filename in sorted(os.listdir(folder)):

        if filename.lower().endswith((".tif", ".tiff")):

            # 画像を読み込む
            path = os.path.join(folder, filename)
            img = Image.open(path)

            # NumPy配列に変換
            data = np.array(img)

            # 行rowの列col_start～col_endを取得

            selected = data[row, col_start:col_end + 1].astype(int)

            print (selected)


            # 左→右に微分

            derivative = np.diff(selected)

            print(derivative)

            morederivative = np.diff(derivative)

            print(morederivative)

            morederivative_1 = morederivative[:len(morederivative)//2+1]
            morederivative_2 = morederivative[len(morederivative)//2+1:]

            # 最小となる場所
            min_index_1 = np.argmin(morederivative_1)

            # 最小となる場所
            min_index_2 = np.argmin(morederivative_2)

            # 元画像上の列番号に戻す
            min_col_1 = col_start + min_index_1 + 1

            # 元画像上の列番号に戻す
            min_col_2 = col_start + min_index_2 + len(morederivative_1) + 1

            # 最大微分値
            min_value_1 = morederivative_1[min_index_1]

            # 最大微分値
            min_value_2 = morederivative_2[min_index_2]

            print(
                f"{filename} : "
                f"最小二回微分_1 = {min_value_1}, "
                f"座標 = ({min_col_1}, {row})"
            )
            
            print(
                f"{filename} : "
                f"最小二回微分_2 = {min_value_2}, "
                f"座標 = ({min_col_2}, {row})"
            )
            

            # =========================
            # 元画像に最大点を表示
            # =========================

            plt.figure(figsize=(10, 8))

            plt.imshow(data, cmap="gray")

            # 最大点を赤い点で表示
            plt.scatter(
                min_col_1,
                row,
                color="red",
                s=50
            )

            plt.scatter(
                min_col_2,
                row,
                color="red",
                s=50
            )

            plt.title(filename)
            plt.xlabel("x (column)")
            plt.ylabel("y (row)")

            plt.show()

            plt.imshow(data, cmap="gray")

            # 選択した部分を赤線で描画
            plt.plot(
                range(col_start, col_end + 1),
                [row] * (col_end - col_start + 1),
                color="red",
                linewidth=2
            )

            plt.show()

else:
    # 調べる列(縦方向)の範囲 ここは黒点ごとに変えてください
    row_start = 459
    row_end = 478
    row = (row_start + row_end) // 2

    # 調べる行(横方向)の範囲
    col_start = 960
    col_end = 970
    col = (col_start + col_end) // 2


    # =========================
    # TIFF画像を処理
    # =========================

    for filename in sorted(os.listdir(folder)):

        if filename.lower().endswith((".tif", ".tiff")):

            # 画像を読み込む
            path = os.path.join(folder, filename)
            img = Image.open(path)

            # NumPy配列に変換
            data = np.array(img)

            # 行rowの列col_start～col_endを取得

            selected = data[row_start:row_end + 1,col].astype(int)

            print (selected)


            # 上→下に微分

            derivative = np.diff(selected)

            print(derivative)

            morederivative = np.diff(derivative)

            print(morederivative)

            morederivative_1 = morederivative[:len(morederivative)//2+1]
            morederivative_2 = morederivative[len(morederivative)//2+1:]

            # 最小となる場所
            min_index_1 = np.argmin(morederivative_1)

            # 最小となる場所
            min_index_2 = np.argmin(morederivative_2)

            # 元画像上の列番号に戻す
            min_row_1 = row_start + min_index_1

            # 元画像上の列番号に戻す
            min_row_2 = row_start + min_index_2 + len(morederivative_1)

            # 最大微分値
            min_value_1 = morederivative_1[min_index_1]

            # 最大微分値
            min_value_2 = morederivative_2[min_index_2]

            print(
                f"{filename} : "
                f"最小二回微分_1 = {min_value_1}, "
                f"座標 = ({col}, {min_row_1})"
            )
            
            print(
                f"{filename} : "
                f"最小二回微分_2 = {min_value_2}, "
                f"座標 = ({col},{min_row_2})"
            )

            # =========================
            # 元画像に最大点を表示
            # =========================

            plt.figure(figsize=(10, 8))

            plt.imshow(data, cmap="gray")

            # 最大点を赤い点で表示
            plt.scatter(
                col,
                min_row_1+1,
                color="red",
                s=50
            )

            plt.scatter(
                col,
                min_row_2+1,
                color="red",
                s=50
            )

            plt.title(filename)
            plt.xlabel("x (column)")
            plt.ylabel("y (row)")

            plt.show()

            plt.imshow(data, cmap="gray")

            # 選択した部分を赤線で描画
            plt.plot(
                [col] * (row_end - row_start + 1),
                range(row_start, row_end + 1),
                color="red",
                linewidth=2
            )

            plt.show()