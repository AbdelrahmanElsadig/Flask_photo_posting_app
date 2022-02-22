from flask import jsonify, session,request
from flask_restful import Api,Resource
from main.database import db
from main import app
import os
import uuid
import psycopg2.extras
api = Api(app)
POST_PATH_DB = '..\static\post_images'
POST_PATH = '.\main\static\post_images'
USER_PATH = '.\main\static\profile_pictures'
USER_PATH_DB = '..\static\profile_pictures'
ALLOWED_IMG_EXTENSIONS = ['GIF','JPEG','JPG','PNG']
def img_check(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.',1)[1]
    if ext.upper() in ALLOWED_IMG_EXTENSIONS:
        return ext
    return False
    
class SignUp(Resource):
    def post(self): 
        img_path = ''
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        username = request.form['username']
        user_password = request.form['user_password']
        email = request.form['email']
        if not email or not username or not user_password:
            return {'msg': 'Do not leave any text field empty'}  
        cur.execute(f'''SELECT username FROM users WHERE username = '{username}' ''')    
        res = cur.fetchone()
        print(res)
        if res:
            return {'msg': 'Account Already exists'}  
            
        session['username'] = username
        session['user_password'] = user_password
        session['email'] = email
        if request.files:
            pfp = request.files['pfp']
            ext = img_check(pfp.filename)
            if ext:
                id = str(uuid.uuid4())
                img_path = os.path.join(USER_PATH, id + '.' + ext)
                pfp.save(img_path)
                img_path = os.path.join(USER_PATH_DB,id + '.' + ext)
        if img_path:       
            cur.execute(f'''INSERT INTO users (username,user_password,email,pfp)
                           values(
                                  '{username}','{user_password}','{email}','{img_path}'
                               )''')
            db.commit()
            cur.execute(f'''SELECT user_id FROM users 
                        WHERE username = '{username}' ''')
            res = cur.fetchone()
            session['user_id'] = res['user_id']
            session['pfp'] = img_path
            return {'username':username,'user_password':user_password,'email':email,'img_path':img_path}
        else: 
            cur.execute(f'''INSERT INTO users (username,user_password,email)
                           values(
                                  '{username}','{user_password}','{email}'
                               )''')
            db.commit()
            cur.execute(f'''SELECT user_id FROM users 
                        WHERE username = '{username}' ''')
            res = cur.fetchone()
            session['user_id'] = res['user_id']
            return {'username':username,'user_password':user_password,'email':email}
                
api.add_resource(SignUp,'/signup')


class Log(Resource):
    def post(self):
        print('started')
        username = request.form['username']
        user_password = request.form['password']
        email = request.form['email']
        if not username or not user_password or not email:
            return {'msg': 'Leave no text field empty!'}
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'''SELECT * FROM users
                    WHERE username = '{username}' AND 
                    user_password = '{user_password}' AND
                    email = '{email}' ''')
        res = cur.fetchone()
        if res:
            session['user_id'] = res['user_id']
            session['username'] = username
            session['user_password'] = user_password
            session['email'] = email
            if 'pfp' in res:
                pfp = res['pfp']
                session['pfp'] = pfp
                return {'username': username,'pfp':pfp}
            return {'username':username}
        else:
            return {'msg': 'Invalid username, password or email'}
api.add_resource(Log,'/log')

class post_creation(Resource):
    def get(self):
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('''SELECT username, pfp, post_date, caption,post_img,
                    COALESCE(like_num,0) AS likes,posts.post_id
                    FROM posts 
                    JOIN users USING(user_id)
                    LEFT JOIN (
                        SELECT COALESCE(SUM(is_like) OVER (PARTITION BY post_id),0) as like_num, post_id, user_id
                        FROM likes
                    ) AS temp
                    ON posts.post_id = temp.post_id AND users.user_id = temp.user_id
                    ORDER BY post_date DESC''')
        res = cur.fetchall()
        response = jsonify(res)
        return response
    
    
    def post(self):
        post_image = request.files['post-image']
        caption = request.form['caption']
        if post_image.filename == '' or not caption:
            return {'msg': 'Do not leave any field empty!'}
        ext = img_check(post_image.filename)
        if not ext:
            return {'msg': 'Invalid image file!'}
        try:
            id = str(uuid.uuid4())
            path = os.path.join(POST_PATH, id + '.' + ext)
            post_image.save(path)
            path = os.path.join(POST_PATH_DB,id + '.' + ext)
        except:
            return {'msg': 'Image saving is the problem'}
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        user_id = session['user_id']
        try:
            cur.execute(f'''INSERT INTO posts (caption,post_img,user_id)
                        VALUES ('{caption}', '{path}', '{user_id}')''')
            db.commit()
        except:
            return {'msg': 'Query did not run correctly'}
        
        print({'caption': caption,'img_path':path,'user_id':user_id})
        return {'caption': caption,'img_path':path,'user_id':user_id}
