import sqlite3
from flask import Flask, render_template, request, redirect, session, flash, url_for
app = Flask(__name__)
app.debug = True

app.secret_key = "abcdef" 


con=sqlite3.connect('users.db')
cur=con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL)''')


con.commit()
con.close()


conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        due_date DATE,
        status TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con=sqlite3.connect('users.db')

        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))

        user = cursor.fetchone()
        if user:
            flash('Username already taken', 'error')
            con.close()
            return redirect(url_for('register'))

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        con.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

     
     return render_template('register.html')




    






@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match
        con=sqlite3.connect('users.db')

        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
         
        con.close()

        if user:
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')
 

@app.route('/home')
def home():
    # Check if user is logged in (authenticated)
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    

    flash('Please log in to access the homepage', 'error')
    return redirect(url_for('login'))




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




@app.route('/create', methods=['POST'])
def create():
     if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        duedate = request.form['duedate']
        status = request.form['status']


        con=sqlite3.connect('users.db')

        cursor = con.cursor()
        cursor.execute('INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)',
                   (title, desc, duedate, status))
        con.commit()
 
        con.close()

        return redirect(url_for('home'))

     
     return render_template('home.html')

@app.route('/ret', methods=['POST'])
def ret():
    taskid = request.form['taskid']
    con=sqlite3.connect('users.db')

    cursor = con.cursor()
    cursor.execute('SELECT * FROM tasks WHERE ID=?',
                   (taskid,))
    task=cursor.fetchone()
    con.close()
    

        #return redirect(url_for('home'))

    return render_template('home.html',task=task)
    


@app.route('/update', methods=['POST'])
def update():
    if 'username' in session:
        task_id = request.form['taskid']
        title = request.form['title']
        desc = request.form['desc']
        duedate = request.form['duedate']
        status = request.form['status']

        con=sqlite3.connect('users.db')

        cursor = con.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()

        if task:
            update_values = []
            update_params = []

            if title:
                update_values.append("title = ?")
                update_params.append(title)
            if desc:
                update_values.append("description = ?")
                update_params.append(desc)
            if duedate:
                update_values.append("due_date = ?")
                update_params.append(duedate)
            if status:
                update_values.append("status = ?")
                update_params.append(status)

            if update_values:
                update_values_str = ', '.join(update_values)
                update_params.append(task_id)

                update_query = f"UPDATE tasks SET {update_values_str} WHERE id = ?"
                cursor.execute(update_query, update_params)
                con.commit()
                con.close()

                
            

         

    return redirect('/home.html')






@app.route('/del', methods=['POST'])
def dele():

    taskid = request.form['taskid']
    con=sqlite3.connect('users.db')

    cursor = con.cursor()
    cursor.execute('DELETE FROM tasks WHERE ID=?',
                   (taskid,))
    con.commit()
    con.close()
    

        #return redirect(url_for('home'))

    return render_template('home.html')
'''
@app.route('/list',methods=['POST'])
def list_tasks():
    orderby= request.form['orderby']


    con = sqlite3.connect('users.db')
    cursor = con.cursor()

        # Retrieve all tasks in ascending order
    cursor.execute("SELECT TITLE FROM tasks ORDER BY ? ASC",(orderby,))
    tasks = cursor.fetchall()

    con.close()

    return render_template('home.html',tasks=tasks)
'''
 










if __name__ == '__main__':
    app.run()