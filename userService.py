import sqlite3

class UserService:
    
    # def __init__(self, database='database.db'):
    #     self.conn = sqlite3.connect(database)
    #     self.cursor = self.conn.cursor()
    
    def get_all_users(self):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        users = cursor.execute("SELECT * FROM users")
        users = users.fetchall()
        con.close()
        return users

    def get_user(self, user_id):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        user = cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = user.fetchone()
        con.close()
        return user
    
    def get_user_by_username(self, username):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        if user_row:
            columns = [column[0] for column in cursor.description]
            user_dict = dict(zip(columns, user_row))
            return user_dict
        con.close()
        return None

    def get_user_by_email(self, email):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = user.fetchone()
        con.close()
        return user    
    
    def create_user(self, user):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute("""
                       INSERT INTO users (username, name, email, password, phone, state, city, country, language, birthdate, occupation, interest)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, (user["username"], user["name"], user["email"], user["password"], user["phone"], user["city"], user["state"], user["country"], user["language"], user['birthdate'], user["occupation"], user["interest"]))
        con.commit()
        con.close()
    
    def update_user(self, user_id, user):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute(f"""
                       UPDATE users 
                       SET username = ?, name = ?, email = ?, password = ?, phone = ?, state = ?, city = ?, country = ?, language = ?, birthdate = ?, occupation = ?, interest = ?
                          WHERE id = {user_id}
                       """, (user["username"], user["name"], user["email"], user["password"], user["phone"], user["state"], user["city"], user["country"], user["language"], user['birthdate'], user["occupation"], user["interest"]))
        con.commit()
        con.close()
    
    def record_search_history(self, user_id, query, language, period_start, period_end):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute('''
            INSERT INTO search_history (user_id, query, language, period_start, period_end)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, query, language, period_start, period_end))
        con.commit()
        con.close()
        
    def get_search_history(self, user_id):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        cursor.execute('''
                       SELECT query, language, period_start, period_end, COUNT(*) AS frequency
                       FROM search_history 
                       WHERE user_id = ?
                       GROUP BY query, language, period_start, period_end
                          ORDER BY frequency DESC
                          LIMIT 5
                       ''', (user_id,))
        search_history = cursor.fetchall()
        con.close()
        print(search_history)
        return search_history
    
    def execute(self, func, *args):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        func(cursor, *args)
        con.commit()
        con.close()