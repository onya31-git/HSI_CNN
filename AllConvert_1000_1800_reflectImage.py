import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ハイパーデータ読み込み関数
def hyprawread(name, hor, ver, SpectDim):
    with open(name, 'rb') as f:
        img = np.fromfile(f, np.uint16, -1)
    img = np.reshape(img, (ver, SpectDim, hor))
    img = np.transpose(img, (0, 2, 1))
    return img

# 画像として保存したい波長
wave = 1700 # ★

# 処理するフォルダのパスを指定
input_directory = 'C:/Users/Atsuya_Watanabe/research/2408PeachDetect/20240724AKATSUKI/HyperspectoralCameraData/20240725(1000~1800)/'
output_directory = 'C:/Users/Atsuya_Watanabe/research/2408PeachDetect/20240724AKATSUKI/HyperspectoralCameraData/processed_images_reflection' + str(wave)+ 'nm/'

# ディレクトリが存在しない場合は作成
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# SIS-Iの場合のパラメータ
hor = 400
ver = 320
SpectDim = 81

# 指定波長に対応するバンドインデックス
band_tmp = int((wave - 900) / 10)

# 白板のデータを読み込み
white_reference_filepath = 'C:/Users/Atsuya_Watanabe/2408PeachDetect/20240724AKATSUKI/HyperspectoralCameraData/20240725(1000~1800)/white_SpectImg(80f,4.5ms).nir'  # 白板データのパスを指定
white_reference = hyprawread(white_reference_filepath, hor, ver, SpectDim)

# フォルダ内のすべてのファイルを処理
for filename in os.listdir(input_directory):
    if filename.endswith('.nir'):
        input_filepath = os.path.join(input_directory, filename)
        
        # 画像データを読み込み
        img = hyprawread(input_filepath, hor, ver, SpectDim)
        
        # 指定波長の画像を抽出
        img_wave = img[:, :, band_tmp]
        white_wave = white_reference[:, :, band_tmp]
        
        # 反射率の計算
        reflectance = img_wave / white_wave
        reflectance = np.clip(reflectance, 0, 1)  # 値を0から1の範囲に制限
        
        # カラースケールに変換
        colormap = cm.get_cmap('jet')  # 'jet'カラーマップを使用
        reflectance_color = colormap(reflectance)[:, :, :3]  # RGB値を抽出
        
        # 8ビットに変換
        reflectance_color = (reflectance_color * 255).astype(np.uint8)
        
        # カラースケール画像をPILイメージに変換
        reflectance_image = Image.fromarray(reflectance_color)
        
        # 保存するファイル名を設定
        save_filename = 'hsc_image_' + str(wave) + 'nm_' + os.path.splitext(filename)[0] + '.png'
        save_filepath = os.path.join(output_directory, save_filename)
        
        # 画像を保存
        reflectance_image.save(save_filepath)
