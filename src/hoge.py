import tkinter as tk
from tkinter import messagebox
import pokewordle

baseGround = tk.Tk()
select_level = tk.IntVar(value=0)
levels = [
    "公式(～第4世代)",
    "第1世代のみ(1)",
    "第2世代のみ(2)",
    "第3世代のみ(3)",
    "第4世代のみ(4)",
    "第5世代のみ(5)",
]

class GameManager:
    def __init__(self, bg):
        self.baseGround = bg
        self._initialize()

    def _initialize(self):
        self.labels = []
        self.input = None
        self.in_game = True

        self.gm = pokewordle.GameManager(select_level.get())
        self.fifty_table = pokewordle.FiftyTable()
        self.answer_count = 0

    def update_word(self, text, color):
        self.labels[self.answer_count].configure(state='normal')
        self.labels[self.answer_count].insert('end', text, color)
        self.labels[self.answer_count].configure(state='disabled')

    def input_end(self):
        self.input.delete(0, tk.END)
        self.input.insert('end', self.gm.get_answer())
        self.input.configure(state='disabled')

    def func(self, event):
        if not self.in_game:
            return
        text1 = self.input.get()
        # 空文字
        if text1 == "":
            return
        self.input.delete(0, tk.END)
        responce = self.gm.hit(text1)
        # 存在しないポケモン
        if responce["result"] == -1:
            return

        result = responce["cells"]
        self.fifty_table.updates(result)

        count = 0
        for item in result:
            if item.state == pokewordle.CellState.GREEN:
                self.update_word(item.char, "green")
                count += 1
            elif item.state == pokewordle.CellState.ORANGE:
                self.update_word(item.char, "orange")
            elif item.state == pokewordle.CellState.MISS:
                self.update_word(item.char, "black")
        if count >= 5:
            self.input_end()
            self.in_game = False

        self.answer_count += 1
        if self.answer_count >= 10:
            self.input_end()
            self.in_game = False

        self.update_draw_fifty()

    def update_draw_fifty(self):
        self.fifty_ui.configure(state='normal')
        self.fifty_ui.delete("1.0","end")
        count = 0
        for item, value in self.fifty_table.fifty.items():
            if count >= 17:
                count = 0
                self.fifty_ui.insert('end', "\n")
            if item in ["ヰ","ヱ","ヵ","ヲ","ヶ"]:
                self.fifty_ui.insert('end', f'{item}', "invisible")
            elif value == pokewordle.CellState.INIT:
                self.fifty_ui.insert('end', f'{item}')
            elif value == pokewordle.CellState.ORANGE:
                self.fifty_ui.insert('end', f'{item}', "orange")
            elif value == pokewordle.CellState.GREEN:
                self.fifty_ui.insert('end', f'{item}', "green")
            else:
                self.fifty_ui.insert('end', f'{item}', "black")
            count += 1
        self.fifty_ui.configure(state='disabled')

    def main(self):
        for i in range(10):
            c = tk.Text(state='disabled', height=1, width=10, wrap="none")
            c.grid(row=i%5, column=int(i/5), padx=0, pady=0)
            c.tag_configure("green", foreground="white", background="green")
            c.tag_configure("orange", foreground="white", background="orange")
            c.tag_configure("black", foreground="gray", background="white")
            self.labels.append(c)

        # 入力欄の作成
        self.input = tk.Entry(width=20)
        self.input.grid(row=4, column=2, columnspan=1)
        self.input.bind('<Return>', self.func)

        # 五十音表の作成
        self.fifty_ui = tk.Text(state='normal', height=5, width=34, wrap="none")
        self.fifty_ui.grid(row=0, column=2, rowspan=4)
        self.fifty_ui.tag_configure("green", foreground="white", background="green")
        self.fifty_ui.tag_configure("orange", foreground="white", background="orange")
        self.fifty_ui.tag_configure("black", foreground="lightgray", background="white")
        self.fifty_ui.tag_configure("invisible", foreground="white", background="white")
        self.update_draw_fifty()

        self.baseGround.mainloop()

    def regenerate(self, event=None):
        for item in self.labels:
            item.destroy()
        self.input.destroy()
        self.fifty_ui.destroy()

        self._initialize()
        self.main()

def show_version():
    msg = "バージョン 1.0.0\n\nCopyright (C) 2021 わい"
    messagebox.showinfo("バージョン情報", msg)

gm = GameManager(baseGround)

# ウィンドウのタイトルを設定
baseGround.title('Poke-Wordle')
baseGround.resizable(False, False)
# メニューバーの作成
menubar = tk.Menu(baseGround)
baseGround.config(menu=menubar)
game_menu = tk.Menu(menubar, tearoff=0)
game_menu.add_command(label='リセット(R)', under=5, accelerator="Ctrl+R", command=gm.regenerate)
# game_menu.add_separator()
game_menu.add_command(label='終了(X)', under=3, command=baseGround.destroy)
menubar.add_cascade(label="ファイル(F)", menu=game_menu, under=5)
mode_menu  = tk.Menu(menubar, tearoff=0)

mode_menu.add_radiobutton(label=levels[0], variable=select_level, value=0)
mode_menu.add_separator()
for item in range(1, len(levels)):
    mode_menu.add_radiobutton(label=levels[item], variable=select_level, value=item)
menubar.add_cascade(label='モード(M)', menu=mode_menu, under=4)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label='バージョン情報(V)…', under=8, command=show_version)
menubar.add_cascade(label='ヘルプ(H)', menu=help_menu, under=4)
baseGround.bind_all("<Control-r>", gm.regenerate)



gm.main()
