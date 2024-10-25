import mysql.connector
import os

DB_HOST = os.getenv("MYSQL_HOST", "mysql-db")
DB_USER = os.getenv("MYSQL_USER", "discorduser")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_NAME = os.getenv("MYSQL_DATABASE", "discorddb")

def create_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def initialize_db():
    conn = create_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS discordWarnings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            discord_id VARCHAR(255) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )
        """
        cursor.execute(create_table_query)
        print("Database initialized successfully.")
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")
    finally:
        cursor.close()
        conn.close()
