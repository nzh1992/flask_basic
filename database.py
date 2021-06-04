# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2021/5/30
Last Modified: 2021/5/30
Description: 
"""
from app import db
from sqlalchemy.schema import CreateTable


class Note(db.Model):
    __tablename__ = "tbl_note"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Note id={}, body={}>".format(self.id, self.body)


class User(db.Model):
    __tablename__ = "tbl_sys_user"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(length=50))
    age = db.Column(db.Integer)

    def __repr__(self):
        return "<Note id={}, name={}, age={}>".format(self.id, self.name, self.age)


class Author(db.Model):
    __tablename__ = "tbl_author"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=70), unique=True)
    phone = db.Column(db.String(length=20))

    articles = db.relationship('Article')


class Article(db.Model):
    __tablename__ = "tbl_article"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('tbl_author.id'))
    title = db.Column(db.String(length=70), unique=True)
    body = db.Column(db.Text)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    body = db.Column(db.Text)

    comments = db.relationship('Comment', back_populates='post', cascade='save-update, merge, delete')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')


class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)


def show_create_table_sql(model_cls):
    sql_text = CreateTable(model_cls.__table__)
    print(sql_text)


if __name__ == '__main__':
    # db.create_all(extend_existing=True)
    db.drop_all()

    # show_create_table_sql(User)
