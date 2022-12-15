from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
 
DB_HOST = "localhost"
DB_NAME = "TST"
DB_USER = "postgres"
DB_PASS = "postgres"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def Index():
    cur = conn.cursor()
    read = "SELECT * FROM data_bmi"
    cur.execute(read) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)
 
@app.route('/add_bmi', methods=['POST'])
def add_bmi():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nama = request.form['nama']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        cur.execute("INSERT INTO data_bmi(nama, gender, height, weight) VALUES (%s,%s,%s,%s)", (nama, gender, height, weight))
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/edit/<nama>', methods = ['POST', 'GET'])
def get_bmi(nama):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute("SELECT * FROM data_bmi WHERE nama = '%s'" % nama)
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', data_bmi = data[0])
 
@app.route('/update/<nama>', methods=['POST'])
def update_bmi(nama):
    if request.method == 'POST':
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE data_bmi
            SET gender = '%s',
                height = %s,
                weight = %s
            WHERE nama = '%s'
        """ % (gender, height, weight, nama))
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<nama>', methods = ['POST','GET'])
def delete_bmi(nama):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute("DELETE FROM data_bmi WHERE nama = '%s'" % (nama))
    conn.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
