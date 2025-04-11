
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import creds

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
                                   

@app.route('/')
def home():
    tables = []

    try:
        conn = mysql.connector.connect(
            host=creds.host,
            user=creds.user,
            password=creds.password,
            database=creds.db
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        results = cursor.fetchall()
        tables = [row[0] for row in results]

    except mysql.connector.Error as err:
        tables = [f"Error: {err}"]

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return render_template('results.html', tables=tables)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        First_name = request.form['First_name']
        Last_Name = request.form['Last_Name'] 
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("First Name:", First_name, ":", "Last Name:", Last_Name, ":","Favorite Genre:", genre)
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')
    
@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", name, ":")
        
        flash('User deleted successfully!', 'warning')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
