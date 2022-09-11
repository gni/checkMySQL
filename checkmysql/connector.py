# -*- coding: utf-8 -*-
import pymysql.cursors

class MySQLConn:
    
    @staticmethod
    def create(host, user, password, db, port):
        return Connection(host, user, password, db, port)

class Connection:
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.connect = pymysql.connect


    def __connect__(self):
        self.con = self.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, cursorclass=pymysql.cursors.DictCursor, connect_timeout=2)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()