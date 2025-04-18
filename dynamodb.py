import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
table = dynamodb.Table('Responses')

def add_dbuser(first_name, username, genre):
    response = table.get_item(Key={'username': username})
    name = response.get('Item')
    
    if name:
        return False  # User already exists
    else:
        table.put_item(Item={
            'username': username,
            'First Name': first_name,
            'Genre': genre
        })
        return True
    
def delete_dbuser(username):
    response = table.get_item(Key={'username': username})
    print("GET response:", response)  # Debug line
    user = response.get('Item')

    if not user:
        return False
    else:
        table.delete_item(Key={'username': username})
        print("Deleted:", username)  
        return True
    
def update_dbuser(username, first_name, genre):
    # Check if the user exists
    response = table.get_item(Key={'username': username})
    user = response.get('Item')

    if not user:
        return False  # User not found
    else:
        # Update the user details
        table.update_item(
            Key={'username': username},
            UpdateExpression="set #first_name = :first_name, #genre = :genre",
            ExpressionAttributeNames={
                '#first_name': 'First Name',
                '#genre': 'Genre'
            },
            ExpressionAttributeValues={
                ':first_name': first_name,
                ':genre': genre
            }
        )
        return True
    
def get_all_users():
    response = table.scan()  # Scans all users in the table (be mindful of scan cost)
    users = response.get('Items', [])
    return users

# e.g., in db.py or flaskapp.py
import mysql.connector
import creds

def get_movies_by_genre(genre):
    db_connection = mysql.connector.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        database=creds.db
    )

    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT movie.title FROM movie JOIN genre WHERE genre_name = %s"
    cursor.execute(query, (genre,))
    movies = cursor.fetchall()

    cursor.close()
    db_connection.close()

    return movies


