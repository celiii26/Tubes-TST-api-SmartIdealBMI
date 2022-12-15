import os
from flask import *
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iniAdalahSecretKey'

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


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.username == 'user' and auth.password == '1234':
        # generate token
        token = jwt.encode({'user' : auth.username, 
                            'exp' : datetime.datetime.utcnow() + 
                            datetime.timedelta(seconds=30)}, 
                            app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/protected', methods=['GET', 'POST'])
@token_required
def protected():
    if request.method == 'GET':
        session.permanent = True
        token = request.args.get('token')
        session["main"] = token
        return redirect(url_for("main"))
    else:
        if "main" in session:
            return redirect(url_for("login"))


@app.route('/main', methods=['GET', 'POST'])
def main():
    if "main" in session:
        if request.method == 'POST':
            
            

            weight = request.form['weight']
            height = request.form['height']
            height = int(height)/100
    
            #count BMI
            bmi = float(weight) / (height*height)
    
            #categorization
            if bmi <= 18.4:
                return '<h3> You are underweight. </h3>'
            elif bmi > 18.4 and bmi < 25.0:
                return '<h3> You have a normal weight </h3>'
            elif bmi >= 25.0:
                weightMin = 18.5 * height * height
                weightMax = 24.9 * height * height
                kuranginMax = int(weight) - weightMin
                kuranginMin = int(weight) - weightMax   
            return(redirect(url_for("count", min=round(kuranginMin))))
        else:
            return '''<form action="main" method="POST">
                        <h3> Body Weight (kg) </h3>
                        <input name = "weight">
                        <h3> Body Height (cm) </h3>
                        <input name = "height">
                        <input type="submit"/></form>''' 
    else:
        return redirect(url_for("login"))

@app.route("/<min>")
def count(min):
    return jsonify({'weightToLose' : f'{min}'})

@app.route("/logout")
def logout():
    session.pop("main", None)
    return '''<h3> Logged Out <h3>
            <a href="login"><button> Login </button></a>'''

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
