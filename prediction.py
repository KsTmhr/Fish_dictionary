#coding utf-8
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

#分析を開始する関数
def fish_pre(x):
    np.set_printoptions(suppress=True)

    # モデルを読み込む
    model = tensorflow.keras.models.load_model('keras_model03.h5')

    # 適切な形状の配列を作成して、kerasモデルに入力します
    # 配列に入れることができる「長さ」または画像の数は
    # 形状タプルの最初の位置、この場合は1によって決定されます。
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # これを画像へのパスに置き換えます
    image = x

    # TM2と同じ方法で、画像のサイズを224x224に変更します。
    # 画像のサイズを少なくとも224x224に変更してから、中央からトリミングする
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # 画像をnumpy配列に変換します
    image_array = np.asarray(image)

    # 画像を正規化する
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # 画像を配列に読み込みます
    data[0] = normalized_image_array

    # 推論を実行する
    prediction = model.predict(data)

    # 結果を辞書に当てはめる
    results=prediction[0]
    fish=["ヤマトイワナ","スズキ","マアジ","サンマ","マイワシ","クロマグロ","バショウカジキ","オジサン","オオクチバス",
    "イシダイ","イシガキダイ","エビスダイ","エンゼルフィッシュ","アイゴ","アイナメ","ウツボ","ウマズラハギ","カンモンハタ",
    "カスミアジ","ギギ","ギンブナ","クダゴンべ","クロダイ","ケムシカジカ","ケツギョ","コイ","ゴンズイ","ブリ","カツオ"]
    dic = {key: val for key, val in zip(results, fish)}

    return(dic,sorted(dic,reverse=True))
