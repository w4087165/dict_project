"""
mysql 信息配置文件

"""

class MySQLConfig():
    def __init__(self):
        self.host = 'localhost',
        self.port = 3306,
        self.user = 'root',
        self.password = '123456',
        self.database = 'dict',
        self.charset = 'utf8'
