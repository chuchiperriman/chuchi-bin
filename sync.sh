#!/bin/sh

set -e

LOCAL="$HOME/Imágenes/Fotos"
if [ ! -d "$LOCAL" ]; then
    mkdir $LOCAL
fi
if [ ! -d "$LOCAL" ]; then
    echo "No existe el directorio $LOCAL"
    exit
fi

REMOTO=/media/DatosLinux/Imágenes/Fotos
if [ ! -d "$REMOTO" ]; then
    REMOTO=/media/perriman/DatosLinux/Imágenes/Fotos
fi
if [ ! -d "$REMOTO" ]; then
    REMOTO=/run/media/perriman/DatosLinux/Imágenes/Fotos
fi
if [ ! -d "$REMOTO" ]; then
    echo "No se encuentra el directorio del pendrive"
    exit
fi
# Sincroniza lo que hay en local con lo que hay en el disco (sin eliminar)
rsync -avz $LOCAL $REMOTO/..
# Sincroniza de remoto a local sin eliminar
rsync -avz $REMOTO $LOCAL/..
