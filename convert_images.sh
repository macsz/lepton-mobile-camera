#!/bin/bash

mkdir -p converted

for IMG in `ls 'images/' | grep pgm`; do convert images/$IMG -resize 800x600 converted/$IMG.jpg; done;
echo Done.;
