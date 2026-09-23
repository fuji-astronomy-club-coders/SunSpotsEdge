from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os


def BoundingBoxStat(
	filename: str, row_start: int, row_end: int, col_start: int, col_end: int, derivatives_times: int
) -> tuple[float,float,float,float,float]:

	"""
	Args:
		filename (str): フォルダの中に入っているTIFF画像のファイル名
		row_start (int):   矩形領域の左端のx座標
		row_end (int):     矩形領域の右端のx座標
		col_start (int):   矩形領域の上端のy座標
		col_end (int):     矩形領域の下端のy座標
		derivatives_times(int): 何回微分するのか (1回 or 2回)
	Return:
		row_result_start (float): 求めた外接矩形の左端のx座標
		col_result_start (float): 求めた外接矩形の上端のy座標
		w_result (float): 求めた外接矩形の横の長さ
		h_result (float): 求めた外接矩形の縦の長さ
		area: 外接矩形の面積
	Raise:
		ValueError: 画像がTIFFファイルではないとき
	"""
	
	if filename.lower().endswith((".tif", ".tiff")):

		# 画像を読み込む
		path = os.path.join(folder, filename)
		img = Image.open(path)

		# NumPy配列に変換
		data = np.array(img)

		# 矩形領域の真ん中の列と行を取りだす
		row = (row_start + row_end) // 2
		col = (col_start + col_end) // 2
		row_selected = data[col, row_start:row_end + 1].astype(int)
		col_selected = data[col_start:col_end + 1, row].astype(int)

		# 微分から座標検出までべっこに関数を設けた
		row_result_start, row_result_end = Differentiation(row_selected,row_start,derivatives_times)
		col_result_start, col_result_end = Differentiation(col_selected,col_start,derivatives_times)

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

		#描画
		bbox_stat = (row_result_start, row_result_end, col_result_start, col_result_end)
		DrawResult(data, row, col, bbox_stat)

		return row_result_start, col_result_start, w_result, h_result, area

	# 画像がTIFFじゃなかった場合の例外処理
	else:
		raise ValueError(
            f"無効な画像フォーマットです。TIFFファイルを指定してください。現在の入力: {filename}"
        )



# 微分から座標検出までやってくれる関数。BoundingBoxStatから呼ばれます
def Differentiation(selected: np.ndarray, start: int, derivatives_times: int) -> tuple[float,float]:

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
	data: np.ndarray, row: int, col: int, bbox_stat: tuple[float,float,float,float]
	) -> None:

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
	plt.scatter(
		row,
		col_result_start,
		color="red",
		s=50
	)

	plt.scatter(
		row,
		col_result_end,
		color="red",
		s=50
	)

	plt.scatter(
		row_result_start,
		col,
		color="red",
		s=50
	)

	plt.scatter(
		row_result_end,
		col,
		color="red",
		s=50
	)

	plt.title(filename)
	plt.xlabel("x (column)")
	plt.ylabel("y (row)")

	plt.show()


# ここは人によって変える
folder = r"C:\Users\seigo\Downloads\2025-08-30-0437_9-CapObj - コピー"

# 試しに呼んでみる
for filename in sorted(os.listdir(folder)):
	x,y,w,h,area = BoundingBoxStat(filename,955,975,460,480,2)






