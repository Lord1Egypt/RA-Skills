---
slug: tts-responder
display_name: TTS Responder
description: Convierte respuestas de texto a audio (OGG) y las envía por Telegram. Uso: "responde de forma hablada".
homepage: https://github.com/openclaw/skills
metadata:
  clawdbot:
    emoji: 🔊
    requires:
      bins: ["piper", "ffmpeg", "sox"]
      env: []
    primaryEnv: null
---

# TTS Responder

Genera respuestas de voz a partir de texto y las envía al chat de Telegram como mensaje de audio.

## Configuración

Requiere tener instalado:
- `piper` (TTS neuronal, gratis, local)
- `ffmpeg` (para convertir a OGG Opus)
- `sox` (opcional, para manipulación de audio)

Instalación en Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y piper ffmpeg sox
```

### Variables de entorno (opcionales)
- `TTS_VOICE`: Modelo de voz de Piper (por defecto: `es_ES/carlfm/x_low` – español, voz masculina)
- `TTS_SPEED`: Factor de velocidad (1.0 = normal)

## Uso

En tu conversación con FryBot:
- Di: *"responde de forma hablada"* → a partir de ahí, mis respuestas se enviarán como audio
- Di: *"responde de forma escrita"* → vuelta a texto normal

Internamente, esta skill intercepta la salida de texto de FryBot, la sintetiza a OGG y la envía por la API de Telegram.

## Comandos directos (para pruebas)

```bash
# Probar Piper (genera WAV)
echo "Hola, esto es una prueba" | piper --model es_ES/carlfm/x_low --output_file /tmp/test.wav

# Convertir a OGG Opus (Telegram)
ffmpeg -i /tmp/test.wav -c:a libopus -b:a 32k /tmp/test.ogg
```

## Notas

- Piper es software libre, se ejecuta completamente localmente.
- Los modelos de voz se descargan automáticamente al primer uso (unos 50 MB).
- Asegúrate de que el bot de Telegram tenga permisos para enviar mensajes de audio.