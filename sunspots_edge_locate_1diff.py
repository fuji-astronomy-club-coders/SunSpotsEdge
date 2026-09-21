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

            # 最大となる場所
            max_index = np.argmax(derivative)

            # 元画像上の列番号に戻す
            max_col = col_start + max_index + 0.5

            # 最大微分値
            max_value = derivative[max_index]

            # 最小となる場所
            min_index = np.argmin(derivative)
            
            # 元画像上の列番号に戻す
            min_col = col_start + min_index + 0.5
            
            # 最小微分値
            min_value = derivative[min_index]

            # 結果を表示

            print(
                f"{filename} : "
                f"最大微分 = {max_value}, "
                f"座標 = ({max_col}, {row})"
            )

            print(
                f"{filename} : "
                f"最小微分 = {min_value}, "
                f"座標 = ({min_col}, {row})"
            )

            # =========================
            # 元画像に最大点を表示
            # =========================

            plt.figure(figsize=(10, 8))

            plt.imshow(data, cmap="gray")

            # 最大点を赤い点で表示
            plt.scatter(
                max_col,
                row,
                color="red",
                s=50
                )

            plt.scatter(
                min_col,
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
        row_start = 458
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
    
                # 列colの列row_start～row_endを取得
    
                selected = data[row_start:row_end + 1,col].astype(int)
    
                print (selected)
    
    
                # 上→下に微分
    
                derivative = np.diff(selected)
    
                print(derivative)
    
                # 最大となる場所
                max_index = np.argmax(derivative)
    
                # 元画像上の行番号に戻す
                max_row = row_start + max_index + 0.5
    
                # 最大微分値
                max_value = derivative[max_index]
    
                # 最小となる場所
                min_index = np.argmin(derivative)
                
                # 元画像上の列番号に戻す
                min_row = row_start + min_index + 0.5
                
                # 最小微分値
                min_value = derivative[min_index]
    
                # 結果を表示
    
                print(
                    f"{filename} : "
                    f"最大微分 = {max_value}, "
                    f"座標 = ({col}, {max_row })"
                )
    
                print(
                    f"{filename} : "
                    f"最小微分 = {min_value}, "
                    f"座標 = ({col}, {min_row })"
                )
    
                # =========================
                # 元画像に最大点を表示
                # =========================
    
                plt.figure(figsize=(10, 8))
    
                plt.imshow(data, cmap="gray")
    
                # 最大点を赤い点で表示
                plt.scatter(
                    col,
                    max_row,
                    color="red",
                    s=50
                )
    
                plt.scatter(
                    col,
                    min_row,
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