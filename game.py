import tkinter as tk
from functools import partial
from tkinter import messagebox
from thread_socket import Threading_socket


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cờ Caro - Socket")
        self.Buts = {}
        self.board = []
        self.name = ""
        self.myTurn = False
        self.Threading_socket = Threading_socket(self)
        print(self.Threading_socket.name)

    def showFrame(self):
        frame1 = tk.Frame(self)
        frame1.pack()
        frame2 = tk.Frame(self)
        frame2.pack()

        Undo = tk.Button(frame1, text="Undo", width=10,  # nút quay lại
                         command=partial(self.Undo, synchronized=True))
        Undo.grid(row=0, column=0, padx=30)

        tk.Label(frame1, text="IP", pady=4).grid(row=0, column=1)
        inputIp = tk.Entry(frame1, width=20)  # Khung nhập địa chỉ ip
        inputIp.grid(row=0, column=2, padx=5)
        connectBT = tk.Button(frame1, text="Kết Nối", width=10,
                              command=lambda: self.Threading_socket.clientAction(inputIp.get()))
        connectBT.grid(row=0, column=3, padx=3)

        makeHostBT = tk.Button(frame1, text="Tạo Host", width=10,  # nút tạo host
                               command=lambda: self.Threading_socket.serverAction())
        makeHostBT.grid(row=0, column=4, padx=30)
        for x in range(Ox):   # tạo ma trận button Ox * Oy
            for y in range(Oy):
                self.Buts[x, y] = tk.Button(frame2, font=('arial', 15, 'bold'), height=1, width=2,
                                            borderwidth=2, command=partial(self.handleButton, x=x, y=y))
                self.Buts[x, y].grid(row=x, column=y)

    def handleButton(self, x, y):
        try:
            if self.Buts[x, y]['text'] == "":  # Kiểm tra ô có ký tự rỗng hay không
                if self.board.count([x, y]) == 0:
                    self.board.append([x, y])
                if len(self.board) % 2 == 1:
                    self.Buts[x, y]['text'] = 'O'
                    self.Threading_socket.sendData(
                        "{}|{}|{}|".format("hit", x, y))
                    if (self.checkWin(x, y, "O")):
                        self.notification("Winner", "O")
                        self.newGame()
                else:
                    print(self.Threading_socket.name)
                    self.Buts[x, y]['text'] = 'X'
                    self.Threading_socket.sendData(
                        "{}|{}|{}|".format("hit", x, y))
                    if (self.checkWin(x, y, "X")):
                        self.notification("Winner", "X")
                        self.newGame()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def notification(self, title, msg):
        try:
            messagebox.showinfo(str(title), str(msg))
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def checkWin(self, x, y, XO):
        try:
            count = 0
            i, j = x, y
            while (j < Ox and self.Buts[i, j]["text"] == XO):
                count += 1
                j += 1
            j = y
            while (j >= 0 and self.Buts[i, j]["text"] == XO):
                count += 1
                j -= 1
            if count >= 6:
                return True
            # check cột
            count = 0
            i, j = x, y
            while (i < Oy and self.Buts[i, j]["text"] == XO):
                count += 1
                i += 1
            i = x
            while (i >= 0 and self.Buts[i, j]["text"] == XO):
                count += 1
                i -= 1
            if count >= 6:
                return True
            # check cheo phai
            count = 0
            i, j = x, y
            while (i >= 0 and j < Ox and self.Buts[i, j]["text"] == XO):
                count += 1
                i -= 1
                j += 1
            i, j = x, y
            while (i <= Oy and j >= 0 and self.Buts[i, j]["text"] == XO):
                count += 1
                i += 1
                j -= 1
            if count >= 6:
                return True
            # check cheo trai
            count = 0
            i, j = x, y
            while (i < Ox and j < Oy and self.Buts[i, j]["text"] == XO):
                count += 1
                i += 1
                j += 1
            i, j = x, y
            while (i >= 0 and j >= 0 and self.Buts[i, j]["text"] == XO):
                count += 1
                i -= 1
                j -= 1
            if count >= 6:
                return True
            return False
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def Undo(self, synchronized):
        try:
            if (len(self.board) > 0):
                x = self.board[len(self.board) - 1][0]
                y = self.board[len(self.board) - 1][1]
                # print(x,y)
                self.Buts[x, y]['text'] = ""
                self.board.pop()
                if synchronized == True:
                    self.Threading_socket.sendData("{}|".format("Undo"))
                print(self.board)
            else:
                print("No character")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def newGame(self):
        try:
            self.board = []
            for x in range(Ox):
                for y in range(Oy):
                    self.Buts[x, y]["text"] = ""
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    try:
        Ox = 15  # Số lượng ô theo trục X
        Oy = 20  # Số lượng ô theo trục Y
        window = Window()
        window.showFrame()
        window.mainloop()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
