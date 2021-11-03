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

# カーソルの位置
px = 0
py = 0

# セレクト数
select = 0

# キーの設定
key = ""
kdown = False

# 設置するかどうか
cursor_c = False


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


def key_down(e):
    """キーが押されたとき"""
    global key, kdown
    key = e.keysym
    kdown = True


def key_up(e):
    """キーが押されてないとき"""
    global key, kdown
    key = ""
    kdown = False


cell = []
check = []

for i in range(10):
    cell.append([0, 0, 0, 0, 0, 0, 0, 0])
    check.append([0, 0, 0, 0, 0, 0, 0, 0])


def draw_block():
    cvs.delete("DROW")
    for y in range(cell_y):
        for x in range(cell_x):
            if (cell[y][x] > 0):
                cvs.create_text(x * cell_len + int(flame_len + cell_len / 2),
                                y * cell_len + int(flame_len + cell_len / 2),
                                text=Word_Kanji[cell[y][x]],
                                anchor="center",
                                font=("HG丸ｺﾞｼｯｸM-PRO", 48),
                                fill=Moji_Color[cell[y][x]],
                                tag="DROW"
                                )


def move_cursor():
    global px, py, cursor_c, index, difficulty, select

    if (index == 1):
        if ((key == "Return")):
            cursor_c = True
        if ((key == "Down")
            and (select >= 0)
                and (select < 3)):
            if (select != 3 - 1):
                select += 1
        if ((key == "Up")
            and (select >= 0)
                and (select < 3)):
            if (select != 0):
                select -= 1
        # 111
    if (index == 5):
        if ((key == "Left")
            and (px < cell_x)
                and (px >= 0)):
            if (px != 0):
                if (cell[py][px - 1] == 0):
                    px -= 1
        if ((key == "Right")
            and (px < cell_x)
                and (px >= 0)):
            if (px != cell_x - 1):
                if (cell[py][px + 1] == 0):
                    px += 1
        if ((key == "Down")
            and (py >= 0)
                and (py < cell_y)):
            if (py != cell_y - 1):
                if (cell[py + 1][px] == 0):
                    py += 1
        if (key == "Up"):
            cursor_c = True


def check_block():
    """消す判定"""
    """
    Word_Kanji = [
        None,
        "木",
        "口",
        "八",
        "十",
        "一",
        "水",
        "✕"
    ]
    """

    for y in range(cell_y):
        for x in range(cell_x):
            check[y][x] = cell[y][x]

    for y in range(1, 9):
        for x in range(cell_x):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    cell[y-1][x] = 7
                    cell[y][x] = 7
                    cell[y+1][x] = 7

    for y in range(cell_y):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    cell[y][x-1] = 7
                    cell[y][x] = 7
                    cell[y][x+1] = 7

    for y in range(1, 9):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    cell[y-1][x-1] = 7
                    cell[y][x] = 7
                    cell[y+1][x+1] = 7
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    cell[y+1][x-1] = 7
                    cell[y][x] = 7
                    cell[y-1][x+1] = 7


def sweep_block():
    num = 0
    for y in range(cell_y):
        for x in range(cell_x):
            if cell[y][x] == 7:
                cell[y][x] = 0
                num = num + 1
    return num


def drop_block():
    """ブロックを落とせるかどうか"""
    flg = False
    for y in range(cell_y - 2, -1, -1):
        for x in range(cell_x):
            if (cell[y][x] != 0 and cell[y+1][x] == 0):
                cell[y+1][x] = cell[y][x]
                cell[y][x] = 0
                flg = True
    return flg


def over_block():
    for x in range(cell_x):
        if cell[0][x] > 0:
            return True
    return False


def set_block():
    for x in range(cell_x):
        cell[0][x] = random.randint(0, difficulty)


def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("HG丸ｺﾞｼｯｸM-PRO", siz, "bold")
    cvs.create_text(x + 2, y + 2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)


