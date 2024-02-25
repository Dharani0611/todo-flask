from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('todos.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS todos
             (id INTEGER PRIMARY KEY, todo TEXT)''')
conn.commit()

@app.route('/')
def index():
    c.execute('SELECT * FROM todos')
    todos = c.fetchall()
    return render_template('todo.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')
    if todo:
        c.execute('INSERT INTO todos (todo) VALUES (?)', (todo,))
        conn.commit()
    return redirect('/')
@app.route('/update/<int:id>', methods=['POST'])
def update_todo(id):
    new_todo = request.form.get('new_todo')
    if new_todo:
        c.execute('UPDATE todos SET todo = ? WHERE id = ?', (new_todo, id))
        conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_todo(id):
    c.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
