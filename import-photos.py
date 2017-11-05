#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pdb
from shutil import copyfile
from PIL import Image
from PIL.ExifTags import TAGS
import time

PRE_FOLDER = "/home/perriman/Imágenes/Pre-importar"
IMPORTAR_FOLDER = "/home/perriman/Imágenes/Importar"
SUBIR_FOLDER = "/home/perriman/Imágenes/Subir"
FOTOS_FOLDER = "/home/perriman/Imágenes/Fotos"

no_processed = []
processed = []

class Processor:
    def __init__(self, f):
        self.file = f
        self.datetime = None
        filename, ext = os.path.splitext(self.file)
        ext = ext.lower()
        if ext in ['.jpg', '.jpeg']:
            self.type = 'jpg'
            self.datetime = self._get_exif(self.file)["DateTimeOriginal"]
        elif ext == '.mts':
            self.type = 'mts'
            et_output = os.popen("exiftool \"%s\"" % self.file.encode('utf-8')).read()
            for l in et_output.split('\n'):
                if 'Date/Time Original' in l:
                    self.datetime = l.split(':', 1)[1].strip()
        if not self.datetime:
            raise Exception("No se pudo determinar la fecha o tipo de fichero para %s" % self.file.encode('utf-8'))

        # Está en formato 2017:05:02 17:19:51+02:00
        self.datetime = self.datetime.replace(":", "") \
                                     .replace(" ", "_") \
                                     .split('+', 1)[0]
        self.date = self.datetime.split('_', 1)[0]
        self.year = int(self.datetime[0:4])
        if self.year < 1990 or self.year > 2020:
            raise Exception("Año incorecto %d" % self.year)

    def process(self):
        print(self.file)
        self._copy_file_for_import()
        if self.type == 'jpg':
            self._copy_image_for_upload()
        elif self.type == 'mts':
            self._copy_file_for_upload()
        else:
            raise Exception("Tipo de fichero desconocido para subir: %s" % self.type)

    def _get_exif(self, fn):
        ret = {}
        i = Image.open(fn)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret

    def _copy_file_for_import(self):
        # No convertimos a int para mantener el 0 por ejemplo de 08
        month = self.datetime[4:6]

        number = 0
        new_name = "%s-%s" % (self.date, os.path.basename(self.file).lower())

        dest_file = os.path.join(IMPORTAR_FOLDER.decode('utf-8'), str(self.year), month, new_name)
        original_filename, file_extension = os.path.splitext(new_name)
        # pdb.set_trace()
        while os.path.exists(dest_file):
            number += 1
            # TODO Mirar si es el mismo fichero comprobando el CRC o MD5
            new_name = "%s-%d%s" % (original_filename, number, file_extension)
            dest_file = os.path.join(IMPORTAR_FOLDER.decode('utf-8'), str(self.year), month, new_name)
        dest_dir = os.path.dirname(dest_file)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        print ("Copiamos %s" % dest_file)
        copyfile(self.file, dest_file)
        self.imported_file = dest_file

    def _copy_image_for_upload(self):
        dest_file = os.path.join(SUBIR_FOLDER.decode('utf-8'), os.path.basename(self.imported_file))
        dest_dir = os.path.dirname(dest_file)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        command = "convert %s -resize '3840x2160' '%s'" % (
            self.file,
            dest_file)
        res = os.system(command.encode('utf-8'))
        if res != 0:
            raise Exception("Error al convertir imágen para subir: %s" % dest_file)

    def _copy_file_for_upload(self):
        dest_file = os.path.join(SUBIR_FOLDER.decode('utf-8'), os.path.basename(self.imported_file))
        dest_dir = os.path.dirname(dest_file)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        copyfile(self.imported_file, dest_file)

os.chdir(PRE_FOLDER)

for root, dirs, files in os.walk(PRE_FOLDER, topdown=False):
    for name in files:
        processor = Processor(os.path.join(root, name).decode('utf-8'))
        try:
            processor.process()
            processed.append(file)
        except Exception as e:
            no_processed.append("%s: %s" % (file, str(e)))
    for name in dirs:
        print(os.path.join(root, name))

print "Procesados: %s" % len(processed)
print ('*' * 70)
print ("No procesados: %d" % len(no_processed))
for np in no_processed:
    print ("%s no procesado" % np)