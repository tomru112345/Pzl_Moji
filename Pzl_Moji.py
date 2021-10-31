import tkinter
import random

index = 0
timer = 0
score = 0
hisc = 1000
difficulty = 0
tsugi = 0

# カーソルの位置
cursor_x = 0
cursor_y = 0

# マスの数
cell_x = 8
cell_y = 10

# マスの長さ
cell_len = 72

# フレームの長さ
flame_len = 24


# マウスの座標初期化
mouse_x = 0
mouse_y = 0

# キャンバスの大きさ
cvs_width = 912
cvs_height = 768

# マウスがクリックしたかどうか
mouse_c = False


def mouse_move(e):
    """マウスの座標取得"""
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y


def mouse_press(e):
    """マウスのクリック取得"""
    global mouse_c
    mouse_c = True


def mouse_release(e):
    """マウスのリリース取得"""
    global mouse_c
    mouse_c = False


neko = []
check = []
for i in range(10):
    neko.append([0, 0, 0, 0, 0, 0, 0, 0])
    check.append([0, 0, 0, 0, 0, 0, 0, 0])


def draw_block():
    cvs.delete("DROW")
    for y in range(cell_y):
        for x in range(cell_x):
            if neko[y][x] > 0:
                cvs.create_text(x * cell_len + int(flame_len + cell_len / 2),
                                y * cell_len + int(flame_len + cell_len / 2),
                                text=Word_Kanji[neko[y][x]],
                                anchor="center",
                                font=("HG丸ｺﾞｼｯｸM-PRO", 24),
                                tag="DROW"
                                )


