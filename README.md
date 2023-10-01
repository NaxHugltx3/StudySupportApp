# Features
Benesseで行われた個人開発ハッカソンの作品です。
ポケモンSleepにインスパイアされ、その勉強版をイメージして作りました。

このPythonスクリプトは、OpenCVを使用してWebカメラでの顔認識を行います。
リアルタイムで顔と目を検出し、Webカメラとのインタラクションに基づいてスコアを提供します。
勉強中に寝てしまうと霊夢がアラームを鳴らしながら注意をしてくれます。

# Requirement

このスクリプトを実行するには、以下のライブラリが必要です：

- OpenCV (`cv2`)
- tkinter (`tk`)
- Pillow (`PIL`)
- simpleaudio (`simpleaudio`)
- numpy (`numpy`)

# Installation
これらのライブラリは、以下のようにpipを使用してインストールできます：

```bash
pip install opencv-python-headless
pip install pillow
pip install simpleaudio
pip install numpy

このリポジトリをクローンします：
git clone https://github.com/yourusername/your-repo.git
cd your-repo

プロジェクトディレクトリに必要な画像ファイルとXMLファイルがあることを確認してください：
alarm_sound.wav：アラーム用の音声ファイル
facial_recognition_webcam.py：メインのPythonスクリプト
haarcascade_eye.xml：目の検出に使用するXMLファイル
haarcascade_frontalface_default.xml：顔の検出に使用するXMLファイル
raige_reimu.png：アラーム用の画像ファイル
standard_reimu.png：標準表示用の画像ファイル

# Usage
Pythonでスクリプトを実行します：
bash
Copy code
python facial_recognition_webcam.py
スクリプトはWebカメラの映像を表示するウィンドウを開きます。
スクリプトはリアルタイムで顔と目を検出します。
Webカメラとのインタラクションに基づいて、ユーザーのスコアを計算します（例：まばたきの回数など）。
"一時中断"（Pause）ボタンをクリックすることで、スクリプトを一時停止できます。
一定の期間目が検出されない場合、アラームウィンドウが表示されることがあります。
スコアはキャンバスに表示されます。

# Note

このスクリプトは顔と目の検出にOpenCVを使用しています。
プロジェクトディレクトリに必要な画像ファイルとXMLファイルがあることを確認してください。
スクリプト内のtimeoutやfinish_timeなどのパラメータを必要に応じて調整できます。
スクリプトは一定期間目が検出されない場合、アラーム音を再生するように設定されています。
ユーザースコアはWebカメラとのインタラクションに基づいて更新されます。
