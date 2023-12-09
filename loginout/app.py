from flask import *
import sqlite3
app = Flask(__name__)
app.secret_key = 'hyeonchill'

@app.route('/', methods = ["POST","GET"])
def home():
    id = None
    if 'id' in session:
        id = session['id']
        print('id in sess')
    return render_template('home.html',s_id = id)

@app.route('/login', methods=["POST","GET"])
def login():
    username = request.form.get("user")
    password = request.form.get("pwd")
    if username and password:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM board WHERE user = ? AND pwd = ?;",(username,password))
        conn.commit()
        if not cur.fetchone():
            cur.close()
            return '<script>alert("invalid input!");history.go(-1);</script>'
        session['id'] = username
        cur.close()
        return redirect(url_for('home'))
    id = None
    if 'id' in session:
        id = session['id']
    return render_template('login.html',s_id=id)

@app.route('/register', methods = ["POST","GET"])
def register():
    username = request.form.get("user")
    password = request.form.get("pwd")
    if username and password:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM board WHERE user = ?;", (username, ))
        if not cur.fetchone():
            cur.execute("INSERT INTO board VALUES (?,?);",(username,password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            conn.close()
            return '<script>alert("user already exists");history.go(-1);</script>'
        
    return render_template('register.html')

@app.route('/modify',methods = ["POST","GET"])
def modify():
    oldname = request.form.get("user")
    oldpass = request.form.get("pwd")
    newname = request.form.get("newuser")
    newpass = request.form.get("newpwd")
    if 'id' in session and oldname and oldpass and newname and newpass:
        print(session['id'], oldname)
        if session['id'] != oldname:
            return '<script>alert("check your current name!");history.go(-1);history.go(-1);</script>'
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM board WHERE user = ? AND pwd = ?;", (oldname, oldpass))
        conn.commit()
        if not cur.fetchone():
            cur.close()
            return '<script>alert("check your current name and password!");history.go(-1);</script>'
        cur.execute("DELETE FROM board WHERE user = ? AND pwd = ?;", (oldname, oldpass))
        conn.commit()
        cur.execute("INSERT INTO board VALUES (?,?);",(newname,newpass))
        conn.commit()
        session['id'] = newname
        cur.close()
        return '<script>alert("modified successfully!");history.go(-1);</script>'
    id = None
    if 'id' in session:
        id = session['id']
    return render_template('modify.html',s_id = id)

@app.route('/logout', )
def logout():
    session.pop('id',None)
    return redirect(url_for('home'))

@app.route('/read')
def read():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM board;")
    rows = cur.fetchall()
    print(rows)
    conn.commit()
    conn.close()
    return render_template('view.html', posts = rows)

if __name__ == "__main__":
    '''conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE board (user TEXT, pwd TEXT);")
    conn.commit()
    conn.close()
    '''
    app.run()