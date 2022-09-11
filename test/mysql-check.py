import unittest
from checkmysql.connector import MySQLConn


class MySQLTest(unittest.TestCase):
    def test_connection(self):
        con = MySQLConn.create('localhost', 'test', 'test', 'test', 3306)
        res = con.fetch("select 1 as checkin;")

        if res[0].get('checkin', None) == 1:
            print('db check ok')
        else:
            print('db check ko')

if __name__ == "__main__":
    unittest.main()