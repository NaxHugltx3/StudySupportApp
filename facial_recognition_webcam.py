import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import simpleaudio as sa
import numpy as np

global current_score
current_score = 0

global timeout_counter
timeout_counter = 0

global finish_time
finish_time = 1000 #何秒間タイムバーを動かすか

global timeout
timeout = 5000  # 5秒のタイムアウト

global face_count
face_count = 0

global pause_flag
pause_flag = False

global sleep_counter
sleep_counter = 0

# 先頭の部分で変数を宣言しておく
global alarm_window
alarm_window = None

global plus_score
plus_score = 0

def move_slider():
    current_value = slider.get()
    if current_value < finish_time:
        new_value = current_value + 1
        slider.set(new_value)
        root.after(1000, move_slider)  #1秒ごとにタイムスライダーを更新

def pause_button_press():
    
    # 確認ウィンドウの作成
    global confirmation_window
    confirmation_window = tk.Toplevel(root)
    confirmation_window.title("confirmation window")
    
    # 注意ラベル
    face_count_label = tk.Label(confirmation_window, text="休憩しますか？", font=("Helvetica", 16))
    face_count_label.pack()
    
    # 一時中断ボタンの作成
    pause_button = tk.Button(confirmation_window, command =rest_button_press ,text="中断する")
    pause_button.pack()
    
    # メインウィンドウより少し小さくする
    confirmation_window_width = WINDOW_WIDTH - 550
    confirmation_window_height = WINDOW_HEIGHT - 740

    # ウィンドウを画面の中央に配置
    confirmation_x_position = (screen_width - confirmation_window_width) // 2
    confirmation_y_position = (screen_height - confirmation_window_height) // 2
    confirmation_window.geometry(f"{confirmation_window_width}x{confirmation_window_height}+{confirmation_x_position}+{confirmation_y_position}")

def rest_button_press():
    
    if confirmation_window:
        confirmation_window.destroy()
    
    global pause_flag
    pause_flag = True
    
    # 確認ウィンドウの作成
    global rest_window
    rest_window = tk.Toplevel(root)
    rest_window.title("rest window")
    
    # 注意ラベル
    face_count_label = tk.Label(rest_window, text="休憩中…", font=("Helvetica", 20))
    face_count_label.pack()
    
    # 一時中断ボタンの作成
    pause_button = tk.Button(rest_window, command =return_button_press ,text="勉強に戻る")
    pause_button.pack()
    
    # メインウィンドウより少し小さくする
    rest_window_width = WINDOW_WIDTH - 550
    rest_window_height = WINDOW_HEIGHT - 740

    # ウィンドウを画面の中央に配置
    confirmation_x_position = (screen_width - rest_window_width) // 2
    confirmation_y_position = (screen_height - rest_window_height) // 2
    rest_window.geometry(f"{rest_window_width}x{rest_window_height}+{confirmation_x_position}+{confirmation_y_position}")

def return_button_press():
    
    global pause_flag
    pause_flag = False
    
    if rest_window:
        rest_window.destroy()

def update_score():
    
    global current_score,plus_score, timeout_counter
    
    if face_count > 0 and not pause_flag:
        timeout_counter = 0
        plus_score += 1
    else:
        timeout_counter += 1000
    
    if(timeout_counter >= timeout and not pause_flag):
        current_score -= 5
        if(current_score < 0):
            current_score = 0
        timeout_counter = 0
        print("decrease_score")
    
    if(plus_score >= 10):
        current_score += plus_score
        plus_score = 0
    
    score_label.config(text="Score: " + str(current_score))
    
    root.after(1000, update_score)  # 1秒ごとにスコアを更新

