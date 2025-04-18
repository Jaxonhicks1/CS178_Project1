import boto3
from dynamodb import *
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import creds

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
table = dynamodb.Table('Responses')

@app.route('/')
def home():
    "Welcome to the movie database"

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
        first_name = request.form['First_name']
        username = request.form['Last_Name']  # assuming username is stored here
        genre = request.form['genre']

        if add_dbuser(first_name, username, genre):
            flash('User added successfully!', 'success')
        else:
            flash('Username already exists. Please choose a different one.', 'danger')

        return redirect(url_for('home'))

    return render_template('add_user.html')

    
@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        last_name = request.form['Last_Name']
        username = last_name  # Assuming username == last name in lowercase

        if delete_dbuser(username):
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found.', 'danger')
        return redirect(url_for('home'))

    return render_template('delete_user.html')

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        last_name = request.form['Last_Name']
        first_name = request.form['First_name']
        genre = request.form['genre']

        username = last_name

        if update_dbuser(username, first_name, genre):
            flash('User updated successfully!', 'success')
        else:
            flash('User not found.', 'danger')
        return redirect(url_for('home'))

    return render_template('update_user.html')

@app.route('/select-user', methods=['GET', 'POST'])
def select_user():
    if request.method == 'POST':
        selected_username = request.form['username']
        
        # Fetch user details based on the username
        response = table.get_item(Key={'username': selected_username})
        user = response.get('Item')
        
        if user:
            genre = user['Genre']  # Extract user's favorite genre
            # Now, get movies from that genre (we assume you have a list of movies or a way to fetch them)
            movies = get_movies_by_genre(genre)
            return render_template('user_movies.html', user=user, movies=movies)
        else:
            flash("User not found!", "danger")
            return redirect(url_for('select_user'))

    all_users = get_all_users()
    return render_template('select_user.html', users=all_users)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
