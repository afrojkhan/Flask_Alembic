from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask import abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY']='B4q4dKDT5nhBdKM8JIrB'  
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }  


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username or email already exists'}), 400
    

  

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    try:
        db.session.commit()
        return jsonify(user.serialize()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username or email already exists'}), 400
    

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Could not delete the user'}), 500



class Post(db.Model):
    __tablename__="post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='posts')


    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        } 



@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data.get('user_id')  
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_post = Post(title=data['title'], content=data['content'], user=user)
    
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.serialize()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error creating the post'}), 400


    
    
    

class Comment(db.Model):
    __tablename__="comment"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='comments')

    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
        } 
    
@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    post_id = data.get('post_id')  
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'message': 'Post not found'}), 404

    new_comment = Comment(text=data['text'], post=post)

    try:
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.serialize()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error creating the comment'}), 400
    
if __name__ == "__main__":
   
    app.run(debug=True)
