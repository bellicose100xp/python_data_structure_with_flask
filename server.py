from flask import Flask, request, jsonify
from sqlite3 import Connection as SQLite3Connection

# ORM (Object Relational Mapper) allow us to interact with SQL database in Object Oriented way. only needed for the foreign key constaints code below
from sqlalchemy import event
from sqlalchemy.engine import Engine

# A wrapper to sqlalchemy that makes it more compatible with flask applications. This is what will be used in the flask application.
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import random

# custom imports
import linked_list
import hash_table
import binary_search_tree
import custom_queue
import stacks

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0  # flask_sqlalchemy generates an error if it's not set. Setting it to 0 to suppress this warning.

# configure sqlite3 to enforce foreign key constraints


@event.listens_for(Engine, 'connect')
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        cursor.close()


# create an instace of our app
db = SQLAlchemy(app)

now = datetime.now()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    posts = db.relationship('BlogPost', cascade='all, delete')  # this means delete any related blogpost when the user is deleted


class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# routes


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(  # create an instace of the class User
        name=data['name'],
        email=data['email'],
        address=data['address'],
        phone=data['phone'],
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200


@app.route('/user/descending_id', methods=['GET'])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone
        })

    return jsonify(all_users_ll.to_array()), 200


@app.route('/user/ascending_id', methods=['GET'])
def get_all_users_ascending():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone
        })

    return jsonify(all_users_ll.to_array()), 200


@app.route('/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone
        })

    user = all_users_ll.get_user_by_id(user_id)

    return jsonify(user), 200
    # return jsonify(all_users_ll.to_array()), 200


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return jsonify(f"user_id: {user_id} successfully deleted"), 200


@app.route('/blog_post/<user_id>', methods=['POST'])
def create_blog_post(user_id):
    data = request.get_json()  # it's the data that's supplied with the post request

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": f"user_id: {user_id} does not exist!"}), 400

    ht = hash_table.HashTable(10)
    ht.add_key_value('title', data['title'])
    ht.add_key_value('body', data['body'])
    ht.add_key_value('date', now)
    ht.add_key_value('user_id', user_id)

    # ht.print_table()

    new_blog_post = BlogPost(
        title=ht.get_value('title'),
        body=ht.get_value('body'),
        date=ht.get_value('date'),
        user_id=ht.get_value('user_id')
    )

    db.session.add(new_blog_post)
    db.session.commit()

    return jsonify("Blog Post Successfully Created"), 200


@app.route('/blog_post', methods=['GET'])
def get_all_blog_posts(user_id):
    pass


@app.route('/blog_post/numeric_body', methods=['GET'])
def get_numeric_bodies():
    blog_posts = BlogPost.query.all()

    q = custom_queue.Queue()
    for post in blog_posts:
        q.enqueue(post)
    
    return_list = []

    for _ in range(len(blog_posts)):
        post =  q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_id": post.data.user_id
        })
    
    return jsonify(return_list), 200



@app.route('/blog_post/<blog_post_id>', methods=['GET'])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'user_id': post.user_id
        })
    
    post = bst.search(blog_post_id)

    if not post:
        return jsonify('post not found')

    return jsonify(post), 200

@app.route('/blog_post/delete_last_10', methods=['DELETE'])
def delete_last_10():
    blog_posts = BlogPost.query.all()
    s = stacks.Stack()
    for post in blog_posts:
        s.push(post)
    
    for _ in range(10):
        post_to_delete = s.pop()
        # print(f'{post_to_delete.data}')
        db.session.delete(post_to_delete.data)
        db.session.commit()

    return jsonify('Last 10 posts deleted successfully'), 200

if __name__ == '__main__':
    app.run(debug=True)
