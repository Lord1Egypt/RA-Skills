#!/usr/bin/env bash
set -euo pipefail

# TTS Responder – convierte texto a audio OGG y envía por Telegram
# Requiere: piper, ffmpeg

TEXT="${1:-}"
OUTPUT_WAV="/tmp/tts-output.wav"
OUTPUT_OGG="/tmp/tts-output.ogg"

# Configuración por defecto
VOICE="${TTS_VOICE:-es_ES/carlfm/x_low}"
SPEED="${TTS_SPEED:-1.0}"

if [[ -z "$TEXT" ]]; then
  echo "Uso: $0 \"texto a hablar\""
  exit 1
fi

# 1. Sintetizar con Piper
piper --model "$VOICE" --output_file "$OUTPUT_WAV" --length_scale $(echo "$SPEED" | awk '{print 1/$1}') <<< "$TEXT"

# 2. Convertir a OGG Opus (formato Telegram)
ffmpeg -y -i "$OUTPUT_WAV" -c:a libopus -b:a 32k -ar 48000 "$OUTPUT_OGG" > /dev/null 2>&1

# 3. Enviar por Telegram (requiere BOT_TOKEN y CHAT_ID en variables de entorno)
if [[ -n "${BOT_TOKEN:-}" && -n "${CHAT_ID:-}" ]]; then
  curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendVoice" \
    -F "chat_id=${CHAT_ID}" \
    -F "voice=@${OUTPUT_OGG}" \
    -F "caption=${TEXT:0:100}..." > /dev/null
  echo "Audio enviado"
else
  echo "Faltan BOT_TOKEN o CHAT_ID. Generado: ${OUTPUT_OGG}"
fi

# Limpieza
rm -f "$OUTPUT_WAV"