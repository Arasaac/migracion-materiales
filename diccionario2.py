#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import mysql.connector
import MySQLdb
import pprint
import os
import magic
from bs4 import BeautifulSoup
from slugify import slugify
import pdb
import json
import codecs
import datetime
import chardet

def encode(word, encoding):
    '''
    Usa chardet para convertir a unicode
    Devuelve cadena en utf-8
    Req:
    > pip install chardet
    '''
    word2=""
    if encoding=='fixit':
        return word.decode('utf-8').encode('latin1').decode('utf-8').encode('utf-8')
    else:
        tmp = word.decode(encoding)  # unicode
        return tmp.encode('utf-8')
    # tmp.encode('utf-8')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def openReadDatabase():
    return MySQLdb.connect('127.0.0.1', 'root', 'password', 'saac')


def obtenerPalabras():
    cnx = openReadDatabase()
    cursor = cnx.cursor()
    query = ("SELECT id_palabra, palabra, definicion FROM palabras where palabra is not null")
    cursor.execute(query)
    palabras = []
    columns = ['id', 'word', 'def']
    for row in cursor:
        palabras.append(dict(zip(columns, row)))
    cursor.close()
    cnx.close()
    return palabras

def obtenerTraducciones(table):
    cnx = openReadDatabase()
    cursor = cnx.cursor()
    query = ("SELECT id_palabra, traduccion, definicion_traduccion FROM " + table + " where traduccion is not null")
    cursor.execute(query)
    palabras = []
    columns = ['id', 'word', 'def']
    for row in cursor:
        palabras.append(dict(zip(columns, row)))
    cursor.close()
    cnx.close()
    return palabras


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


idiomas = [{"id_idioma": 1,"idioma_ru": "Russian","idioma_abrev": "ru"},
            {"id_idioma": 2,"idioma_en": "Romanian","idioma_abrev": "ro"}, # fixit no va 
            {"id_idioma": 3,"idioma_en": "Arabic","idioma_abrev": "ar", "encoding1": "CP1256", "encoding2": "CP1256"}, 
            {"id_idioma": 4,"idioma_en": "Chinese","idioma_abrev": "zh"}, 
            {"id_idioma": 5,"idioma_en": "Bulgarian","idioma_abrev": "bg"}, 
            {"id_idioma": 6,"idioma_en": "Polish","idioma_abrev": "pl", "encoding2": "fixit"}, 
            {"id_idioma": 7,"idioma_en": "English","idioma_abrev": "en"}, # ni idea... el fixit no va :-( 
            {"id_idioma": 8,"idioma_en": "French","idioma_abrev": "fr", "encoding2": "fixit"}, 
            {"id_idioma": 9,"idioma_en": "Catalan","idioma_abrev": "ca", "encoding2": "fixit"}, 
            {"id_idioma": 10,"idioma_en": "Euskera","idioma_abrev": "eu"}, 
            {"id_idioma": 11,"idioma_en": "German","idioma_abrev": "de"}, 
            {"id_idioma": 12,"idioma_en": "Italian","idioma_abrev": "it"}, 
            {"id_idioma": 13,"idioma_en": "Portuguese","idioma_abrev": "pt"}, # el fixit no va 
            {"id_idioma": 14,"idioma_en": "Galician","idioma_abrev": "ga"}, 
            {"id_idioma": 15,"idioma_en": "Brazilian Portuguese","idioma_abrev": "br", "encoding2": "fixit"}, 
            {"id_idioma": 16,"idioma_en": "Croatian","idioma_abrev": "cr"}, 
            {"id_idioma": 17,"idioma_en": "Valencian","idioma_abrev": "val"}]

# idiomas = [{"id_idioma": 15,"idioma_en": "Brazilian Portuguese","idioma_abrev": "br", "encoding2": "fixit"}]

analisis1 = ""
analisis2 = ""
palabras = obtenerPalabras()
'''
for palabra in palabras:
    if palabra['def'] is None:
        palabra['def']=""
    if palabra['word'] is None:
        palabra['word']=""
    analisis1 = analisis1 + " " + palabra['word'] 
    analisis2 = analisis2 + " " + palabra['def']
encoding1 = chardet.detect(analisis1).get('encoding')
encoding2 = chardet.detect(analisis2).get('encoding')
if encoding1 is None:
    print "Unable to guess enconding type"
else: 
    print " Encoding expected to be: " + encoding1 + " y " + encoding2

for palabra in palabras:
    palabra['word'] = encode(palabra['word'], 'ISO-8859-1')
    palabra['def'] = encode(palabra['def'], 'ISO-8859-1')

with codecs.open("words_es.txt", 'w', encoding='utf-8') as outfile:
    json.dump(palabras, outfile, indent=4, sort_keys=True, default = myconverter, ensure_ascii=False, encoding='utf8')
'''
for idioma in idiomas:
    print idioma
    table = "traducciones_" + str(idioma['id_idioma'])
    palabras = obtenerTraducciones(table)
    analisis1=""
    analisis2=""
    for palabra in palabras:
        if palabra['def'] is None:
            palabra['def']=""
        if palabra['word'] is None:
            palabra['word']=""
        analisis1 = analisis1 + " " + palabra['word'] 
        analisis2 = analisis2 + " " + palabra['def']
    encoding1 = chardet.detect(analisis1).get('encoding')
    encoding2 = chardet.detect(analisis2).get('encoding')
    if encoding1 is None:
        print "Unable to guess enconding type"
    else: 
        print " Encoding expected to be: " + encoding1 + " y " + encoding2
    if 'encoding1' in idioma:
        encoding1=idioma['encoding1']
        print "Change encoding1 to " + encoding1
    if 'encoding2' in idioma:
        encoding2=idioma['encoding2']
        print "Change encoding2 to " + encoding2
    for palabra in palabras:
        #print palabra['word']
        palabra['word'] = encode(palabra['word'], encoding1)
        palabra['def'] = encode(palabra['def'], encoding2)
        #print palabra['def']
    fileName = "words_" + idioma['idioma_abrev'] + ".txt"
    with codecs.open(fileName, 'w', encoding='utf-8') as outfile:
        json.dump(palabras, outfile, indent=4, sort_keys=True, default = myconverter, ensure_ascii=False, encoding='utf8')
