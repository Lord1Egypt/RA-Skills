#!/bin/bash
# openclaw-whisper-bridge.sh
# Bridge to redirect whisper CLI calls to Sphinx GPU Server

AUDIO_PATH=$1
MODEL=$2 # Ignored, server uses its own model
LANG=${3:-es}

# Invocación al servidor Sphinx
RESULT=$(curl -s -X POST http://sphinx.espuny.net:5000/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@$AUDIO_PATH" \
  -F "model=whisper-1" \
  -F "language=$LANG" \
  -F "response_format=json")

# Extraer el texto del JSON
echo "$RESULT" | jq -r '.text'
