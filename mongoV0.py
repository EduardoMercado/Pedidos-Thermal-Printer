#!/usr/bin/python


from __future__ import print_function
import base64, HTMLParser, httplib, json, sys, urllib, zlib
from unidecode import unidecode
from Adafruit_Thermal import *
from pymongo import MongoClient
from time import sleep

# Other globals.  You probably won't need to change these. -----------------

printer   = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
agent     = 'Gutenbird v1.0'
mongosite = 'mongodb://pedidos:Tias08MatIgo11Rod@c736.candidate.15.mongolayer.com:10736/pedidos'


# lastID is command line value (if passed), else 1
if len(sys.argv) > 1: lastId = sys.argv[1]
else:                 lastId = '1'



# Mainline

#print ('inicia conneccion')

connection = MongoClient(mongosite)

#print (connection)
db = connection.pedidos
pedidosDB = db.pedidos
clientesDB = db.direcciones


#try:
pedidos = pedidosDB.find({'estatus':'Enviado a tienda'})
#except:


for pedido in pedidos:
  #print(pedido)
  idCliente = pedido['cliente'][0]
  #print(idCliente)	
  cliente = clientesDB.find_one({'owner':idCliente})
  
  printer.print('{:<32}'.format(cliente['nombre']))
  
  printer.print(' ' + '{:<31}'.format(cliente['telefono']))
  printer.print(' ' + '{:<31}'.format(cliente['calle']))
  printer.print('numExt ' + '{:<25}'.format(cliente['numExt']))
  printer.print('numInt ' + '{:<25}'.format(cliente['numInt']))
  printer.print('Col ' + '{:<28}'.format(cliente['colonia']))

  printer.print('total ' + '{:<26}'.format(str(pedido['total'])))
  printer.print('{:<32}'.format(str(pedido['fecha'])))
  sleep(1.5)
  printer.print('\n')
  
  # Remove HTML escape sequences
  # and remap Unicode values to nearest ASCII equivalents
  printer.print('\n')
  for item in pedido['pedido']:
    for detalle in item.items():
      if type(detalle[1]) is list:
        printer.print('inicio Ingredientes \n')
	sleep(0.5)
        for ingrediente in detalle[1]:
          printer.print(unidecode(
            HTMLParser.HTMLParser().unescape(ingrediente)))
          printer.print('\n')
          sleep(0.5)
        printer.print('fin ingredientes \n')  
      else:
        if type(detalle[1]) is int:
          pass
        elif detalle[0] == 'detalle':
          pass
        else:
          printer.print(detalle[0] + ': ')   
          printer.print(unidecode(
            HTMLParser.HTMLParser().unescape(detalle[1])))
          printer.print('\n')
          sleep(0.5)
      sleep(0.5)
    printer.print('\n')  
    printer.print('Nuevo Producto \n')
  printer.print('\n')
  sleep(0.5)
  printer.print('fin de pedido \n')
  printer.feed(3)
  sleep(1)
  check = pedidosDB.update({'_id': pedido['_id']}, {'$set':{'estatus': 'En tienda'}})


connection.close()
#print('conneccion cerrada')
