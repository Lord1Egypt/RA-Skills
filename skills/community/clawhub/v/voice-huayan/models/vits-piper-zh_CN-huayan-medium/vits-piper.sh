#!/usr/bin/env bash

lang=$LANG
echo "lang: $LANG"

name=$NAME
if [[ $name == 'tugao' && $lang == "pt_PT" ]]; then
  name=tugão
  export NAME=tugão
fi

echo "name: $name"

type=$TYPE
echo "type: $type"

pip install iso639-lang

set -ex

# for en_US-lessac-medium.onnx
# export LANG=en_US
# export TYPE=lessac
# export NAME=medium

# if lang is en_US, then code is en
code=${lang:0:2}

if [[ $name == gyro && $lang == fa_IR && $type == medium ]]; then
  wget -qq https://huggingface.co/gyroing/Persian-Piper-Model-gyro/resolve/main/fa_IR-gyro-medium.onnx
  wget -qq https://huggingface.co/gyroing/Persian-Piper-Model-gyro/resolve/main/fa_IR-gyro-medium.onnx.json
  wget -qq https://huggingface.co/gyroing/Persian-Piper-Model-gyro/resolve/main/MODEL_CARD
elif [[ $name == "rezahedayatfar-ibrahimwalk" && $lang == fa_en ]]; then
  wget https://huggingface.co/mah92/persian-english-piper-tts-model/resolve/main/fa_en-rezahedayatfar-ibrahimwalk-medium.onnx
  wget https://huggingface.co/mah92/persian-english-piper-tts-model/resolve/main/fa_en-rezahedayatfar-ibrahimwalk-medium.onnx.json
  wget https://huggingface.co/mah92/persian-english-piper-tts-model/resolve/main/MODEL_CARD
else
  wget -qq https://huggingface.co/rhasspy/piper-voices/resolve/main/$code/$lang/$name/$type/$lang-$name-$type.onnx
  wget -qq https://huggingface.co/rhasspy/piper-voices/resolve/main/$code/$lang/$name/$type/$lang-$name-$type.onnx.json
  wget -qq https://huggingface.co/rhasspy/piper-voices/resolve/main/$code/$lang/$name/$type/MODEL_CARD
fi

wget -qq https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/espeak-ng-data.tar.bz2
tar xf espeak-ng-data.tar.bz2
rm espeak-ng-data.tar.bz2

pip install piper-phonemize onnx onnxruntime==1.16.0

python3 ./vits-piper.py
