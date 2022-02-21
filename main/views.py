from flask import render_template, request, redirect
from main import app
from main.api import session
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/posts/my_posts')
@app.route('/posts/likes')
@app.route('/posts/')
def posts():
    if not session.get('username',False):
        return redirect('/login')
    return render_template('posts.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if session.get('username',False):
        return redirect('/posts')
    return render_template('login.html')

@app.route('/register/',methods=['POST','GET'])
def register():
    if session.get('username',False):
        return redirect('/posts')
    return render_template('register.html')

@app.route('/create_post/',methods=['GET','POST'])
def send_post():
    if 'username' not in session:
        return redirect('/login')
    return render_template('create_post.html')

@app.route('/edit_profile/',methods=['POST','GET'])
def edit_profile_content():
    if 'username' not in session:
        return redirect('/login')
    return render_template('edit_profile.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('user_password',None)
    session.pop('user_id',None)
    session.pop('email',None)
    if 'pfp' in session:
        session.pop('pfp',None)
    return redirect('/login')