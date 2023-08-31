import sqlite3


def insert_user(telegram_id, full_name, age, contact, address, reason):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name, age, contact, address, reason)
    VALUES (?,?,?,?,?,?)
    ''', (telegram_id, full_name, age, contact, address, reason))

    database.commit()
    database.close()


def get_all_users_ids():
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT telegram_id FROM users
    """)
    users_ids = cursor.fetchall()
    database.close()
    users = []
    for user in users_ids:
        users.append(user[0])
    return users


def get_user_data(telegram_id):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users
    WHERE telegram_id = ?
    ''', (telegram_id,))
    user = cursor.fetchone()
    database.close()
    return user