api.add_resource(post_creation,'/post_creation')

class post_sort(Resource):
    def get(self):
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('''SELECT username, pfp, post_date, caption,post_img,
                    COALESCE(like_num,0) AS likes,posts.post_id
                    FROM posts 
                    JOIN users USING(user_id)
                    LEFT JOIN (
                        SELECT COALESCE(SUM(is_like) OVER (PARTITION BY post_id),0) as like_num, post_id, user_id
                        FROM likes
                    ) AS temp
                    ON posts.post_id = temp.post_id AND users.user_id = temp.user_id
                    ORDER BY likes DESC''')
        res = cur.fetchall()
        response = jsonify(res)
        return response
api.add_resource(post_sort,'/likes_sort')

class My_Posts(Resource):
    def get(self):
        username = session['username']
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'''SELECT username, pfp, post_date, caption,post_img,
                    COALESCE(like_num,0) AS likes,posts.post_id
                    FROM posts 
                    JOIN users USING(user_id)
                    LEFT JOIN (
                        SELECT COALESCE(SUM(is_like) OVER (PARTITION BY post_id),0) as like_num, post_id, user_id
                        FROM likes
                    ) AS temp
                    ON posts.post_id = temp.post_id AND users.user_id = temp.user_id
                    WHERE username = '{username}'
                    ORDER BY post_date DESC''')
        res = cur.fetchall()
        response = jsonify(res)
        return response
api.add_resource(My_Posts,'/my_posts')

class Like(Resource):
    def post(self):
        post_id = request.get_json(force=True)
        user_id = session['user_id']
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'''INSERT INTO likes (user_id,post_id,is_like)
                    VALUES ('{user_id}', '{post_id['post_id']}', 1); ''')
        db.commit()
        return {'msg': 'success'}
    def get(self):
        user_id = session['user_id']
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'''SELECT post_id FROM likes
                    WHERE user_id = '{user_id}' ''')
        res = cur.fetchall()
        print(res)
        return res
api.add_resource(Like,'/likes')

class Edit(Resource):
    def post(self):
        path = ''
        old_username = session['username']
        new_username = request.form['username']
        print(request.files['pfp'].filename)
        if new_username == '' and request.files['pfp'].filename == '':
            return {'msg': 'Do not leave both fields empty'}
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'''SELECT username FROM users
                    WHERE username = '{new_username}' ''')
        res = cur.fetchone()
        if res:
            return {'msg': 'Username Taken'}
        if new_username != '':
            cur.execute(f'''UPDATE users 
                        SET username = '{new_username}'
                        WHERE username = '{old_username}' ''')
            session['username'] = new_username
            db.commit()
        else:
            new_username = old_username
        img_path = ''
        pfp = None
        if request.files:
            img_path = str(uuid.uuid4())
            pfp = request.files['pfp']
            ext = img_check(pfp.filename)
            if ext:
                pfp.save(os.path.join(USER_PATH,img_path + '.' + ext))
                cur.execute(f'''SELECT pfp FROM users
                            WHERE username = '{new_username}' ''')
                res = cur.fetchone()
                if res:
                    os.remove('.\main' + res['pfp'][2:])
                path = os.path.join(USER_PATH_DB, img_path + '.' + ext)
                cur.execute(f'''UPDATE users 
                            SET pfp = '{path}' 
                            WHERE username = '{new_username}' ''')
                session['pfp'] = path
                db.commit()      
        return {'new_username': new_username,'img_path': path}
    
    
api.add_resource(Edit,'/edit')
