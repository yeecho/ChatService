import json
from typing import Optional, Awaitable

import tornado.web
import tornado.websocket

import db


class RegisterHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        print(bytes)

    def get(self):
        self.render('register.html')

    def post(self):
        str_info = bytes.decode(self.request.body)
        print('str_info:', str_info)
        self.register(str_info)

    def register(self, info):
        values = info.split('&')
        cid = values[0].split('=')[1]
        name = values[1].split('=')[1]
        password = values[2].split('=')[1]
        print(cid, name, password)
        r = db.insertUser((cid, name, password))
        self.write(r[1])


class LoginHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        print(bytes)

    def get(self):
        pass

    def post(self):
        content = bytes.decode(self.request.body)
        print('content:', content)
        self.login(content)

    def login(self, content):
        dct = {'result': False}
        try:
            d = json.loads(content)
            cid = d['cid']
            password = d['password']
            # 数据库中进行账号和密码校验
            r = db.loginCheck(cid, password)
            print(r)
            if r[0]:
                dct['result'] = True
                dct['cid'] = cid
                dct['name'] = r[1][0]
                dct['contact'] = r[1][1]
            else:
                dct['reason'] = r[1]
            self.write(json.dumps(dct))
            print(dct)
        except:
            dct['reason'] = '登录请求解析错误'
            self.write(json.dumps(dct))
            print('登录请求解析错误')


class ChatHandler(tornado.websocket.WebSocketHandler):

    onlineUsers = dict()

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        print(bytes)

    def open(self, *args: str, **kwargs: str):
        print('发现一个链接')

    def on_message(self, message):
        try:
            info = json.loads(message)
            msgType = info['MsgType']
            srcId = info['cid']
            if msgType == 'handshake':
                self.handshake(srcId)
            elif msgType == 'chat':
                desId = info['DesId']
                text = info['text']
                self.chat(desId, text, srcId)
        except Exception as e:
            print(e)
            self.write('数据解析出错')

    def on_close(self) -> None:
        # 获取当前断开链接的websocket的key并删除该键值对
        index = list(self.onlineUsers.values()).index(self)
        print('index:', index)
        cid = list(self.onlineUsers.keys())[index]
        self.onlineUsers.pop(cid)
        # cid = list(self.onlineUsers.keys())[list(self.onlineUsers.values()).index(self)]
        # print('用户%s断开链接:' % cid)
        # self.onlineUsers.pop(cid)

    def handshake(self, cid):
        dct = {'MsgType': 'system'}
        try:
            if str(cid) in self.onlineUsers.keys():
                print('%s已在线，挤掉它' % cid)
                # 通知已上线的客户端，被人挤占，必须退出
                dct['code'] = 400
                handler = self.onlineUsers[cid]
                log = json.dumps(dct)
                print(handler, '即将被挤下线', log)
                handler.write_message(log)
                # self.onlineUsers[cid].write_message(json.dumps(dct))
                # 通知当前客户端，挤占上线成功
                dct['code'] = 201
                self.write_message(json.dumps(dct))
                self.onlineUsers[str(cid)] = self
            else:
                print('%s上线' % cid)
                self.onlineUsers[cid] = self
                dct['code'] = 200
                self.write_message(json.dumps(dct))
        except Exception as e:
            print(e)
        print(self.onlineUsers)

    def chat(self, desId, text, srcId):
        print(desId, text, srcId)
        dct = {'MsgType': 'chat', 'SrcId': srcId, 'text': text}
        handler = self.onlineUsers[desId]
        print(handler)
        s = json.dumps(dct)
        print(s)
        handler.write_message(s)

