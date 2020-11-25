from socket import *


def send_response(c, filename):
    with open(filename) as f:
        data = f.read()

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"
    response += data

    c.send(response.encode())


def recv_request(c):
    data = c.recv(1024 * 10)
    print(data.decode())


def main():
    s = socket()
    s.bind(("0.0.0.0",8800))
    s.listen(5)

    while True:
        c,addr = s.accept()
        print("Connect from",addr)
        recv_request(c)
        send_response(c,"zhihu.html")
        c.close()

    s.close()

if __name__ == '__main__':
    main()