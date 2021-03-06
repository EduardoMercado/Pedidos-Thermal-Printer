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
mongosite = 'mongodb://'



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
    if 'quien' in item.keys():
      printer.print('para: ')
      printer.print(unidecode(
        HTMLParser.HTMLParser().unescape(item['quien'])))
      printer.print('\n')
       sleep(0.5)
    if 'nombre' in item.keys():
      printer.print('producto: ')
      printer.print(unidecode(
        HTMLParser.HTMLParser().unescape(item['nombre'])))
      printer.print('\n')
      sleep(0.5)
    if 'pan' in item.keys():
      printer.print('pan: ')
      printer.print(item['pan'])
      printer.print('\n')
      sleep(0.5)
    if 'tamanio' in item.keys():
      printer.print('tamanio o sabor: ')
      printer.print(item['tamanio']
      printer.print('\n')
      sleep(0.5)
    if 'queso' in item.keys():
      printer.print('Queso: ')
      printer.print(item['queso'])
      printer.print('\n')
      sleep(0.5)
    if 'tostado' in item.keys():
      printer.print('tostado \n')
      sleep(0.5)
    if 'ingredientes' in item.keys():
      printer.print('inicio Ingredientes \n')
      sleep(0.5)
      for ingrediente in item['ingredientes]:
        printer.print(ingrediente)
        printer.print('\n')
        sleep(0.5)
      printer.print('fin ingredientes \n')  
    if 'indicacion' in item.keys():
      printer.print('nota: ')
      printer.print(unidecode(
        HTMLParser.HTMLParser().unescape(item['indicacion'])))
      printer.print('\n')
    printer.print('\n')  
    printer.print('Nuevo Producto \n')
    sleep(0.5)
  printer.print('\n')
  sleep(0.5)
  printer.print('fin de pedido \n')
  printer.feed(3)
  check = pedidosDB.update({'_id': pedido['_id']}, {'$set':{'estatus': 'En tienda'}})

connection.close()
#print('conneccion cerrada')
