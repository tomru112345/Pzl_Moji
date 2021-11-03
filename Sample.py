import tkinter
key = ""
kdown = False


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


def main():
    fnt = ("Times New Roman", 30)
    txt = "mouse({},{})".format(key, kdown)
    cvs.delete("TEST")
    cvs.create_text(456, 384, text=txt, fill="black", font=fnt, tag="TEST")
    root.after(100, main)


root = tkinter.Tk()
root.title("キー")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
cvs = tkinter.Canvas(root, width=912, height=768)
cvs.pack()
main()
root.mainloop()
