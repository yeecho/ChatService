import unittest
import sqlite3
import db

# python -m unittest


class TestCase(unittest.TestCase):

    def test_check(self):
        conn = sqlite3.connect(db.DB)
        cs = conn.cursor()
        sql = 'select * from chat_user'
        r = cs.execute(sql).fetchall()
        for item in r:
            print(item)
        conn.commit()
        cs.close()
        conn.close()

    def test_insert(self):
        data = (123, 'yuyu', 123)
        rowid = db.insertUser(data)
        print(rowid, data)

    def test_isRegisted(self):
        r = db.isRegistered(123)
        print(type(r), r)

    def test_find_column(self):
        column = 'password'
        sql = 'select ' + column + ' from chat_user where id = ' + str(id)

    def test_delete_user(self):
        db.deleteUser(123)

    def test_update(self):
        sql = 'update chat_user set contact = "[""1234"", ""12345""]" where cid = 123'
        conn = sqlite3.connect(db.DB)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()