# -*-coding:utf-8 -*-
import httplib
import json
import pygsheets
import time


URL = 'api.coinmarketcap.com' #https://api.coinmarketcap.com/v1/ticker/
gc = pygsheets.authorize() # first authorize
gc = pygsheets.authorize(outh_file='client_secret.json') #  you already have a file with tokens
# Open spreadsheet and then workseet,client_secret.json
sh = gc.open('TestSheet')
wks = sh.sheet1
conn = httplib.HTTPSConnection(URL)


def get_response(conn, url='/v1/ticker/'):
    """
    get response by https connection, return json data
    :param url: url to request
    :param conn: https connection, share a connection
    :return: the response
    """

    data = ''
    status = 0
    try:
        conn.request("GET", url)
        res = conn.getresponse()
        status = res.status
        if status == 200:
            data = res.read()
        else:
            print 'status error url:', url
    except Exception as e:
        print 'url:%s, status:%s, exception:%s' % ( url, status, repr(e))
    return data

def get_price():
    data = get_response(conn)
    data_json = json.loads(data)
    symbols = {'USDT':0.0, 'BTC':0.0,'ETH':0.0, 'BLZ':0.0,'ONT':0.0, 'ZIL':0.0,'ACAT':0.0,
               'EDT':0.0,'BNB':0.0,'KCS':0.0,'NEO':0.0}
    for symbol_dic in data_json:
        symbol = symbol_dic['symbol']
        price = float(symbol_dic['price_usd'])
        if symbols.has_key(symbol):
            symbols[symbol] = price
    for k,v in symbols.items():
        if v < 0.0000001:
            print k, ' not exist'
        print k,v
    return symbols


def update_sheet(wks, symbol_price_dic):
    symbol_names =  list(range(2,25)) # Col A
    # symbol_prices = list(range(2,14))  # col D
    for i in symbol_names:
        name = wks.cell('A'+str(i)).value
        price = wks.cell('D'+str(i)).value

        if name == '':
            continue
        print 'before update, name:{0}, price:{1}'.format(name.encode('utf-8'), price.encode('utf-8'))
        print type(price)
        if symbol_price_dic.has_key(name):
            if price > 0.000001:
                print 'update, name:{0}, price:{1}'.format(name, symbol_price_dic[name])
                wks.update_cell('D'+str(i), '$'+str(symbol_price_dic[name]))
                # wks.cell('D'+str(i)).set_text_format('bold', True).value = ('$'+str(symbol_price_dic[name])).decode('utf-8')
            else:
                print 'not exist, name:{0}, price:{1}'.format(name, symbol_price_dic[name])
                wks.update_cell('D' + str(i), '$' + str(symbol_price_dic[name]))
                # wks.cell('D' + str(i)).set_text_format('bold', True).value = '$'+str(symbol_price_dic[name])


if __name__ == '__main__':
    while True:
        print '********* update *********'
        symbol_price_dic = get_price()
        update_sheet(wks, symbol_price_dic)
        time.sleep(60)


