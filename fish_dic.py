#coding utf-8
from PIL import Image,ImageTk,ImageOps
import tkinter as tk
import tkinter.filedialog as fd
import prediction as pre
import dictionary

# スクレイピング
# pip install google_images_download
# googleimagesdownload -k 検索したいワード

# 画面を作る
root=tk.Tk()
root.title(u"魚図鑑　ver 0.3")
root.geometry("900x600")

# 辞書を取得する
fish_dic=dictionary.get_dic()

# ボタンに設定する関数を作るクラス
class print_answer:
    def __init__(self,kind,result,bt):
        self.kind=kind
        self.result=result
        self.bt=bt

    def print_dic(self):
        global fish_dic
        global buttons

        # ボタンの背景色を変える
        for i in range(29):
            buttons[i].configure(bg="white")
        buttons[self.bt].configure(bg="#afeeee")

        # 結果を辞書で検索
        m=dictionary.main_dic(self.kind)
        img=Image.open(m[0])
        image=img.resize(size=(int(img.width/1.5),int(img.height/1.5)))
        img_data=ImageTk.PhotoImage(image)

        # データを代入
        disc=m[1]
        size=m[2]
        dist=m[3]
        hab=m[4]
        bait=m[5]
        if len(m)==7:
            alias=m[6]

        # 結果をラベルに代入
        fnt=("",17)
        btn2.configure(text="分析")
        kind_lbl.configure(font=("",30),text=self.kind)
        if "e"in str(self.result):
            seido.configure(font=fnt,text="精度：0.00%")
        else:
            seido.configure(font=fnt,text="精度："+str(self.result*100)[:4]+"%")
        setumei.configure(font=fnt,text=str(disc))
        taityo.configure(font=fnt,text="体長："+str(size))
        bunpu.configure(font=fnt,text="分布："+str(dist))
        seisoku.configure(font=fnt,text="生息域："+str(hab))
        esa.configure(font=fnt,text="主な食べ物："+str(bait))
        if len(m)==7:
            betumei.configure(font=fnt,text="別名："+str(alias))
        else:
            betumei.configure(font=fnt,text="")

        # ラベルを表示
        kind_lbl.place(x=250,y=10)
        seido.place(x=300,y=60)
        setumei.pack(pady=10,anchor=tk.W)
        taityo.pack(pady=10,anchor=tk.W)
        esa.pack(pady=10,anchor=tk.W)
        bunpu.pack(pady=10,anchor=tk.W)
        seisoku.pack(pady=10,anchor=tk.W)
        if len(m)==7:
            betumei.pack(pady=10,anchor=tk.W)
        fot.configure(image=img_data)
        fot.image=img_data

#===================================================関数=============================================================#

# 画像を表示する関数
def disp_photo(path):
    # 画像を読み込む
    new_image= Image.open(path)
    global image_log
    image_log=new_image
    size = (224, 224)
    new_image = ImageOps.fit(new_image, size, Image.ANTIALIAS).resize((300,300))
    # そのイメージをラベルに表示する
    image_data= ImageTk.PhotoImage(new_image)
    lbl2.configure(image=image_data)
    lbl2.image=image_data

# 画像を読み込む関数
def openfile():
    # これを画像へのパスに置き換えます
    fpath=fd.askopenfilename()
    if fpath:
        disp_photo(fpath)

# 分析結果を表示する関数
def analysis():

    global image_log
    global dic
    global buttons

    # 予測の実行
    n = pre.fish_pre(image_log)

    # 結果の代入
    dic = n[0]
    results =n[1]
    result=max(results)

    # 結果の表示
    main=print_answer(dic[result],result,0)
    main.print_dic()

    # その他の検索候補
    x=[]
    for i in range(29):
        m=dictionary.main_dic(dic[results[i]])
        img2=Image.open(m[0])
        image2=img2.resize(size=(int(img2.width/2.5),int(img2.height/2.5)))
        img_data2=ImageTk.PhotoImage(image2)
        images[i].configure(image=img_data2)
        images[i].image=img_data2
        images[i].place(x=0,y=i*75)

        y=print_answer(dic[results[i]],results[i],i)
        x.append(y)
        buttons[i].configure(command=y.print_dic)
        if results[i]>0.0001:
            buttons[i].configure(font=("",15),text=dic[results[i]]+"  "+str(results[i]*100)[:4]+"%",height=3)

        else:
            buttons[i].configure(font=("",15),text=dic[results[i]]+"          ",height=3)

