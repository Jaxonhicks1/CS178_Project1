import mysql.connector
import creds

def show_tables():
    try:
        conn = mysql.connector.connect(
            host=creds.host,
            user=creds.user,
            password=creds.password,
            database=creds.db
        )
        cursor = conn.cursor()
        query = "SHOW TABLES"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for row in results:
                print(row[0])
        else:
            print("No tables found in the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    show_tables()