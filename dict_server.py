"""
电子词典服务器：
功能接受用户请求 进行逻辑处理返回查询结果
    技术点确定
     *并发模型  ： 携程
     *数据传输  ： tcp传输
     *数据库    : 查询
    2.结构设计
      *类封装  将查询操作功能为类

    3.功能模块
        * 搭建网络通信模型

    4.数据表进行建立(dict:words)
        * 用户 user -> id name passwd
         create table user (id int primary key auto_increment ,name varchar(32) not null,passwd varchar(128) not null);
        * 历史记录表 hist-> name word time
        create table hist(id int primary key auto_increment ,name varchar(32) not null,word varchar(28) not null, time datetime default now());
    import hashlib
    生成加密对象
    hash = hashlib.md5()

    对密码进行加密 (passwd)
    hash.update(passwd.encode())

    加密后的密码(返回加密后的字符串)
    pwd = hash.hexdigest()

"""
#导入模块------------------
import gevent
from gevent import monkey
monkey.patch_socket()
from socket import *
import os
from db_handel import Database #导入数据库操作对象
#定义全局变量
SERVER_ADDR = ('127.0.0.1',8080)
#定义电子词典


# 注册方法
def sign_in(c,db):
    data = c.recv(1024).decode()
    data = data.split(' ')
    name = data[0]
    passwd = data[1]
    print(name,passwd)
    if db.sign_in(name,passwd):
        print('ok')
        c.send("OK".encode())
    else:
        c.send('ERROR'.encode())
        print('失败')
#登录
def do_login(c,db):
    data = c.recv(1024).decode()
    data = data.split(' ')
    name = data[0]
    passwd = data[1]
    print(name, passwd)
    if db.db_do_login(name,passwd):
        print('登录成功')
        c.send("OK".encode())
    else:
        c.send('ERROR'.encode())
        print('失败')
#查询单词
def do_query(c,db):
    while True:
        data = c.recv(1024).decode()
        if data == "##":
            return
        data = data.split(' ')
        name = data[0]
        world = data[1]
        # 没找到返回None 找到返回单词解释
        mean = db.query(world)
        # 添加信息到历史记录表
        db.inser_hist(name,world)
        if not mean:
            print('没找到单词')
            c.send('None'.encode())
        else:
            print('找到单词')
            c.send(mean.encode())

#查找历史记录
def do_hist(c,db):
    data = c.recv(1024).decode()
    data = data.split(' ')
    request = data[0]
    name = data[1]
    if request == 'ALLHIST':
        hist_msg = db.get_all_hist(name)
    elif request == "TENHIST":
        hist_msg = db.get_ten_hist(name)
    c.send(str(hist_msg).encode())

def handle(c):
    # 链接数据库
    db = Database(database='dict')
    db.connect_database()
    db.create_cursor()
    while True:
        try:
            data = c.recv(1024).decode()
        except KeyboardInterrupt:
            print('服务器意外退出')
            break
        if not data:
            break
        print(c.getpeername(),":",data)
        if data == 'LOGIN':
            #登录
            do_login(c,db)
        elif data == 'SIGN_IN':
            sign_in(c,db)
        elif data == 'EXIT':
            print(c.getpeername,': 退出')
            break
        elif data == "QUERY":
            do_query(c,db)
        elif data == "HIST":
            do_hist(c,db)


def main():

    #创建网络套接字
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(SERVER_ADDR)
    sockfd.listen(6)



    #建立链接 创建携程对象 循环接受多客户请求
    while True:
        print('wait...')
        try:
            conn, addr = sockfd.accept()
        except KeyboardInterrupt:
            print('服务器退出')
        print('conn from ', addr)
        gevent.spawn(handle,conn)

if __name__ == '__main__':
    main()