import threading
import socket


class Threading_socket():
    def __init__(self, gui):
        super().__init__()
        self.dataReceive = ""
        self.conn = None
        self.gui = gui
        self.name = ""

    def clientAction(self, inputIP):
        try:
            self.name = "client"
            print("client connect ...............")
            HOST = inputIP  # Cấu hình địa chỉ server
            PORT = 8000              # Cấu hình Port sử dụng
            self.conn = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)  # Cấu hình socket
            self.conn.connect((HOST, PORT))  # tiến hành kết nối đến server
            t1 = threading.Thread(target=self.client)  # tạo luồng chạy client
            t1.start()
            self.gui.notification("Đã kết nối tới", str(HOST))
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def client(self):
        try:
            while True:
                self.dataReceive = self.conn.recv(
                    1024).decode()  # Đọc dữ liệu server trả về
                if (self.dataReceive != ""):
                    print(f"client {self.dataReceive}")
                    friend = self.dataReceive.split("|")[0]
                    action = self.dataReceive.split("|")[1]
                    if (action == "hit" and friend == "server"):
                        x = int(self.dataReceive.split("|")[2])
                        y = int(self.dataReceive.split("|")[3])
                        self.gui.handleButton(x, y)
                    if (action == "Undo" and friend == "server"):
                        self.gui.Undo(False)
                self.dataReceive = ""
        except Exception as err:
            print(err)

    def serverAction(self):
        try:
            self.name = "server"
            HOST = socket.gethostbyname(
                socket.gethostname())  # Láy  lập địa chỉ
            print("Make host.........." + HOST)
            self.gui.notification("Gui IP cho ban", str(HOST))
            PORT = 8000  # Thiết lập port lắng nghe
            # cấu hình kết nối
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))  # lắng nghe
            s.listen(1)  # thiết lập tối ta 1 kết nối đồng thời
            self.conn, addr = s.accept()  # chấp nhận kết nối và trả về thông số
            t2 = threading.Thread(target=self.server, args=(addr, s))
            t2.start()
            self.gui.notification("Đã Kết Nối ....",
                                  str("Đã Kết Nối ...."))
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            s.close()  # đóng socket

    def server(self, addr, s):
        try:
            # in ra thông địa chỉ của client
            print('Connected by', addr)
            while True:
                # Đọc nội dung client gửi đến
                self.dataReceive = self.conn.recv(1024).decode()
                print(f"server : {self.dataReceive}")
                if (self.dataReceive != ""):
                    friend = self.dataReceive.split("|")[0]
                    action = self.dataReceive.split("|")[1]
                    if (action == "hit" and friend == "client"):
                        x = int(self.dataReceive.split("|")[2])
                        y = int(self.dataReceive.split("|")[3])
                        self.gui.handleButton(x, y)
                    if (action == "Undo" and friend == "client"):
                        self.gui.Undo(False)
                self.dataReceive = ""
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        finally:
            s.close()  # đóng socket

    def sendData(self, data):
        # Gửi dữ liệu lên server`
        try:
            self.conn.sendall(str("{}|".format(self.name) + data).encode())
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
