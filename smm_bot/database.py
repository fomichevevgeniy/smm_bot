import sqlite3

database = sqlite3.connect('bot.db')
cursor = database.cursor()


def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT,
        age TEXT,
        contact TEXT,
        address TEXT,
        reason TEXT
    )
    ''')


create_users_table()
database.commit()
database.close()
