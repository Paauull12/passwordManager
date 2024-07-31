import sqlite3


class DBManager:

    def __init__(self, db_name='passwords.db'):
        self.db_name = db_name
        self.create_table()

    def create_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.create_connection()

        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS passwords(
                    id integer primary key,
                    user_id integer,
                    service text not null,
                    username text not null,
                    password text not null,
                    foreign key(user_id) references user(id)
                    )
            ''')
            conn.execute('''CREATE TABLE IF NOT EXISTS master(
                    id integer primary key,
                    username text not null,
                    password_hash text not null)
            ''')

    def insertInTable(self, user_id, service, username, enc_pass):
        conn = self.create_connection()
        with conn:
            conn.execute('''
                insert into passwords(user_id, service, username, password) values (?, ?, ?, ?)
            ''', (user_id, service, username, enc_pass))

    def get_passwords(self, user_id):
        conn = self.create_connection()
        with conn:
            cursor = conn.execute('''
                select service, username, password from passwords where user_id = ?
            ''', (user_id,))
            return cursor.fetchall()

    def insert_user(self, user_name, enc_pass):
        conn = self.create_connection()
        with conn:
            conn.execute('''
                insert into master(username, password_hash) values (?, ?)
            ''', (user_name, enc_pass))

    def get_user(self, username):
        conn = self.create_connection()
        with conn:
            cursor = conn.execute('select id , password_hash from master where username = ?', (username,))
            return cursor.fetchone()
