#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Carga Sales Journals Meteor"""
 
__appname__ = "Carga Sales Journals"
__author__  = "Eduardo Mercado (ed/gutmer)"
__version__ = "0.0pre0"
__license__ = "GNU GPL 3.0 or later"
 


# import modules used here -- sys is a very standard one
import sys
from pymongo import MongoClient


# Gather our code in a main() function
def main():
    print 'Sistema de carga de info nomina'
    print 'No Cerrar esta ventana'
    # Command line args are in sys.argv[1], sys.argv[2] ...
    # sys.argv[0] is the script name itself and can be ignored
    mongosite = 'mongodb://Eduardo:XimEdu05@dharma.mongohq.com:10051/Facturas'   
    # el de pruebas 'mongodb://store40798:LaPincheTienda1@dharma.mongohq.com:10051/Facturas'
    
    print ('inicia conneccion')
    
    connection = MongoClient(mongosite)
    
    print (connection)
    db = connection.Facturas
    infoNomina = db.infoNomina
    
    #try:
    datos = infoNomina.find_one()
    #except:
    #print('* error al insertar carga inicial *')
    

    connection.close()
    print('conneccion cerrada')
    print (datos)   

if __name__ == '__main__':
    main()
