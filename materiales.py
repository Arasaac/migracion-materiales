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

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def getId(str):
    """Obtenemos por ejemplo {1}{2}{3} como foreign key y devolvemos un array
    con la lista de id"""
    return '' if (str is None or str == '') else str[1:-1].split('}{')


def openReadDatabase():
    return mysql.connector.connect(user='root', password='password', database='saac')


def obtenerMateriales():
    # cnx = openReadDatabase()
    cursor = cnx.cursor()
    query = ("SELECT * FROM materiales where id_material=1")
    cursor.execute(query)
    materiales = []
    columns = tuple([d[0].decode('utf8') for d in cursor.description])
    for row in cursor:
        materiales.append(dict(zip(columns, row)))
    cursor.close()
    # cnx.close()
    #pdb.set_trace()
    # Algún campo, realmente corresponde a arrays de datos:
    campos = (
        'material_autor', 'material_tipo', 'material_area_curricular', 'material_subarea_curricular', 'material_archivos',
        'material_idiomas'
    )
    # cambiamos los campos de tipo {1}{2}.. a algo como [1,2,..]
    for material in materiales:
        for campo in campos:
            material[campo] = getId(material[campo])
            print campo
            print material[campo]
        # El campo descripción está guardado en html:
        soup = BeautifulSoup(material['material_descripcion'], 'html.parser')
        material['material_descripcion'] = soup.get_text().replace('\n', '\n\n')
        #print material['id_material']
        material['material_area_curricular'] = material['material_area_curricular'] if material['material_area_curricular'] else []
        material['material_subarea_curricular'] = material['material_subarea_curricular'] if material['material_subarea_curricular'] else []
        material['areas'] = material['material_area_curricular'] + material['material_subarea_curricular']
        print material['areas']

        # Borramos los datos que no nos interesan:
        del material['material_area_curricular']
        del material['material_subarea_curricular']
        del material['material_nivel']
        del material['material_objetivos']
        del material['material_dirigido']
        del material['material_edad']
        del material['material_saa']
    return materiales


def obtenerAutores():
    # cnx = openReadDatabase()
    cursor = cnx.cursor()
    query = ("SELECT * FROM autores")
    cursor.execute(query)
    autores = []
    columns = tuple([d[0].decode('utf8') for d in cursor.description])
    for row in cursor:
        autores.append(dict(zip(columns, row)))
    cursor.close()
    # cnx.close()
    return autores

def transformarMateriales():
    newMaterials=[]
    for material in materiales:
        newMaterial ={}
        # newMaterial['areas'] = [areasCurriculares[str(a)] for a in material['areas']]
        print material['areas']
        newMaterial['areas'] = [areasCurriculares[str(a)] for a in material['areas']]
        print newMaterial['areas']
        newMaterial['idMaterial'] = [material['id_material']]
       # newMaterial['licencia'] = licencias[material['material_licencia']]
       # newMaterial['estado'] = estados[material['material_estado']]
        newMaterial['actividades'] = [actividades[str(a)] for a in material['material_tipo']]
        newMaterial['titulo'] = material['material_titulo']
        newMaterial['descripcion'] = material['material_descripcion']
       # newMaterial['archivos'] = material['material_archivos']
       # newMaterial['imagenes'] = []
       # newMaterial['recomendado'] = False
       # newMaterial['etiquetas'] = []
       # newMaterial['fechaAlta'] = material['fecha_alta']
       # newMaterial['zip'] = str(material['id_material']) + ".zip"
       # newMaterial['fechaActualizacion']=None
       # newMaterial['idiomas'] = material['material_idiomas']
       # newMaterial['autores'] = [autor for autor in autores if autor['id_autor'] in map(int, material['material_autor'])]

        # pdb.set_trace()
        newMaterials.append(newMaterial)
    return newMaterials

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

