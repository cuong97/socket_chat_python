from md_chat import ConnectSQL as Conn
import sys
import time
import socket
import threading
print_lock = threading.Lock()


def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("UTF-8")
            print("\nmess_rec: ", msg)
        except OSError:
            break


class User:
    def __init__(self):
        self.id = 1
        self.flag = None
        self.username = None
        self.clientRunning = True

    def sing_in(self):
        username = input("username: ")
        self.username = username
        password = input("password: ")
        conn = Conn()
        conn.open()
        with conn.con:
            if conn.check_sign_in(username, password) > 0:
                self.id = conn.check_sign_in(username, password)
                self.flag = 1
            else:
                print("Sign in fail!")
                self.flag = 0

    def sing_up(self):
        print("-------cac thong tin de dang ky!-------")
        username = input("user: ")
        password = input("pass: ")
        city = input("city: ")
        conObj = Conn()
        conObj.open()
        with conObj.con:
            if conObj.check_city(city) == 0:
                conObj.write_to_city(city, )
            id = conObj.tran_city_to_id(city, )
            conObj.sing_up(username, password, id)

    def sign_out(self):
        self.flag = 0
        print("You was sign out!")

    def show_mess(self, id):
        if self.flag == 1:
            conOb = Conn()
            conOb.open()
            conOb.select_mess(id)

    def show_mess_detail(self, id1):
        if self.flag ==1:
            frien = input("Chon nguoi dung: ")
            conOb = Conn()
            conOb.open()
            id2 = conOb.tran_name_to_id(frien)
            if id2 > 0:
                conOb.show_mess_detail(id1, id2)
            else:
                print("----Tai khoan khong ton tai----\n")

    def show_friend(self, id):
        if self.flag:
            conOb = Conn()
            conOb.open()
            conOb.show_friend(id)
        else:
            print("Ban chua dang nhap\n")

    def send_mess(self, id):
        if self.flag == 1:
            SERVER = "127.0.0.1"
            PORT = 8080
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((SERVER, PORT))
                print('Connected to chat server', SERVER)
                MESSAGE = "Hello server, World!"
                client.sendall(bytes(MESSAGE, 'UTF-8'))
                conOb = Conn()
                conOb.open()
                self.show_friend(id)
                namefr = input("Nhap ten ban be: ")
                id2 = conOb.tran_name_to_id(namefr)
                if id2 > 0:
                    try:
                        sta = 1
                        localtime = time.asctime(time.localtime(time.time()))
                        seconds = time.time()
                        while True:
                            threading.Thread(target=receive, args=(client,)).start()
                            print_lock.acquire()
                            mess = input("Nhap tin nhan:")
                            client.sendall(bytes(mess, 'UTF-8'))
                            #conOb.write_mess(int(id), int(id2), str(mess), str(localtime), int(sta), float(seconds))
                            print_lock.release()
                        client.close()
                        conOb.show_mess_detail(id, id2)
                        print("gui thanh cong")
                    except EOFError:
                        pass
                else:
                    print("Tai khoan khong ton tai.")
            except:
                conOb = Conn()
                conOb.open()
                self.show_friend(id)
                namefr = input("Nhap ten ban be: ")
                id2 = conOb.tran_name_to_id(namefr)
                if id2 > 0:
                    try:
                        sta = 1
                        localtime = time.asctime(time.localtime(time.time()))
                        seconds = time.time()
                        mess = input("Nhap tin nhan:")
                        conOb.write_mess(int(id), int(id2), str(mess), str(localtime), int(sta), float(seconds))
                        conOb.show_mess_detail(id, id2)
                        print("gui thanh cong")
                    except EOFError:
                        pass
                else:
                    print("Tai khoan khong ton tai.")

    def add_friend(self, id1):
        if self.flag == 1:
            newfr = input("Nhap ten nguoi ban muon them: ")
            conOb = Conn()
            conOb.open()
            id2 = conOb.tran_name_to_id(newfr)
            if id2 > 0:
                if conOb.check_block(id1, id2) == 0 and conOb.check_friend(id1, id2) == 0:
                    conOb.write_to_friend(id1, id2)
                    conOb.show_friend(id1)
                else:
                    print("You were blocked by her  or You was friend")
            else:
                print("Tai khoan khong ton tai")
        else:
            print("Ban chua dang nhap")

    def block(self, id1):
        if self.flag == 1:
            conOb = Conn()
            conOb.open()
            self.show_friend(id)
            namefr = input("Nhap ten ban be: ")
            id2 = conOb.tran_name_to_id(namefr)
            if id2 > 0:
                conOb.block(id1, id2)
                conOb.show_friend(id1)
            else:
                print("Tai khoan khong ton tai.")

    def receiveMsg(selt, sock):
        serverDown = False
        while selt.clientRunning and (not serverDown):
            try:
                msg = sock.recv(1024).decode('ascii')
                print(msg)
            except:
                print('Server is Down. You are now Disconnected. Press enter to exit...')
                serverDown = True

    def send_socket(self, id):
        if self.flag == 1:
            SERVER = "127.0.1.1"
            PORT = 8080
            uname = self.username
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((SERVER, PORT))
                print('Connected to chat server', SERVER)
                client.send(uname.encode('ascii'))
                threading.Thread(target=User.receiveMsg, args=(self, client,)).start()
                while self.clientRunning:
                    tempMsg = input()
                    msg = uname + '>>' + tempMsg
                    if '**quit' in msg:
                        self.clientRunning = False
                        client.send('**quit'.encode('ascii'))
                    else:
                        client.send(msg.encode('ascii'))
            except:
                conOb = Conn()
                conOb.open()
                self.show_friend(id)
                namefr = input("Nhap ten ban be: ")
                id2 = conOb.tran_name_to_id(namefr)
                if id2 > 0:
                    try:
                        sta = 1
                        localtime = time.asctime(time.localtime(time.time()))
                        seconds = time.time()
                        mess = input("Nhap tin nhan:")
                        conOb.write_mess(int(id), int(id2), str(mess), str(localtime), int(sta), float(seconds))
                        conOb.show_mess_detail(id, id2)
                        print("gui thanh cong")
                    except EOFError:
                        pass
                else:
                    print("Tai khoan khong ton tai.")


def clear_screen():
    import os
    os.system("clear")


def main_in():
    clear_screen()
    print("Sign successfuly!")
    print("[1]showmess [2]detailmess [3]sendmess [7]send_socket [4]Addfriend [5]showfr [6]block [8]Detail_friend [9]exit")
    while True:
        choose = int(input("Nhap vao lua chon: "))
        if choose == 1:
            use.show_mess(use.id)
        if choose == 2:
            use.show_mess_detail(use.id)
        if choose == 3:
            use.send_mess(use.id)
        if choose == 4:
            use.add_friend(use.id)
        if choose == 5:
            use.show_friend(use.id)
        if choose == 6:
            use.block(use.id)
        if choose == 7:
            use.send_socket(use.id)
        if choose == 9:
            clear_screen()
            print("[1] login  [2] SingUp  [3] Logout  [4] Exit")
            break


def main():
    try:
        print("[1] login  [2] SingUp  [3] Logout  [4] Exit")
        while True:
            choose = int(input("Nhap vao lua chon: "))
            if choose == 1:
                use.sing_in()
                if use.flag == 1:
                    main_in()
            if choose == 2:
                use.sing_up()
            if choose == 3:
                use.sign_out()
            if choose == 4:
                sys.exit()
    except ValueError:
        print("loi lua chon menu")


if __name__ == '__main__':
    use = User()
    main()
