"""
客户端
    功能：
    登录 注册客户端
    登录成功后 连接服务器 进行词典操作



"""
#导入模块

from socket import socket
from menu_view import *     # 导入菜单
import getpass   #只能运行于终端getpass.getpass  密码输入隐藏
import re

#登录
def login():
    # 向服务器发送一次登录请求
    sockfd.send('LOGIN'.encode())
    name = input('User：')
    passwd = getpass.getpass('输入密码:')
    msg = "%s %s"%(name,passwd)
    sockfd.send(msg.encode())
    #接收消息
    data = sockfd.recv(1024).decode()
    if data == "OK":
        #进入二级界面
        select_dict(name)
    else:
        print('用户名密码错误', data)
    return False
#注册
def sign_in():
    #向服务器发送一次注册请求
    sockfd.send('SIGN_IN'.encode())
    while True:
        name = input('Uers name:')
        passwd = getpass.getpass('password:')
        passwd1 = getpass.getpass('please input password again:')
        if passwd != passwd1:
            print('两次密码不一致')
            continue
        #空格检测
        if " " in name or " " in passwd:
            print('用户名密码不能有空格')
            continue
        #向服务器发送注册请求
        msg = '%s %s'%(name,passwd)
        sockfd.send(msg.encode())
        #接受服务器返回信息
        data = sockfd.recv(1024).decode()
        if data == 'OK':
            # 进入二级界面
            select_dict(name)
        else:
            print('注册失败',data)
        return False
#退出
def exit():
    sockfd.send('EXIT'.encode())

#查询单词
def do_query(name):
    sockfd.send('QUERY'.encode())
    while True:
        word = input('单词：')
        if word == "##": #结束查询
            sockfd.send(word.encode())
            break
        msg = "%s %s"%(name,word)
        sockfd.send(msg.encode())
        data = sockfd.recv(4096).decode()
        print('查询结果',data)
#历史记录
def do_hist(name):
    sockfd.send('HIST'.encode())
    msg = input('[1] 全部历史记录\n'
                '[2] 最近前10条记录\n')
    if msg == "1":
        msg = 'ALLHIST %s'%name
        sockfd.send(msg.encode())
    elif msg == "2":
        msg = 'TENHIST %s'%name
        sockfd.send(msg.encode())
    data = sockfd.recv(4096).decode()
    data = re.findall(r'\(.+?\(.+?\)\)',data)
    for i in data:
        print(i)




#定义全局变量
ADDR = ('127.0.0.1',8080)
sockfd = socket()
sockfd.connect(ADDR)
#查单词
def select_dict(name):
    #二级界面
    while True:
        s = input(second_menu)
        if s == '1':
            do_query(name)
        elif s == '2':
            # 历史记录
            do_hist(name)
        elif s == '3':
            # 退出
            break

def main():
    #主循环
    while True:
        s = input(first_menu)
        if s == '1':
            login()
        elif s == '2':
            sign_in()
        elif s == '3':
            exit()
            break #退出


    #关闭套接字
    sockfd.close()


if __name__ == '__main__':
    main()