def check_block():
    for y in range(cell_y):
        for x in range(cell_x):
            check[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(cell_x):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7

    for y in range(cell_y):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7

    for y in range(1, 9):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    neko[y-1][x-1] = 7
                    neko[y][x] = 7
                    neko[y+1][x+1] = 7
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    neko[y+1][x-1] = 7
                    neko[y][x] = 7
                    neko[y-1][x+1] = 7


def sweep_block():
    num = 0
    for y in range(cell_y):
        for x in range(cell_x):
            if neko[y][x] == 7:
                neko[y][x] = 0
                num = num + 1
    return num


def drop_block():
    """ブロックを落とせるかどうか"""
    flg = False
    for y in range(cell_y - 2, -1, -1):
        for x in range(cell_x):
            if (neko[y][x] != 0 and neko[y+1][x] == 0):
                neko[y+1][x] = neko[y][x]
                neko[y][x] = 0
                flg = True
    return flg


def over_block():
    for x in range(cell_x):
        if neko[0][x] > 0:
            return True
    return False


def set_block():
    for x in range(cell_x):
        neko[0][x] = random.randint(0, difficulty)


def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Meiryo UI", siz, "bold")
    cvs.create_text(x + 2, y + 2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)


def game_main():
    global index, timer, score, hisc, difficulty, tsugi
    global cursor_x, cursor_y, mouse_c
    if index == 0:  # タイトルロゴ
        draw_txt("もじもじくん", 312, 240, 100, "violet", "TITLE")
        cvs.create_rectangle(168, 384, 456, 456,
                             fill="skyblue", width=0, tag="TITLE")
        draw_txt("Easy", 312, 420, 40, "white", "TITLE")
        cvs.create_rectangle(168, 528, 456, 600,
                             fill="lightgreen", width=0, tag="TITLE")
        draw_txt("Normal", 312, 564, 40, "white", "TITLE")
        cvs.create_rectangle(168, 672, 456, 744,
                             fill="orange", width=0, tag="TITLE")
        draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        index = 1
        mouse_c = False
    elif index == 1:  # タイトル画面 スタート待ち
        difficulty = 0
        if mouse_c:
            if 168 < mouse_x and mouse_x < 456 and 384 < mouse_y and mouse_y < 456:
                difficulty = 4
            if 168 < mouse_x and mouse_x < 456 and 528 < mouse_y and mouse_y < 600:
                difficulty = 5
            if 168 < mouse_x and mouse_x < 456 and 672 < mouse_y and mouse_y < 744:
                difficulty = 6
        if difficulty > 0:
            for y in range(cell_y):
                for x in range(cell_x):
                    neko[y][x] = 0
            mouse_c = False
            score = 0
            tsugi = 0
            cursor_x = 0
            cursor_y = 0
            set_block()
            draw_block()
            cvs.delete("TITLE")
            index = 2
    elif index == 2:  # 落下
        if not drop_block():
            index = 3
        draw_block()
    elif index == 3:  # 揃ったか
        check_block()
        draw_block()
        index = 4
    elif index == 4:  # 揃ったネコがあれば消す
        sc = sweep_block()
        score = score + sc*difficulty*2
        if score > hisc:
            hisc = score
        if sc > 0:
            index = 2
        else:
            if not over_block():
                tsugi = random.randint(1, difficulty)
                index = 5
            else:
                index = 6
                timer = 0
        draw_block()
    elif index == 5:  # マウス入力を待つ
        if (flame_len <= mouse_x
            and mouse_x < flame_len + cell_len * cell_x
            and flame_len <= mouse_y
                and mouse_y < flame_len + cell_len * cell_y):
            cursor_x = int((mouse_x - flame_len) / cell_len)
            cursor_y = int((mouse_y - flame_len) / cell_len)
            if mouse_c:
                mouse_c = False
                # set_block()
                neko[cursor_y][cursor_x] = tsugi
                tsugi = 0
                index = 2
        cvs.delete("CURSOR")
        cvs.create_rectangle(cursor_x * cell_len + int(flame_len + cell_len / 2) - (cell_len / 2),
                             cursor_y * cell_len +
                             int(flame_len + cell_len / 2) - (cell_len / 2),
                             cursor_x * cell_len +
                             int(flame_len + cell_len / 2) + (cell_len / 2),
                             cursor_y * cell_len +
                             int(flame_len + cell_len / 2) + (cell_len / 2),
                             outline="#FF0000", width=3, tag="CURSOR")
        draw_block()
    elif index == 6:  # ゲームオーバー
        timer = timer + 1
        if timer == 1:
            draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 50:
            cvs.delete("OVER")
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE "+str(score), 160, 60, 32, "blue", "INFO")
    draw_txt("HISC "+str(hisc), 450, 60, 32, "yellow", "INFO")
    if tsugi > 0:
        cvs.create_text(752, 128,
                        text=Word_Kanji[tsugi],
                        anchor="center",
                        font=("HG丸ｺﾞｼｯｸM-PRO", 24),
                        tag="INFO"
                        )
    root.after(100, game_main)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("落ち物パズル : もじもじくん")
    root.resizable(False, False)  # ウィンドウサイズ変更できない
    root.bind("<Motion>", mouse_move)  # マウスが動いた時に実行
    root.bind("<ButtonPress>", mouse_press)  # マウスクリックを指定
    root.bind("<ButtonRelease>", mouse_release)  # マウスリリースを指定
    cvs = tkinter.Canvas(root, width=cvs_width, height=cvs_height)
    cvs.pack()

    # フィールド作成
    flame_color = "#808080"
    cvs.create_line(flame_len / 2, 0, flame_len / 2,
                    cvs_height, width=24, fill=flame_color)
    cvs.create_line(0, flame_len / 2, (flame_len + cell_len * cell_x + flame_len / 2),
                    flame_len / 2, width=24, fill=flame_color)
    cvs.create_line((flame_len + cell_len * cell_x + flame_len / 2), 0,
                    (flame_len + cell_len * cell_x + flame_len / 2), cvs_height, width=24, fill=flame_color)
    cvs.create_line(0, (cvs_height - flame_len / 2), (flame_len + cell_len * cell_x + flame_len / 2),
                    (cvs_height - flame_len / 2), width=24, fill=flame_color)

    for y in range(cell_y):
        for x in range(cell_x):
            if ((x + y) % 2 == 0):
                cell_color = "#C0C0C0"
            else:
                cell_color = "#FFFFFF"
            cvs.create_rectangle(flame_len + x * cell_len,
                                 flame_len + y * cell_len,
                                 flame_len + (x + 1) * cell_len,
                                 flame_len + (y + 1) * cell_len,
                                 fill=cell_color, outline=flame_color)

    Word_Kanji = [
        None,
        "木",
        "口",
        "八",
        "十",
        "一",
        "水",
        "卍"
    ]

    game_main()
    root.mainloop()
