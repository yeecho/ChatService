import tornado.ioloop
import tornado.web
import handler
import db

handlers = [
            ('/register', handler.RegisterHandler),
            ('/login', handler.LoginHandler),
            ('/chat', handler.ChatHandler)
        ]

if __name__ == '__main__':

    db.createTable(db.SQL_CREATE_USER)

    app = tornado.web.Application(handlers)
    app.listen(8088)
    tornado.ioloop.IOLoop.current().start()
