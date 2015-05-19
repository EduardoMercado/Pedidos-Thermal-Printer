#!/usr/bin/python


from __future__ import print_function
import HTMLParser
from unidecode import unidecode
from Adafruit_Thermal import *
from pymongo import MongoClient
from time import sleep, time
import urllib  # Python URL functions
import urllib2  # Python URL functions

# Other globals.  You probably won't need to change these. -----------------

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
agent = 'Gutenbird v1.0'
mongosite = 'mongodb://'


# Mainline
def main():
    # print ('inicia conneccion')
    connection = MongoClient(mongosite)

    # print (connection)
    db = connection.pedidos
    pedidosDB = db.pedidos
    clientesDB = db.direcciones
    logDB = db.log

    # try:
    pedidos = pedidosDB.find({'estatus': 'Enviado a tienda'})
    # except:

    for pedido in pedidos:
        # print(pedido)
        idCliente = pedido['cliente'][0]
        # print(idCliente)
        cliente = clientesDB.find_one({'owner': idCliente})

        printer.print('{:<32}'.format(cliente['nombre']))

        printer.print(' ' + '{:<31}'.format(cliente['telefono']))
        printer.print(' ' + '{:<31}'.format(cliente['calle']))
        printer.print(' numExt ' + '{:<24}'.format(cliente['numExt']))
        printer.print(' numInt ' + '{:<24}'.format(cliente['numInt']))
        printer.print(' Col ' + '{:<27}'.format(cliente['colonia']))

        printer.print('total ' + '{:<26}'.format(str(pedido['total'])))
        printer.print('{:<32}'.format(str(pedido['fecha'])))
        sleep(2)
        printer.print('\n')

        # Remove HTML escape sequences
        # and remap Unicode values to nearest ASCII equivalents
        printer.print('\n')

        for p, item in enumerate(pedido['pedido'], start=1):
            printer.underlineOn()
            printer.print('Producto: ')
            printer.print(str(p) + '\n')
            printer.underlineOff()
            sleep(0.4)
            if 'quien' in item.keys():
                printer.print('para: ')
                printer.print(unidecode(
                  HTMLParser.HTMLParser().unescape(item['quien'])))
                printer.print('\n')
                sleep(0.3)
            if 'nombre' in item.keys():
                printer.print('producto: ')
                printer.print(unidecode(
                  HTMLParser.HTMLParser().unescape(item['nombre'])))
                printer.print('\n')
                sleep(0.3)
            if 'pan' in item.keys():
                printer.print('pan: ')
                printer.print(item['pan'])
                printer.print('\n')
                sleep(0.3)
            if 'tamanio' in item.keys():
                printer.print('tamanio o sabor: ')
                printer.print(item['tamanio'])
                printer.print('\n')
                sleep(0.3)
            if 'queso' in item.keys():
                printer.print('Queso: ')
                printer.print(item['queso'])
                printer.print('\n')
                sleep(0.3)
            if 'tostado' in item.keys():
                printer.print(item['tostado'])
                printer.print('\n')
                sleep(0.3)
            if 'ingredientes' in item.keys():
                printer.print('inicio Ingredientes \n')
                sleep(0.3)
                for ingrediente in item['ingredientes']:
                    printer.print('  ' + unidecode(
                      HTMLParser.HTMLParser().unescape(ingrediente)))
                    printer.print('\n')
                    sleep(0.3)
                printer.print('fin ingredientes \n')
            if 'indicacion' in item.keys():
                printer.print('nota: ')
                printer.print(unidecode(
                  HTMLParser.HTMLParser().unescape(item['indicacion'])))
                printer.print('\n')
                sleep(0.6)
            printer.print('\n')
        printer.print('\n')
        sleep(0.4)
        printer.print('fin de pedido \n')
        printer.feed(3)
        pedidosDB.update(
            {'_id': pedido['_id']},
            {'$set': {'estatus': 'En tienda'}})

    # indico que estoy trabajando
    logDB.insert({'tienda': 'juriquilla', 'selloTiempo': time()})

    connection.close()
    # print('conneccion cerrada')


def enviaMensaje(pedido):
    authkey = "YourAuthKey"  # Your authentication key.

    mobiles = "9999999999"  # Multiple mobiles numbers separated by comma.

    message = "Test message"  # Your message to send.

    sender = "112233"  # Sender ID,While using route4 6 characters long.

    route = "default"  # Define route

    # Prepare you post parameters
    values = {
              'authkey': authkey,
              'mobiles': mobiles,
              'message': message,
              'sender': sender,
              'route': route
              }

    url = "http://msg91.com/sendhttp.php"  # API URL

    postdata = urllib.urlencode(values)  # URL encoding the data here.

    req = urllib2.Request(url, postdata)

    response = urllib2.urlopen(req)

    output = response.read()  # Get Response

    print(output)  # Print Response


if __name__ == '__main__':
    main()
