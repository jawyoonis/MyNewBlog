# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlalchemy 
import unittest 
from flask.ext.sqlalchemy import SQLAlchemy 
from flask_blog import db, app 


#modesl 

from author.models import*
from blog.models import*

class UserTest(unittest.TestCase):
    def setUp(self):
        db_username= app.config["DB_USERNAME"]
        db_password= app.config["DB_PASSWORD"]
        db_host= app.config["DB_HOST"]
        self.db_uri= "mysql+pymysql://%s:%s@%s/" % (db_username, db_password, db_host)
        app.config["TESTING"]=True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["BLOG_DATABASE_NAME"]='test_blog'
        app.config['SQLALCHEMY_DATABASE_URI']= self.db_uri + app.config["BLOG_DATABASE_NAME"]
        engine= sqlalchemy.create_engine(self.db_uri)
        conn= engine.connect()
        conn.execute("commit")
        conn.execute("CREATE DATABASE " + app.config["BLOG_DATABASE_NAME"])
        db.create_all()
        conn.close()
        self.app= app.test_client()
    def tearDown(self):
        db.session.remove()
        engine= sqlalchemy.create_engine(self.db_uri)
        conn= engine.connect()
        conn.execute("commit")
        conn.execute("DROP DATABASE " + app.config["BLOG_DATABASE_NAME"])
        conn.close()
        
        
    def create_blog(self):
        return self.app.post("/setup", data=dict(
            name="My Test Blog",
            fullname="Jamal Aw Yonis",
            email="jamaalmohammad123@gmail.com",
            username="awyoonisj",
            possword='test',
            confirm= 'test'
            ), follow_redirects=True)
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username, password=password), follow_redirects=True)
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
        
    def test_create_blog(self):
        rv= self.create_blog()
        print(rv.data)
        assert "Blog created" in str(rv.data)
        
    def test_login_logout(self):
        self.create_blog()
        rv= self.login("awyoonisj", 'jamal')
        
        assert "User awyoonisj logged in " in str(rv.data)
        
        
        
        
        
if __name__ == "__main__":
    unittest.main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        