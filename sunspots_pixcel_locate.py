"""画像をカーソル位置によって座標を確認しながら表示するツール"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseEvent
from PIL import Image

# TIFF画像のパス
image_path = r"C:\Users\sakil\Downloads\2025-08-30-0437_9-CapObj - コピー\2025-08-30-0437_9-CapObj - コピー\img00001000.tiff"

# 画像を読み込む
img = Image.open(image_path)

# NumPy配列に変換
data = np.array(img)

fig, ax = plt.subplots()

# 画像を表示
ax.imshow(data, cmap="gray")

ax.set_title("マウスカーソルを画像に合わせてください")


def mouse_move(event: MouseEvent) -> None:
    """マウス移動イベントに応じて、現在のカーソル位置の座標とピクセル値をタイトルに表示します。

    Parameters
    ----------
    event : MouseEvent
        Matplotlibのマイベニューイベント情報。
    """
    if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
        x = int(event.xdata)
        y = int(event.ydata)

        # 画像の範囲内ならピクセル値を取得
        if 0 <= x < data.shape[1] and 0 <= y < data.shape[0]:
            value = data[y, x]

            ax.set_title(f"x={x}, y={y}, pixel value={value}")
            fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", mouse_move)

plt.show()
