import sys
import mariadb
import api


try: 
    conn = mariadb.connect(
    user='oskar',
    password='Epicgamer1',
    database='stock',
    port=5000
    )
    conn.autocommit = True
except mariadb.Error as ex:
    print("Error: {}".format(ex))
    sys.exit(1)
cur = conn.cursor()


def SymbolLiFix(Li = []):
    Lli = []
    for x in range(len(Li)):
        Lli.append(Li[x][0])
    return Lli

def GetUser(p_name, cur):
    try:
        cur.execute('select u.id, u.name, u.symbol, s.curPrice, s.percent, u.orgPrice from users u inner join stock s on u.symbol = s.symbol where u.name = "{}";'.format(p_name))
        return cur.fetchall()
    except mariadb.Error as err:
        print(err)
        return

def GetStock(p_stock, cur):
    try:
        cur.execute('select symbol, curPrice, percent, monPrice, monPercent from stock where symbol="{}"'.format(p_stock))
        return cur.fetchall()
    except mariadb.Error as err:
        print(err)
        return

def GetAllStock(cur):
    try:
        cur.execute('select symbol from stock;');
        return cur.fetchall()
    except mariadb.Error as err:
        print(err)
        return

def UpdateStock(p_stock, p_curPrice, p_percent, cur):
    try:
        cur.execute('update stock set curPrice={c} where symbol="{s}";'.format(c=p_curPrice, s=p_stock))
        cur.execute('update stock set percent={c} where symbol="{s}";'.format(c=p_percent, s=p_stock))
        return #cur.fetchall()
    except mariadb.Error as err:
        print(err)
        return

def AddPlayer(p_name, p_invest, p_orgPrice, cur):
    try:
        cur.execute('insert into users (name, symbol, orgPrice) values ("{u}", "{i}", {o});'.format(u=p_name.lower(),i=p_invest.upper(),o=p_orgPrice))
        return #cur.fetchall()
    except mariadb.Error as err:
        print(err)
        return

def AddStock(p_symbol, cur):
    try:
        cur.execute('insert into stock (symbol) values ("{}");'.format(p_symbol))
        return
    except mariadb.Error as err:
        print(err)
        return

def GetTopPlayers(p_limit, cur):
    try:
        cur.execute('select u.name, u.symbol, s.curPrice, s.percent from users u inner join stock s on u.symbol = s.symbol order by s.percent desc limit {};'.format(p_limit))
        return cur.fetchall()
    except mariadb.Error as err:
        print(err)
        return

conn.close()


