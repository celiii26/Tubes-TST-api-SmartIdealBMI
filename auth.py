from flask import *
import jwt
import datetime
from functools import wraps
import psycopg2

#pip install jwt
#pip install pyjwt
#pip install Flask-JWT

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iniAdalahSecretKey'

DB_HOST = "localhost"
DB_NAME = "TST"
DB_USER = "postgres"
DB_PASS = "postgres"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403
        
        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    cur = conn.cursor()
    read = "SELECT * FROM bmi"
    cur.execute(read) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('showDB.html', list_users = list_users)

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.username == 'hello' and auth.password == 'pass':
        # generate token
        token = jwt.encode({'user' : auth.username, 
                            'exp' : datetime.datetime.utcnow() + 
                            datetime.timedelta(seconds=30)}, 
                            app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)