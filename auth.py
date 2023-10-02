import os
import sys
import itertools
import ruamel.yaml
import mysql.connector as sql
import mariadb
from getpass import getpass

plugins = ["RainBowCreation", "Lands", "LuckPerms"]
yaml = ruamel.yaml.YAML()

def getpath(plugin):
    return "plugins/"+plugin+"/config.yml"

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
    for i in range(10):
        auth = input("Enter Auth/database type [mysql, mariadb] (Skip will use noauth):").lower()
        if (auth == ''):
            auth = 'noauth'
            return [auth]
        elif (auth == 'sql' or auth == 'mysql'):
            auth = 'mysql'
            break
        elif (auth == 'maria' or auth == 'mariadb'):
            auth = 'mariadb'
            break
        else:
            print("Auth not support or typo")
        if (i == 9):
            print("Please ckeck your database type and try again.")
            return None
    user = input("username (Skip will use root):")
    if (user == ''):
        user = 'root'
    password = getpass("password(Skip will use nopass):")
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

def config_checker():
    check = True
    for path in plugins:
        if (not os.path.exists(getpath(path))):
            print(f"{path} not exists please check that the file or run ./start to recreate the files and try again.")
            check = False
    return check

def rbccore(data):
    i = itertools.count(0)
    if (data[next(i)] != 'noauth'):
        with open(getpath(plugins[0]), "r") as f:
            config = yaml.load(f)
            config['mySQL']['enable'] = True
            config['mySQL']['username'] = data[next(i)]
            config['mySQL']['password'] = data[next(i)]
            config['mySQL']['url'] = data[next(i)]
            config['mySQL']['port'] = data[next(i)]
            config['mySQL']['database'] = data[next(i)]
        with open(getpath(plugins[0]), "w") as f:
            yaml.dump(config, f)
       
def lands(data):
    i = itertools.count(0)
    if (data[next(i)] == 'mysql'):
        with open(getpath(plugins[1]), "r") as f:
            config = yaml.load(f)
            config['database']['mysql']['enabled_20'] = True
            config['database']['mysql']['username'] = data[next(i)]
            config['database']['mysql']['password'] = data[next(i)]
            config['database']['mysql']['ip-address'] = data[next(i)]
            config['database']['mysql']['port'] = data[next(i)]
            config['database']['mysql']['database'] = data[next(i)]
        with open(getpath(plugins[1]), "w") as f:
            yaml.dump(config, f)

def luckperms(data):
    i = itertools.count(0)
    if (data[next(i)] != 'noauth'):
        with open(getpath(plugins[2]), "r") as f:
            config = yaml.load(f)
            match(data[0]):
                case('mysql'):
                    config['storage-method'] = 'MySQL'
                case('mariadb'):
                    config['storage-method'] = 'MariaDB'
            config['data']['username'] = data[next(i)]
            config['data']['password'] = data[next(i)]
            config['data']['address'] = data[next(i)]+":"+str(data[next(i)])
            config['data']['database'] = data[next(i)]
            config['data']['pool-settings']['keepalive-time'] = 60000
            config['sync-minutes'] = 1
        with open(getpath(plugins[2]), "w") as f:
            yaml.dump(config, f)

def main():
    data = dinput()
    if (data == None):
        return
    try:
        match(data[0]):
            case('noauth'):
                print("Using noauth you can start the stanalone server using ./start.sh but the server will not connected to RainBowCreationMainNet!")
                return
            case('mysql'):
                conn = mysql(data)
            case('mariadb'):
                conn = mariadb(data)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM heartbeat")
    for (ping) in cur:
        if (ping[0] == 'pong'):
            print("connected")
        else:
            print("Cant connect to auth server..")
            return
    if (not config_checker()):
        return
    rbccore(data)
    lands(data)
    luckperms(data)
    
main()