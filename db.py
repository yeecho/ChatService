import json
import sqlite3

DB = 'yc.db'
TB_USER = 'chat_user'

SQL_CREATE_USER = '''
        create table if not exists chat_user(
            cid text primary key,
            name text,
            password text,
            contact text
        )
    '''


def createTable(sql):
    conn = sqlite3.connect(DB)
    cs = conn.cursor()
    cs.execute(sql)
    conn.commit()
    cs.close()
    conn.close()


def insertUser(data):
    if isExist(data[0]):
        return False, '账号已存在'
    sql = 'insert into chat_user(cid, name, password) values(?, ?, ?)'
    conn = sqlite3.connect(DB)
    cs = conn.cursor()
    r = cs.execute(sql, data).lastrowid
    conn.commit()
    cs.close()
    conn.close()
    print(type(r), r)
    if r > 0:
        return True, '注册成功, 恭喜您成为第%s位用户' % r
    else:
        return False, '注册失败'


def deleteUser(cid):
    if not isExist(cid):
        return
    sql = 'delete from chat_user where cid = ' + str(cid)
    conn = sqlite3.connect(DB)
    cs = conn.cursor()
    cs.execute(sql)
    conn.commit()
    cs.close()
    conn.close()


def updateUser():
    pass


def isExist(cid):
    sql = 'select * from chat_user where cid = ' + str(cid)
    conn = sqlite3.connect(DB)
    cs = conn.cursor()
    r = cs.execute(sql).fetchone()
    cs.close()
    conn.close()
    return r is not None


def loginCheck(cid, pswd):
    sql = 'select password, name, contact from chat_user where cid = ' + str(cid)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    r = cur.execute(sql).fetchone()
    if r is not None:
        if str(pswd) == r[0]:
            name = r[1]
            contact = r[2]
            contacts = list()
            if contact:
                try:
                    lst = json.loads(contact)
                    for cid in lst:
                        sql = 'select name from chat_user where cid = ' + str(cid)
                        r = cur.execute(sql).fetchone()
                        contacts.append((str(cid), r[0]))
                except Exception as e:
                    print('联系人数据解析错误')
                    print(e)
            return True, (name, contacts)
        else:
            return False, '密码错误'
    else:
        return False, '账号不存在'

