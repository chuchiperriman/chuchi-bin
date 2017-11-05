#!/bin/bash

WHATSAPP_FOLDER="$HOME/Imágenes/Pre-importar/20160907 Móvil"

if [ ! -d "$WHATSAPP_FOLDER" ]; then
  echo "No existe $WHATSAPP_FOLDER"
  exit -1
fi


# for file in "/home/chuchi/personal/telefono/WhatsApp/Media/WhatsApp Images/"*.jpg
# do
#     if [[ -f $file ]]; then
#         filename=`basename "$file"`
#         fecha=$(echo $filename | cut -f2 -d-)
#         fecha=${fecha:0:4}:${fecha:4:2}:${fecha:6:2}
#         echo $filename : $fecha
#         exiftool -overwrite_original "-DateTimeOriginal=$fecha 12:00:00" "$file"
#     fi
# done
