import os
import numpy as np
from PIL import Image
from matplotlib import cm
from matplotlib.colors import Normalize

COLORMAP_NAME = 'jet'       # カラーマップ名
NORM_MODE = 'percentile'      # 正規化方式: 'percentile' | 'minmax' | 'fixed'
P_LOW, P_HIGH = 2, 98         # percentile使用時の下限・上限 (%)
RAW_MIN, RAW_MAX = 0, 4095    # 'fixed' 使用時のレンジ

# カラーマップを一度だけ取得
cmap = cm.get_cmap(COLORMAP_NAME)

# ハイパーデータ読み込み関数
def hyprawread(name, hor, ver, SpectDim):
    with open(name, 'rb') as f:
        img = np.fromfile(f, np.uint16, -1)
    img = np.reshape(img, (ver, SpectDim, hor))
    img = np.transpose(img, (0, 2, 1))
    return img

for i in range(400, 1000, 100):
    # 画像として保存したい波長
    wave = i # ★

    # 処理するフォルダのパスを指定
    input_directory = '../data/20250905_dataCollection/HSC_data/HSC_data_400nm_1000nm'
    output_directory = '../data/20250905_dataCollection/HSC_data/processed_images_colors' + str(wave)+ 'nm/'


    # ディレクトリが存在しない場合は作成
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # SIS-Iの場合のパラメータ
    width=1200
    height=1024
    SpectDim = 125

    # 指定波長に対応するバンドインデックス
    band_tmp = int((wave - 380) / 5)

    # フォルダ内のすべてのファイルを処理
    for filename in os.listdir(input_directory):
        if filename.endswith('.nh8'):
            input_filepath = os.path.join(input_directory, filename)
            
            img=hyprawread (input_filepath,width,height,SpectDim)
            
            # #グレースケールの場合はこちら##################################
            # # 指定波長の画像を抽出
            # img_wave = ((img[:, :, band_tmp]) / 4095) * 255
            # img_test = Image.fromarray(np.uint8(img_wave))

            # # 保存するファイル名を設定
            # save_filename = filename.split('_')[0] + '_' + filename.split('_')[1] + '.png'
            # save_filepath = os.path.join(output_directory, save_filename)
            
            # # 画像を保存
            # img_test.save(save_filepath)
            ###############################################################

            # カラースケールの場合はこちら###################################
            band = img[:, :, band_tmp].astype(np.float32)

            # 正規化 (例: パーセンタイル)
            vmin = np.percentile(band, P_LOW)
            vmax = np.percentile(band, P_HIGH)
            norm = Normalize(vmin=vmin, vmax=vmax, clip=True)
            band_norm = norm(band)

            # カラーマップ適用
            rgba = cmap(band_norm)              # (H, W, 4) RGBA
            rgb = (rgba[..., :3] * 255).astype(np.uint8)  # RGBに変換
            img_color = Image.fromarray(rgb, mode='RGB')

            # 保存するファイル名を設定
            save_filename = filename.split('_')[0] + '_' + filename.split('_')[1] + '.png'
            save_filepath = os.path.join(output_directory, save_filename)
            
            # 画像を保存
            img_color.save(save_filepath)
            ###############################################################

