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

    4.协议确定

      L  请求文件列表
      Q  退出
      G  下载文件
      P  上传文件
"""
#导入模块------------------
import gevent
from gevent import monkey
monkey.patch_socket()
from socket import *
import pymysql
from sql_config import * #导入数据库配置
#定义全局变量
SERVER_ADDR = ('127.0.0.1',8080)
SQL_CONFIG = MySQLConfig()

#定义电子词典查询类
class DictServer():
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def handle(self,c):
        while True:
            print('asdfsadf')
            data = c.recv(1024).decode()
            if not data:
                break
            print(data)
            c.send(b'OK')

    # 循环接受客户端请求
    def do_connect(self):
        print('Waiting connect ... ')
        while True:
            print('sdfasdfasdfasdf')
            conn, addr = self.sockfd.accept()
            print('conn from ', addr)
            gevent.spawn(self.handle, conn)


def main():

    #创建网络套接字
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(SERVER_ADDR)
    sockfd.listen(6)

    #建立链接 创建携程对象 循环接受多客户请求
    dict_server = DictServer(sockfd)
    g_c = gevent.spawn(dict_server.do_connect())
    gevent.joinall([g_c])





if __name__ == '__main__':
    main()