def show_alarm_window():
    
    global alarm_window
    global image_window

    if image_window:
        # image_windowが存在していれば非表示にする
        image_window.withdraw()
    
    # 既にalarm_windowが表示されている場合は何もしない
    if alarm_window and alarm_window.winfo_exists():
        return
    
    # 確認ウィンドウの作成
    alarm_window = tk.Toplevel(root)
    alarm_window.title("alarm window")
    
    # 注意ラベル
    face_count_label = tk.Label(alarm_window, text="何寝とんねん！！", font=("Helvetica", 25))
    face_count_label.pack(pady=10)
    
    global image_pil
    image_pil = Image.open(counvert_image_path)  # 画像をPIL Imageとして読み込み

    # 画像をリサイズ
    image_pil = image_pil.resize((200, 200), Image.LANCZOS)

    # PIL ImageオブジェクトをTkinter PhotoImageオブジェクトに変換
    image_tk = ImageTk.PhotoImage(image=image_pil)

    # 画像を表示するためのラベルを作成
    image_label = tk.Label(alarm_window, image=image_tk)
    image_label.image = image_tk  # ラベルにImageTkオブジェクトを保持させるために参照を保持
    image_label.pack()
    
    # メインウィンドウより少し小さくする
    alarm_window_width = WINDOW_WIDTH - 250
    alarm_window_height = WINDOW_HEIGHT - 550

    # ウィンドウを画面の中央に配置
    confirmation_x_position = (screen_width - alarm_window_width) // 2
    confirmation_y_position = (screen_height - alarm_window_height) // 2
    alarm_window.geometry(f"{alarm_window_width}x{alarm_window_height}+{confirmation_x_position}+{confirmation_y_position}")

    wave_obj.play()  # 音声再生
    
    # 5秒後にウィンドウを破棄
    alarm_window.after(5000, lambda: close_alarm_window())

def close_alarm_window():
    global alarm_window
    global image_window

    # alarm_windowが存在していれば破棄する
    if alarm_window:
        alarm_window.destroy()

    # image_windowが存在していれば再表示する
    if image_window:
        image_window.deiconify()

def show_image_window():
    
    # 新しいウィンドウを作成
    global image_window
    image_window = tk.Toplevel(root)
    image_window.title("")

    # 画像ファイルの読み込み
    image_pil = Image.open(original_image_path)
    image_pil = image_pil.resize((100, 100), Image.LANCZOS)

    # 画像を左右反転
    image_pil = image_pil.transpose(Image.FLIP_LEFT_RIGHT)

    # PIL ImageオブジェクトをTkinter PhotoImageオブジェクトに変換
    image_tk = ImageTk.PhotoImage(image=image_pil)

    # 画像を表示するためのラベルを作成
    image_label = tk.Label(image_window, image=image_tk)
    image_label.image = image_tk  # ラベルにImageTkオブジェクトを保持させるために参照を保持
    image_label.pack(side=tk.LEFT, padx=10, pady=10)  # 左寄せでパディングを追加
    
    # テキストラベルを作成
    text_label = tk.Label(image_window, text="勉強がんばろう", font=("Helvetica", 14))
    text_label.pack(side=tk.LEFT, padx=10, pady=10)  # 左寄せでパディングを追加
    
    # ウィンドウの位置とサイズを指定（左上に配置）
    image_window_x = x_position - 25
    image_window_y = y_position + 75
    image_window.geometry(f"260x110+{image_window_x}+{image_window_y}") #  # 幅400、高さ400、位置(x=0, y=0)
    
    # ウィンドウを常にrootウィンドウの上に表示
    image_window.attributes("-topmost", True)

