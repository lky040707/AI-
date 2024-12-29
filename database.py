import sqlite3

def init_db():
    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()

    # 创建 users 表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT,
                  role TEXT DEFAULT 'user')''')

    # 创建 records 表
    c.execute('''CREATE TABLE IF NOT EXISTS records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, 
                  score INTEGER, 
                  date TEXT)''')

    # 创建 results 表
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, 
                  question TEXT, 
                  user_answer TEXT, 
                  correct_answer TEXT, 
                  is_correct INTEGER)''')

    conn.commit()
    conn.close()

def save_record(username, score):
    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO records (username, score, date) VALUES (?, ?, datetime('now'))",
              (username, score))
    conn.commit()
    conn.close()

def save_results(username, results):
    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()
    for result in results:
        # 如果是简答题，保存用户的错误答案
        if not result['is_correct']:
            c.execute(
                "INSERT INTO results (username, question, user_answer, correct_answer, is_correct) VALUES (?, ?, ?, ?, ?)",
                (username, result['question'], result['user_answer'], result['correct_answer'], int(result['is_correct'])))
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')",
                  (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  # 用户名已存在
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
              (username, password))
    user = c.fetchone()
    conn.close()
    return user

def create_admin():
    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'admin')",
                  ('admin', 'admin123'))
        conn.commit()
    except sqlite3.IntegrityError:  # 如果管理员已存在，忽略
        pass
    finally:
        conn.close()