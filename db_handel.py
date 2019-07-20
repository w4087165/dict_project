"""
数据库操作模块
增加 删除 修改 查询
"""
#查询
import pymysql
import hashlib
SAlT = '#YAN' #加盐

#创建数据库操作对象
class Database:
    def __init__(self,host='localhost',port=3306, user='root',password='123456',database='None',charset='utf8'):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    # 链接数据库
    def connect_database(self):
        self.db = pymysql.connect(host = self.host,
                     port = self.port,
                     user = self.user,
                     password = self.password,
                     database = self.database,
                     charset = self.charset)

    def close(self):
        self.db.close()

    def create_cursor(self):
        # 创建游标对象
        self.cur = self.db.cursor()

    def sign_in(self,name,passwd):
        passwd = passwd
        name = name
        sql = "select * from user where name = %s"
        result = self.cur.execute(sql,[name])
        print(result,type(result))
        if result < 1:
            try:
                #密码加密
                hash = hashlib.md5((name+SAlT).encode())
                hash.update(passwd.encode())
                passwd = hash.hexdigest()
                sql = 'insert into user(name,passwd) value(%s,%s)'
                self.cur.execute(sql,[name,passwd])
                self.db.commit()
                print('注册成功 欢迎登录')
                return True
            except Exception as e:
                self.db.rollback()
                print(e)
                return False
        else:
            print('错误 已有此用户')
            self.db.rollback()

    #登录
    def db_do_login(self,name,passwd):
        name = name
        passwd = passwd
        #加密 和数据库匹配
        hash = hashlib.md5((name + SAlT).encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        try:
            sql = 'select * from user where name = %s and passwd = %s'
            self.cur.execute(sql, [name, passwd])
            result = self.cur.fetchone()
            print(result)
            if not result:
                print('用户名或密码错误')
                return False
            return True
        except Exception as e:
            print('错误', e)
            self.db.rollback()
            return False

    #查单词
    def query(self,word):
        sql = "select decipher from worlds where worlds = %s"
        self.cur.execute(sql,[word])
        r= self.cur.fetchone()
        if r:
            return r[0]
    #插入历史记录
    def inser_hist(self,name,word):
        sql = 'insert into hist(name,word) values (%s,%s)'
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
            print('存入表成功')
        except Exception:
            self.db.rollback()
            print('存入历史失败')
    def get_all_hist(self,name):
        sql = 'select * from hist where name = %s'
        self.cur.execute(sql,[name])
        result = self.cur.fetchall()
        if result:
            #如果查到返回查找结果
            return result

        return '暂无历史信息'

    def get_ten_hist(self,name):
        sql = "select * from hist where name = %s order by time desc limit 10"
        self.cur.execute(sql, [name])
        result = self.cur.fetchall()
        if result:
            # 如果查到返回查找结果
            return result

        return '暂无历史信息'

