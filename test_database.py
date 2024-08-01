import sqlite3
from database import DBManager


def test_databases():
    db = DBManager("test.db")

    conn = db.create_connection()

    with conn:

        cursor = conn.cursor()

        cursor.execute('''
            select name from sqlite_master where type='table' and name='passwords';
        ''')

        result = cursor.fetchone()

    assert result is not None
    cursor.close()

    db.insert_user("marius", "oparolaputernica")

    cursor = conn.cursor()

    cursor.execute('''
        select id from master where username = "marius";
    ''')

    result1 = cursor.fetchone()
    cursor.close()

    assert result1 is not None
    print(result1[0])

    db.insertInTable(int(result1[0]), "serviciu_da", "username", "parolatare2")

    cursor = conn.cursor()

    cursor.execute('''
        select service from passwords where user_id = ?
    ''', (result1[0],))

    final_rez = cursor.fetchone()

    assert final_rez[0] == "serviciu_da"

