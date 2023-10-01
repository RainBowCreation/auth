import sys
import itertools
import yaml
import mysql.connector as sql
import mariadb

def mysql(data:list):
    i = itertools.count(1)
    conn = sql.connect(
        user=data[next(i)],
        password=data[next(i)],
        host=data[next(i)],
        port=data[next(i)],
        database=data[next(i)]
    )
    return conn

def mariadb(data:list):
    i = itertools.count(1)
    conn = sql.connect(
        user=data[next(i)],
        password=data[next(i)],
        host=data[next(i)],
        port=data[next(i)],
        database=data[next(i)]
    )
    return conn
def dinput():
    auth = input("Enter Auth/database type [mysql, mariadb] (Skip will use noauth):").lower()
    for i in range(10):
        if (auth == ''):
            auth = 'noauth'
            break
        elif (auth == 'sql' or auth == 'mysql'):
            auth = 'mysql'
            break
        elif (auth == 'maria' or auth == 'mariadb'):
            auth = 'mariadb'
            break
        else:
            print("Auth not support or typo")
    user = input("username (Skip will use root):")
    if (user == ''):
        user = 'root'
    password = input("password(Skip will use nopass):")
    host = input("host (Skip will use localhost):")
    if (host == ''):
        host = 'localhost'
    port = input("port (Skip will use 3306):")
    if (port == ''):
        port = 3306
    else:
        port = int(port)
    database = input('database (Skip will use default):')
    return [auth, user, password, host, port, database]

def main():
    data = dinput()
    try:
        match(data[0]):
            case('no auth'):
                #do no auth
                return
            case('mysql'):
                conn = mysql(data)
            case('mariadb'):
                conn = mariadb(data)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Get Cursor
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM ping")
    for (ping) in cur:
        if (ping[0] == 'pong'):
            print("connected")
            #do the thing 
            
main()