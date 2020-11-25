"""
基于 select 的 IO并发模型
select_server.py
重点代码！！！
"""

from socket import *
from select import *

# 创建全局变量
HOST = "0.0.0.0"
PORT = 8800
ADDR = (HOST, PORT)

# 创建套接字
sockfd = socket()
sockfd.bind(ADDR)
sockfd.listen(5)

sockfd.setblocking(False)
ep = epoll()
ep.register(sockfd, EPOLLIN)

map = {sockfd.fileno(): sockfd}

# 循环监控关注的IO
while True:
    events = ep.poll()
    # 对监控的套接字就绪情况分情况讨论
    for fd, event in events:
        if fd == sockfd.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            # 连接一个客户端就多监控一个
            connfd.setblocking(False)
            ep.register(connfd, EPOLLIN | EPOLLERR)
            map[connfd.fileno()] = connfd
        elif event == EPOLLIN:
            # 某个客户端连接套接字就绪
            data = map[fd].recv(1024).decode()
            # 客户端退出
            if not data:
                ep.unregister(fd)  # 删除监控
                map[fd].close()
                del map[fd]
                continue
            print(data)
            map[fd].send(b'OK')