def game_main():
    global index, timer, score, hisc, difficulty, tsugi
    global cursor_x, cursor_y, mouse_c, cursor_c, px, py
    if index == 0:  # タイトルロゴ
        # draw_txt("もじもじ", 312, 240, 100, "violet", "TITLE")
        cvs.create_rectangle(168, 384, 456, 456,
                             fill="black", width=0, tag="TITLE")
        draw_txt("Easy", 312, 420, 40, "white", "TITLE")
        cvs.create_rectangle(168, 528, 456, 600,
                             fill="black", width=0, tag="TITLE")
        draw_txt("Normal", 312, 564, 40, "white", "TITLE")
        cvs.create_rectangle(168, 672, 456, 744,
                             fill="black", width=0, tag="TITLE")
        draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        index = 1
        mouse_c = False
    elif index == 1:  # タイトル画面 スタート待ち
        difficulty = 0
        move_cursor()
        cvs.delete("TITLE")
        if (select == 0):
            cvs.create_rectangle(168, 384, 456, 456,
                                 fill="white", width=0, tag="TITLE")
            draw_txt("Easy", 312, 420, 40, "black", "TITLE")
            cvs.create_rectangle(168, 528, 456, 600,
                                 fill="black", width=0, tag="TITLE")
            draw_txt("Normal", 312, 564, 40, "white", "TITLE")
            cvs.create_rectangle(168, 672, 456, 744,
                                 fill="black", width=0, tag="TITLE")
            draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        if (select == 1):
            cvs.create_rectangle(168, 384, 456, 456,
                                 fill="black", width=0, tag="TITLE")
            draw_txt("Easy", 312, 420, 40, "white", "TITLE")
            cvs.create_rectangle(168, 528, 456, 600,
                                 fill="white", width=0, tag="TITLE")
            draw_txt("Normal", 312, 564, 40, "black", "TITLE")
            cvs.create_rectangle(168, 672, 456, 744,
                                 fill="black", width=0, tag="TITLE")
            draw_txt("Hard", 312, 708, 40, "white", "TITLE")
        if (select == 2):
            cvs.create_rectangle(168, 384, 456, 456,
                                 fill="black", width=0, tag="TITLE")
            draw_txt("Easy", 312, 420, 40, "white", "TITLE")
            cvs.create_rectangle(168, 528, 456, 600,
                                 fill="black", width=0, tag="TITLE")
            draw_txt("Normal", 312, 564, 40, "white", "TITLE")
            cvs.create_rectangle(168, 672, 456, 744,
                                 fill="white", width=0, tag="TITLE")
            draw_txt("Hard", 312, 708, 40, "black", "TITLE")

        if mouse_c:
            if 168 < mouse_x and mouse_x < 456 and 384 < mouse_y and mouse_y < 456:
                difficulty = 4
            if 168 < mouse_x and mouse_x < 456 and 528 < mouse_y and mouse_y < 600:
                difficulty = 5
            if 168 < mouse_x and mouse_x < 456 and 672 < mouse_y and mouse_y < 744:
                difficulty = 6
        if cursor_c:
            if (select == 0):
                difficulty = 4
            if (select == 1):
                difficulty = 5
            if (select == 2):
                difficulty = 6
        if difficulty > 0:
            for y in range(cell_y):
                for x in range(cell_x):
                    cell[y][x] = 0
            mouse_c = False
            cursor_c = False
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
    elif index == 4:  # 揃ったら消す
        sc = sweep_block()
        score = score + sc*difficulty*2
        if score > hisc:
            hisc = score
        if sc > 0:
            index = 2
        else:
            if not over_block():
                tsugi = random.randint(1, difficulty)
                px = 0
                py = 0
                index = 5
            else:
                index = 6
                timer = 0
        draw_block()
    elif index == 5:  # 入力を待つ
        move_cursor()
        if ((px >= 0 and px < cell_x) and (py >= 0 and py < cell_y)):
            cursor_x = px
            cursor_y = py
            if (cursor_c and (cell[cursor_y][cursor_x] == 0)):
                cursor_c = False
                set_block()
                cell[cursor_y][cursor_x] = tsugi
                tsugi = 0
                index = 2
        cvs.delete("CURSOR")
        if (cell[cursor_y][cursor_x] == 0):
            cvs.create_rectangle(cursor_x * cell_len + int(flame_len + cell_len / 2) - (cell_len / 2),
                                 cursor_y * cell_len +
                                 int(flame_len + cell_len / 2) -
                                 (cell_len / 2),
                                 cursor_x * cell_len +
                                 int(flame_len + cell_len / 2) +
                                 (cell_len / 2),
                                 cursor_y * cell_len +
                                 int(flame_len + cell_len / 2) +
                                 (cell_len / 2),
                                 outline="#FF0000", width=5, tag="CURSOR")

            cvs.create_text(cursor_x * cell_len + int(flame_len + cell_len / 2),
                            cursor_y * cell_len +
                            int(flame_len + cell_len / 2),
                            text=Word_Kanji[tsugi],
                            anchor="center",
                            font=("HG丸ｺﾞｼｯｸM-PRO", 48),
                            fill=Moji_Color[tsugi],
                            tag="CURSOR"
                            )
        draw_block()

    elif index == 6:  # ゲームオーバー
        cvs.delete("DROW")
        timer = timer + 1
        if timer == 1:
            draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 30:
            cvs.delete("OVER")
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE "+str(score), 160, 60, 32, "blue", "INFO")
    draw_txt("HISC "+str(hisc), 450, 60, 32, "yellow", "INFO")
    if tsugi > 0:
        cvs.create_text(752,
                        128,
                        text=Word_Kanji[tsugi],
                        anchor="center",
                        font=("HG丸ｺﾞｼｯｸM-PRO", 48),
                        fill=Moji_Color[tsugi],
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

    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)

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

    """
    cvs.create_text(752,
                        128,
                        text=Word_Kanji[tsugi],
                        anchor="center",
                        font=("HG丸ｺﾞｼｯｸM-PRO", 48),
                        fill=Moji_Color[tsugi],
                        tag="INFO"
                        )
    """

    cvs.create_line(752 - cell_len / 2 - flame_len / 2,
                    128 - cell_len / 2,
                    752 - cell_len / 2 - flame_len / 2,
                    128 + cell_len / 2, width=24, fill=flame_color)
    cvs.create_line(752 - cell_len / 2 - flame_len,
                    128 - cell_len / 2 - flame_len / 2,
                    752 + cell_len / 2 + flame_len,
                    128 - cell_len / 2 - flame_len / 2,
                    width=24,
                    fill=flame_color)
    cvs.create_line(752 + cell_len / 2 + flame_len / 2,
                    128 - cell_len / 2,
                    752 + cell_len / 2 + flame_len / 2,
                    128 + cell_len / 2, width=24, fill=flame_color)
    cvs.create_line(752 - cell_len / 2 - flame_len,
                    128 + cell_len / 2 + flame_len / 2,
                    752 + cell_len / 2 + flame_len,
                    128 + cell_len / 2 + flame_len / 2,
                    width=24,
                    fill=flame_color)
    # cvs.create_line((flame_len + cell_len * cell_x + flame_len / 2), 0,
    #                 (flame_len + cell_len * cell_x + flame_len / 2), cvs_height, width=24, fill=flame_color)
    # cvs.create_line(0, (cvs_height - flame_len / 2), (flame_len + cell_len * cell_x + flame_len / 2),
    #                 (cvs_height - flame_len / 2), width=24, fill=flame_color)

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
        "水",
        "十",
        "一",
        "八",
        "✕"
    ]

    Moji_Color = [
        None,
        "#FF4F02",
        "#FF0461",
        "#005FFF",
        "#00ECFF",
        "#00F9A9",
        "#B6FF01",
        "#FF0000"
    ]

    game_main()
    root.mainloop()
