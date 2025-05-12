import time
import sqlite3
from flask import Flask, render_template, request
from processing import run_multiprocessing, run_single_processor
from threads import run_multithread, run_single


app = Flask(__name__)

# Database initialization
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                j INTEGER NOT NULL,
                result REAL NOT NULL,
                time_taken REAL NOT NULL,
                method TEXT NOT NULL
            )
        ''')
        conn.commit()

# Shared sum formula
def formula(start, end):
    total = 0
    for i in range(start, end + 1):
        total += 1 / (i ** 2)
    return total



# MULTIPROCESSING
def partial(start, end, q):
    # This function is now defined outside of run_multiprocessing
    result = formula(start, end)
    q.put(result)


# Save result to database
def save_result_to_db(j, result, time_taken, method):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO calculations (j, result, time_taken, method)
            VALUES (?, ?, ?, ?)
        ''', (j, result, time_taken, method))
        conn.commit()

# Get all calculations from the database
def get_all_calculations():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM calculations')
        calculations = cursor.fetchall()
    return calculations

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    time_taken = None
    j = None

    if request.method == 'POST':
        j = int(request.form['j'])
        method = request.form['method']

        if method == 'single':
            result, time_taken = run_single(j)
        elif method == 'multithread':
            result, time_taken = run_multithread(j)
        elif method == 'multiprocessing':
            result, time_taken = run_multiprocessing(j)
        elif method == 'single_processor':
            result, time_taken = run_single_processor(j)

        # Save the result to the database
        save_result_to_db(j, result, time_taken, method)

    return render_template('index.html', result=result, time_taken=time_taken)

@app.route('/output')
def output():
    calculations = get_all_calculations()
    return render_template('output.html', calculations=calculations)

if __name__ == '__main__':
    init_db()  # Initialize the database and create the table if it doesn't exist
    app.run(debug=True)