actividades = {
    '24': u'Libro LIM',  # actividad lim
    '29': u'Actividad para Picaa',  # actividad picaa
    '14': u'GIF animado',  # animación
    '2': u'Aplicación Informática',  # aplicación informática
    '31': u'Tablero para AraBoard',  # araboard
    '32': u'Bingo',  # bingo
    '20': u'Canción',  # canción
    '19': u'Cuaderno',  # cuaderno
    '1': u'Cuento',  # cuento
    '34': u'Dominó',  # dominos
    '15': u'Ficha de actividades',  # ficha
    '28': u'JClic',  # jclic
    '6': u'Juego Colectivo',  # juego colectivo
    '33': u'Juego de la Oca',  # juego de la oca
    '5': u'Juego Individual',  # juego individual
    '18': u'Libro',  # libro
    '3': u'Material Audiovisual',  # material audiovisual
    '30': u'Tablero para PictoDroid Lite',  # pictodroid Lite
    '21': u'Pizarra Digital - PDI',  # pizarra digital
    '4': u'Presentación por Diapositivas',  # presentación
    '12': u'Protocolo de exploración',  # protocolo
    '26': u'Rutina',  # rutinas
    '25': u'Señaléctica',  # señaléctica
    '27': u'Secuencia',  # secuencias
    '23': u'Smart Notebook',  # smart notebook
    '16': u'Tablero de comunicación',  # tablero
    '22': u'Tablero para TICO',  # tablero tico
    '13': u'Test de Evaluación'  # test de evaluación
}

areasCurriculares = {
    '1': [u'Literatura'],   # Lengua y literatura
    '2': [u'Numeración (Matemáticas)', u'Operaciones básicas (Matemáticas)', u'Problemas (Matemáticas)', u'Geometría (Matemáticas)'],   # Matemáticas
    '4': [u'Ciencias Naturales', u'Ciencias Sociales'],   # Conocimiento del medio natural, social y cultural
    '6': [u'Plástica'],   # Educación artística
    '7': [u'Conocimiento de si mismo y autonomía personal'],   # Conocimiento de si mismo y autonomía personal
    '8': [u'Desconocida8'],   # Taller,
    '11': [u'Desconocida11'],
    '12': [u'Desconocida12'],
    '9': [u'Educación Física'],   # Educación física
    '10':  [u'Religión'],  # Religión,
    '14': [u'Fonología (Lenguaje)'],  # Fonética - fonología
    '13': [u'Discriminación visual (Lenguaje)', u'Discriminación auditiva (Lenguaje)'],  # Habilidades prelingüísticas
    '18': [u'Lectura (Lenguaje)', u'Escritura (Lenguaje)'],  # Lectura y escritura
    '19': [u'Música'],  # Música
    '16': [u'Morfosintaxis (Lenguaje)'],  # Morfosintaxis
    '20': [u'Plástica'],  # Plástica
    '17': [u'Pragmática (Lenguaje)'],  # Pragmática
    '15': [u'Semántica (Lenguaje)']  # Semántica
}

estados = {
    0: [u'Pendiente de revisión'],   # Lengua y literatura
    1: [u'Publico'],   # Matemáticas
    2: [u'Privado'],   #
}

idiomas = {
    'ar': 152,
    'bg': 153,
    'br': 164,
    'ca': 154,
    'de': 151,
    'en': 160,
    'eu': 157,
    'fr': 158,
    'ga': 159,
    'it': 161,
    'pl': 162,
    'pt': 163,
    'ro': 167,
    'ru': 168,
    'zh': 155,
    'es': 156
}

licencias = {
    1: u'Sin definir',  # sin definir
    2: u'Creative Commons BY-NC-SA',  # Creative Commons BY-NC-SA
    3: u'Software propietario',  # Software propietario
    4: u'GNU General Public License',  # GNU General Public License
    5: u'Mozilla Public License'  # Mozilla Public License
}


cnx = openReadDatabase()

materiales = obtenerMateriales()
autores = obtenerAutores()

cnx.close()

#MyPrettyPrinter().pprint(materiales)
#MyPrettyPrinter().pprint(autores)
#pprint.pprint(materiales)

newMaterials = transformarMateriales()
#MyPrettyPrinter().pprint(newMaterials)

# print json.dumps(MyPrettyPrinter().pprint(newMaterials))
# MyPrettyPrinter().pprint(newMaterials)
with codecs.open('materiales.txt', 'w', encoding='utf-8') as outfile:
    json.dump(newMaterials, outfile, indent=4, sort_keys=True, default = myconverter, ensure_ascii=False)
