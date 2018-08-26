import socket
import sys
import threading

print_lock = threading.Lock()

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("UTF-8")
            print("client: ", msg)
        except OSError:
            break

def handle_client(client):
    while True:
        threading.Thread(target=receive, args=(client,)).start()
        out_data = input(">> ")
        if out_data == bytes("{quit}", "utf8"):
            client.close()
            break
        else:
            client.sendall(bytes(out_data, 'UTF-8'))
    client.close()

def Main():
    host = "127.0.0.1"
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print(addr, "Has Connection to the server")
        threading.Thread(target=handle_client, args=(c,)).start()
    s.close()


if __name__ == '__main__':
    Main()
