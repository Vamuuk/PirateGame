import sqlite3


def create_tables():
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_data 
                 (username TEXT, coins INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_achievements 
                 (username TEXT, achievement TEXT)''')
    conn.commit()
    conn.close()


def get_user_coins(username):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("SELECT coins FROM user_data WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0


def save_coins(username, coins):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()

    c.execute("SELECT * FROM user_data WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        c.execute("UPDATE user_data SET coins = ? WHERE username = ?", (coins, username))
    else:
        c.execute("INSERT INTO user_data (username, coins) VALUES (?, ?)", (username, coins))

    conn.commit()
    conn.close()


def get_top_users(limit=5):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("SELECT username, coins FROM user_data ORDER BY coins DESC LIMIT ?", (limit,))
    users = c.fetchall()
    conn.close()
    return users


def save_achievement(username, achievement):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_achievements (username, achievement) VALUES (?, ?)", (username, achievement))
    conn.commit()
    conn.close()


def get_user_achievements(username):
    conn = sqlite3.connect('game_data.db')
    c = conn.cursor()
    c.execute("SELECT achievement FROM user_achievements WHERE username = ?", (username,))
    achievements = [row[0] for row in c.fetchall()]
    conn.close()
    return achievements


create_tables()
