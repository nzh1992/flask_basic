# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2021/5/17
Last Modified: 2021/5/17
Description: 
"""
import urllib

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from sqlalchemy import and_, or_
import click

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{urllib.parse.quote("Nzh199266@")}@127.0.0.1:3306/flask_basic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


@app.route('/')
@app.route('/hello')
def index():
    return '<h1>hello flask</h1>'


@app.route('/greet', defaults={'name': 'anonymous'})
@app.route('/greet/<name>')
def greet(name):
    return f'<h1>hello, {name}</h1>'


valid_colors = ['blue', 'white', 'red']


@app.route('/colors/<any(%s):color>' % str(valid_colors)[1: -1])
def three_colors(color):
    return f'<h1>{color}</h1>'


@app.cli.command()
def hello():
    click.echo("hello, flasker.")


@app.cli.command()
def init_db():
    try:
        db.create_all()
    except Exception as e:
        click.echo(f"Initailize database failed. reason: {str(e)}")
    else:
        click.echo("Initailized database successful.")


# @app.before_request
# def do_something():
#     print("do something before request.")
#
#
# @app.after_request
# def after_request(red):
#     print(f"do something before request. ")


# 数据库操作练习
from database import Note, User, Draft


@app.route('/note', methods=['POST'])
def create_note():
    request_body = request.get_json()

    try:
        new_note = Note(id=request_body.get('id'), body=request_body.get('content'))
        db.session.add(new_note)
        db.session.commit()
    except Exception as e:
        return f"create failed.{str(e)}"
    else:
        return f"create successful. id={new_note.id}"


@app.route('/notes', methods=['GET'])
def get_all_notes():
    all_notes = Note.query.all()
    all_notes_count = Note.query.count()
    return all_notes


@app.route('/note/<note_id>', methods=['GET'])
def get_note(note_id):
    # note = Note.query.get_or_404(note_id)

    # 1. 使用filter过滤
    # note = Note.query.filter(Note.id==note_id).first()

    # 1.1 LIKE
    # note = Note.query.filter(Note.id.like('%1%')).first()

    # 1.2 IN
    # note = Note.query.filter(Note.id.in_([1, 2, 3])).first()

    # 1.3 NOT IN
    # note = Note.query.filter(~Note.id.in_([1, 2, 3])).first()

    # 1.4 AND，两种写法
    # 第一种，借助sqlalchemy._and函数
    # note = Note.query.filter(and_(Note.id==note_id, Note.body.contains('this'))).first()

    # 第二种，filter中加入多个表达式，用逗号分隔
    note = Note.query.filter(Note.id==note_id, Note.body.contains('this')).first()

    # 2. 使用filter_by过滤
    # note = Note.query.filter_by(id=note_id).first()

    return note


# 给flask shell添加上下文
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Note': Note}


# 添加flask命令，初始化数据库
@app.cli.command()
@click.option('--drop', is_flag=True, help='create after drop')
def initdb(drop):
    if drop:
        click.confirm("初始化数据库，是否删除原有表？，输入y继续", abort=True)
        click.echo("Drop tables.")

    db.create_all()
    click.echo("数据库初始化，ok")


# set时间监听函数
@db.event.listens_for(Draft.body, 'set')
def increment_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1





