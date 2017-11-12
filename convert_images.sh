#!/bin/bash

mkdir -p converted

for IMG in `ls 'images/' | grep pgm`; do convert images/$IMG converted/$IMG.jpg; done;
echo Done.;