# モザイク処理を適用する関数
def apply_mosaic_to_image(image, block_size=1):
    
    img_pil = Image.fromarray(image)
    w, h = img_pil.size
    img_mosaic = img_pil.resize((w // block_size, h // block_size), resample=Image.NEAREST)
    img_result = img_mosaic.resize((w, h), resample=Image.LANCZOS)
    return np.array(img_result)

def update_frame():
    
    ret, frame = cap.read()
    
    # 読み込みが成功した場合
    if ret:
        
        frame = cv.resize(frame, (800, 600))
        
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        face = cascade.detectMultiScale(gray_frame)
        
        faces_with_sizes = []  # (x, y, w, h, size) のリストを作成
        for (x, y, w, h) in face:
            faces_with_sizes.append((x, y, w, h, w * h))
        
        # サイズの大きい順にソート
        faces_with_sizes.sort(key=lambda item: item[4], reverse=True)
        
        global face_count
        face_count = 0  # 検出された顔の数をカウント
        for x, y, w, h in face:
            if face_count < 1 and not pause_flag:  # 1つまでの顔を囲む
                
                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)  # 顔の周りに矩形を描画
                
                # 顔領域内で目を検出
                face_roi = gray_frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(face_roi)
                
                eyes_with_sizes = []  # (ex, ey, ew, eh, size) のリストを作成
                for (ex, ey, ew, eh) in eyes:
                    eyes_with_sizes.append((ex, ey, ew, eh, ew * eh))
                
                # サイズの大きい順にソート
                eyes_with_sizes.sort(key=lambda item: item[4], reverse=True)
                
                eye_count = 0  # 検出された目の数をカウント
                
                global sleep_counter
                
                for (ex, ey, ew, eh) in eyes:
                    # 2つまでの目を囲む
                    # 顔の矩形の上半分にある矩形のみを目としてカウント
                    if eye_count < 2 and y + ey < y + h // 2:
                        cv.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)  # 目の周りに矩形を描画
                        eye_count += 1
                    
                    sleep_counter = 0
                
                if eye_count < 1:
                    sleep_counter += 1
                    if(sleep_counter >= 1):
                        show_alarm_window()
                        
            face_count += 1
        
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame_mosaic = apply_mosaic_to_image(frame_rgb)
    img = Image.fromarray(frame_mosaic)
    img_tk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
    canvas.img_tk = img_tk
    
    root.after(5, update_frame)  # 5ミリ秒ごとに更新

#顔認識の定義
HAAR_FILE = "haarcascade_frontalface_default.xml"
cascade = cv.CascadeClassifier(HAAR_FILE)

#目認識の定義
eye_cascade_path = './haarcascade_eye.xml'
eye_cascade = cv.CascadeClassifier(eye_cascade_path)

# 内蔵カメラの起動
cap = cv.VideoCapture(0)

# 画像ファイルの読み込み
original_image_path = "standard_reimu.png"
counvert_image_path = "raige_reimu.png"

# 再生する音声ファイルのパスを指定
alarm_sound_path = "alarm_sound.wav"
wave_obj = sa.WaveObject.from_wave_file(alarm_sound_path) # サウンドオブジェクトを作成

# ウィンドウサイズ関連の定数
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 800
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700

# Tkinter ウィンドウの作成
root = tk.Tk()
root.title("Camera Display")

# ウィンドウを画面の中央に配置
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - WINDOW_WIDTH) // 2
y_position = (screen_height - WINDOW_HEIGHT) // 2
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_position}+{y_position}")

# タイムスライダーの作成
slider = tk.Scale(root, from_=0, to=1000, length=500, orient="horizontal", showvalue=False)
slider.pack(pady=10)

# 一時中断ボタンの作成
pause_button = tk.Button(root, text="一時中断",command=pause_button_press)
pause_button.pack(pady=5)

# 動画キャンバスの作成
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

# スコアを表示するラベル
score_label = tk.Label(canvas, text="Score: "+str(current_score), font=("Helvetica", 22), bg="white")
score_label.place(x=CANVAS_WIDTH-110, y=20)  # キャンバスの右上に配置

# アプリケーションを実行
if __name__ == "__main__":
    
    update_score()
    show_image_window()
    
    root.after(1000, move_slider)
    root.after(5, update_frame)

    root.mainloop()
    cap.release() # アプリケーションが終了する際にカメラリソースを解放