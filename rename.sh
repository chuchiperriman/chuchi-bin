for f in *
do
    a="$(echo $f | sed s/Villanueva\ de\ Rampalay/Playa/)"
    mv "$f" "$a"
    # mv -i "${file}" "${file/Villanueva de Rampalay/Playa}"
done