#===================================================ラベルを作る======================================================#

# 題名
title_lbl=tk.Label(text="魚図鑑",font=("",35))
title_lbl.place(x=0,y=0)

# 検索欄
txtlbl=tk.Label(text="図鑑内を検索")
txtlbl.place(x=200,y=10)

# 画像選択欄
frame1 = tk.Frame(width =300,height=300,relief="groove",bd=3)
frame1.propagate(False)
frame1.place(x=0,y=125)


#==============================予測結果表示欄============================================
frame2 = tk.LabelFrame(text="予測結果",width =600,height=307,relief="groove",bd=3)
frame2.propagate(False)
frame2.place(x=300,y=118)

frame4=tk.Frame(frame2,width=600,height=100,relief="groove",bd=3)
frame2.propagate(False)
frame4.pack()

# 結果欄のキャンバス
canvas2 = tk.Canvas(frame2,width=595)

# 結果欄のバーフレーム
bar_frame2 = tk.Frame(canvas2)
canvas2.create_window((0,0), window=bar_frame2, anchor=tk.NW, width=canvas2.cget('width'))

# Scrollbar を生成して配置 frame2
bar2 = tk.Scrollbar(frame2, orient=tk.VERTICAL)
bar2.config(command=canvas2.yview)
bar2.pack(side=tk.RIGHT, fill=tk.Y)

# Canvas2の設定
canvas2.config(yscrollcommand=bar2.set)
canvas2.config(scrollregion=(0,0,0,400))# 横のスタート位置？、スタート位置、横の終了位置？、終了位置
canvas2.pack()


#=================================その他上位の検索候補欄====================================
frame3=tk.LabelFrame(text="その他の検索候補",width=600,height=175)
frame3.propagate(False)
frame3.place(x=300,y=425)

# スクロールバーのキャンバス
canvas = tk.Canvas(frame3,width=595)

# スクロールバーのフレーム
bar_frame = tk.Frame(canvas)
canvas.create_window((0,0), window=bar_frame, anchor=tk.NW, width=canvas.cget('width'))

# Scrollbar を生成して配置 frame3
bar = tk.Scrollbar(frame3, orient=tk.VERTICAL)
bar.config(command=canvas.yview)
bar.pack(side=tk.RIGHT, fill=tk.Y)

# Canvasの設定
canvas.config(yscrollcommand=bar.set)
canvas.config(scrollregion=(0,0,0,len(fish_dic)*75))# 横のスタート位置？、スタート位置、横の終了位置？、終了位置
canvas.pack()

# 複数の Buttonを生成し、Frame上に配置
buttons=[]
images=[]
for i in range(29):
    bt=tk.Button(bar_frame,height=3,font=("",15),text=" ")
    img=tk.Label(bar_frame)
    buttons.append(bt)
    images.append(img)
    bt.pack(fill=tk.X)

#=============================================ボタン・ラベル=========================================
# 画像参照ボタン
btn1=tk.Button(text="参照",command=openfile,width=41,height=2)
btn1.place(x=0,y=70)

# 分析スタートボタン
btn2=tk.Button(text="分析",command=analysis,width=41,height=2)
btn2.place(x=300,y=70)

# 説明
lbl1=tk.Label(text="分析する魚の画像を参照してください　分析ボタンを押すと分析が開始されます　分析には十秒ほどかかります")
lbl1.place(x=0,y=50)

# 画像表示欄
lbl2=tk.Label(frame1,text="画像を選ぶ\n(拡張子は.jpgか.jfifのみ)",width =300,height=300)
lbl2.pack()

# 魚の名前
kind_lbl=tk.Label(frame4)
# 精度
seido=tk.Label(frame4)
# 説明
setumei=tk.Label(bar_frame2)
# 体長
taityo=tk.Label(bar_frame2)
# 分布
bunpu=tk.Label(bar_frame2)
# 生息域
seisoku=tk.Label(bar_frame2)
# エサ
esa=tk.Label(bar_frame2)
# 別名
betumei=tk.Label(bar_frame2)
# 写真
fot=tk.Label(frame4)
fot.place(x=0,y=0)


root.mainloop()
