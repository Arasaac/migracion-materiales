#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
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

def encode(word):
    '''
    Usa chardet para convertir a unicode
    Devuelve cadena en utf-8
    Req:
    > pip install chardet
    '''
    encoding = chardet.detect(word).get('encoding')
    print encoding
    tmp = word.decode(encoding)  # unicode
    return tmp.encode('utf-8')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def openReadDatabase():
    return mysql.connector.connect(user='root', password='password', database='saac')


def obtenerPalabras():
    cnx = openReadDatabase()
    cursor = cnx.cursor()
    query = ("SELECT id_palabra, palabra, definicion FROM palabras ")
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
    query = ("SELECT id_palabra, traduccion, definicion_traduccion FROM " + table)
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


idiomas = [{"id_idioma": 2,"idioma_en": "Romanian","idioma_abrev": "ro"}, {"id_idioma": 3,"idioma_en": "Arabic","idioma_abrev": "ar"}, {"id_idioma": 4,"idioma_en": "Chinese","idioma_abrev": "zh"}, {"id_idioma": 5,"idioma_en": "Bulgarian","idioma_abrev": "bg"}, {"id_idioma": 6,"idioma_en": "Polish","idioma_abrev": "pl"}, {"id_idioma": 7,"idioma_en": "English","idioma_abrev": "en"}, {"id_idioma": 8,"idioma_en": "French","idioma_abrev": "fr"}, {"id_idioma": 9,"idioma_en": "Catalan","idioma_abrev": "ca"}, {"id_idioma": 10,"idioma_en": "Euskera","idioma_abrev": "eu"}, {"id_idioma": 11,"idioma_en": "German","idioma_abrev": "de"}, {"id_idioma": 12,"idioma_en": "Italian","idioma_abrev": "it"}, {"id_idioma": 13,"idioma_en": "Portuguese","idioma_abrev": "pt"}, {"id_idioma": 14,"idioma_en": "Galician","idioma_abrev": "ga"}, {"id_idioma": 15,"idioma_en": "Brazilian Portuguese","idioma_abrev": "br"}, {"id_idioma": 16,"idioma_en": "Croatian","idioma_abrev": "cr"}, {"id_idioma": 17,"idioma_en": "Valencian","idioma_abrev": "val"}]

palabras = obtenerPalabras()
with codecs.open('words_es.txt', 'w', encoding='utf-8') as outfile:
    json.dump(palabras, outfile, indent=4, sort_keys=True, default = myconverter, ensure_ascii=False)

for idioma in idiomas:
    print idioma
    table = "traducciones_" + str(idioma['id_idioma'])
    palabras = obtenerTraducciones(table)
    for palabra in palabras:
        print palabra['word']
        palabra['word'] = encode(palabra['word'])
        print "TRANSLATED###" + palabra['word']
    fileName = "words_" + idioma['idioma_abrev'] + ".txt"
    with codecs.open(fileName, 'w', encoding='utf-8') as outfile:
        json.dump(palabras, outfile, indent=4, sort_keys=True, default = myconverter, ensure_ascii=False)
