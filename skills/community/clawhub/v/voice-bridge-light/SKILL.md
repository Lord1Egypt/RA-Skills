# Voice Bridge Light

Lightweight offline voice bridging service providing OpenAI-compatible STT/TTS HTTP API.

## Features

- **TTS Text-to-Speech**: Supports Edge TTS (online) and Piper (local)
- **STT Speech Recognition**: Based on Whisper local recognition
- **OpenAI Compatible API**: Compatible with OpenAI Audio API
- **Lightweight Deployment**: Minimal dependencies, easy to install

## Usage

### Installation

```bash
pip install -r requirements.txt
```

### Start Service

Default using Edge TTS:
```bash
python api_server.py
```

Using Piper (model required):
```bash
TTS_ENGINE=piper PIPER_MODEL=models/piper/zh_CN-huayan-medium.onnx python api_server.py
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /health` | GET | Health check |
| `POST /audio/speech` | POST | TTS speech synthesis |
| `POST /audio/transcriptions` | POST | STT speech recognition |

### Configuration Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICE_BRIDGE_HOST` | `0.0.0.0` | Listen address |
| `VOICE_BRIDGE_PORT` | `18790` | Listen port |
| `TTS_ENGINE` | `edge` | TTS engine: `edge` or `piper` |
| `EDGE_VOICE` | `zh-CN-XiaoxiaoNeural` | Edge TTS voice |
| `PIPER_MODEL` | `models/piper/zh_CN-huayan-medium.onnx` | Piper model path |
| `STT_MODEL` | `base` | Whisper model size |

### TTS Request Example

```bash
curl -X POST http://localhost:18790/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hello, world!",
    "voice": "zh-CN-XiaoxiaoNeural",
    "response_format": "mp3"
  }' \
  --output speech.mp3
```

### STT Request Example

```bash
curl -X POST http://localhost:18790/audio/transcriptions \
  -F "file=@speech.mp3" \
  -H "Content-Type: multipart/form-data"
```

## OpenClaw Integration

Configure in `openclaw.json`:

```json
{
  "tts": {
    "enabled": true,
    "provider": "local-piper",
    "baseUrl": "http://127.0.0.1:18790",
    "apiKey": "local",
    "voice": "zh-CN-XiaoxiaoNeural"
  }
}
```

## Dependencies

- Python 3.8+
- edge-tts (Edge TTS)
- faster-whisper (Whisper STT)
- soundfile (audio processing)
- Flask + Flask-CORS (web service)

## Service Management

### systemd Service (Recommended)

```ini
[Unit]
Description=Voice Bridge Light - STT/TTS HTTP API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/skills/voice-bridge-light
ExecStart=/usr/bin/python3 api_server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl daemon-reload
systemctl enable voice-bridge-light.service
systemctl start voice-bridge-light.service
```

## Performance

- TTS latency: < 1s (Edge TTS requires network)
- STT latency: depends on audio length, real-time CPU
- Memory usage: ~300-500MB (mainly from Whisper model)

## Notes

- Edge TTS requires internet access to Microsoft services
- Piper requires downloading model files (first use)
- Whisper model loads slowly on first run, recommend warm-up
- Production environment recommended to use systemd management

## License

MIT
