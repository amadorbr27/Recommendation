import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        
    def get_user(self, user_id):
        user = self.cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = user.fetchone()
        return user
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(100) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(30) NOT NULL,
                phone VARCHAR(11) NOT NULL,
                state VARCHAR(30) NOT NULL,
                city VARCHAR(50) NOT NULL,
                country VARCHAR(50) NOT NULL,
                language VARCHAR(50) NOT NULL,
                birthdate DATE NOT NULL,
                occupation VARCHAR(30) NOT NULL,
                interest VARCHAR(30) NOT NULL);
        """)
                
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                search_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query VARCHAR(50) NOT NULL,
                language VARCHAR(30) NOT NULL,
                period_start INTEGER,
                period_end INTEGER,
                article_title TEXT,
                article_link TEXT,
                article_description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,               
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.connection.commit()
        
    def close_connection(self):
        self.connection.close()