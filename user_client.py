"""
客户端
    功能：
    登录 注册客户端
    登录成功后 连接服务器 进行词典操作
"""
#导入模块

from socket import socket

sockfd = socket()
ADDR = ('127.0.0.1',8080)

sockfd.connect(ADDR)
while True:
    try:
        msd = input('》》》')


    except KeyboardInterrupt:
        print('客户端退出')
        break
    if not msd:
        break
    try:
        sockfd.send(msd.encode())
    except BrokenPipeError:
        print('服务器 错误')
        break
    data = sockfd.recv(1024)
    print(data.decode())
sockfd.close()