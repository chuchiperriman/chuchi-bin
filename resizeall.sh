# 4k
BASE_DIR=~/Imágenes
RESOLUTION=3840x2160
DIR_IMPORTAR=$BASE_DIR/Importar
DIR_TRANSFORMAR=$BASE_DIR/Subir

for dirmes in $(find $DIR_IMPORTAR -name "??" -type d); do
  dirano=$(dirname $dirmes)
  mes=$(basename $dirmes)
  ano=$(basename $dirano)
  dirmesfin=$DIR_TRANSFORMAR/$ano/$mes
  echo $dirmes
  echo $dirano
  echo $mes
  echo $ano
  echo $dirmesfin
  IFS=$'\n'
  for file in $(find $dirmes -iname '*.jpg'); do
    mkdir -p $dirmesfin
    # res=${file%.*}-$RESOLUTION.jpg
    # res=$dirmesfin/$(basename $res)
    res=$dirmesfin/$(basename $file)
    convert $file -resize $RESOLUTION "$res"
    echo $file - $res
  done
  cp $dirmes/*.MTS $dirmes/*.mts $dirmes/*.avi $dirmes/*.AVI $dirmes/*.Avi $dirmes/*.mp4 $dirmes/*.MP4 $dirmes/*.Mp4 $dirmesfin/.
done

NUM_IMPORTAR=$(find $DIR_IMPORTAR | wc -l)
NUM_TRANSFORMAR=$(find $DIR_TRANSFORMAR | wc -l)

if [ $NUM_IMPORTAR != $NUM_TRANSFORMAR ]; then
  echo "*************************************"
  echo "Hay distinto número de ficheros: Inicio: $NUM_IMPORTAR, transformado: $NUM_TRANSFORMAR"
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
fi
echo "Para importar: $NUM_IMPORTAR"
echo "Importadas: $NUM_TRANSFORMAR"

