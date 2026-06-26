---
name: xiaozhiclaw
description: XiaoZhi AI Device (ESP32) integration for OpenClaw. Enables real-time voice interaction with your AI assistant through XiaoZhi hardware. Supports WebSocket bridge, Volcengine Doubao STT/TTS, and Opus audio streaming.
---

# XiaoZhiClaw - XiaoZhi AI Device Integration

## 🔒 Security

- ✅ No external API keys stored in code
- ✅ All credentials via environment variables
- ✅ No shell command execution
- ✅ WebSocket connections only (no inbound HTTP)
- ✅ Open source and auditable
- ⚠️ Requires Volcengine Doubao API credentials

## Overview

XiaoZhiClaw is an OpenClaw channel that connects XiaoZhi AI ESP32 hardware devices to OpenClaw agents, enabling real-time voice interaction.

## Permissions

### Required Permissions
- ✅ Network Access: WebSocket server (port 8080 by default)
- ✅ Audio Processing: Opus encoding/decoding
- ✅ STT/TTS API: Volcengine Doubao (HTTPS)
- ❌ No Admin/Root Privileges Required
- ❌ No System Command Execution

### Data Flow
```
XiaoZhi Device → WebSocket → STT (Doubao) → OpenClaw Agent
     ↓                                          ↓
  Microphone                              AI Response
     ↓                                          ↓
  Speaker ← WebSocket ← TTS (Doubao) ← OpenClaw Agent
```

## Use Cases

### 1. Voice Conversation
```
Talk to your AI assistant through XiaoZhi hardware
Ask questions and get voice responses
Real-time voice interaction
```

### 2. Hardware Control
```
Control volume, brightness via MCP commands
Hardware status monitoring
Device management
```

### 3. Voice Commands
```
Voice-activated AI assistant
Hands-free operation
Physical AI companion
```

## Usage Examples

### Start the Service

```bash
# The WebSocket server starts automatically when OpenClaw starts
# Default port: 8080
```

### Configure XiaoZhi Device

Configure your XiaoZhi firmware to connect to:
```
ws://YOUR_COMPUTER_IP:8080
```

### Voice Interaction Flow

1. **User speaks** → XiaoZhi microphone captures audio
2. **Audio streaming** → Opus frames sent via WebSocket
3. **STT processing** → Volcengine Doubao transcribes to text
4. **AI processing** → OpenClaw agent processes and responds
5. **TTS processing** → Volcengine Doubao converts to speech
6. **Audio playback** → XiaoZhi speaker plays response

## Environment Variables

```bash
# Required: Volcengine Doubao API Credentials
# Get from: https://console.volcengine.com/
DOUBAO_APP_ID=your_app_id_here
DOUBAO_ACCESS_TOKEN=your_access_token_here

# Optional: WebSocket Server Configuration
XIAOZHI_PORT=8080

# Optional: Audio Configuration
AUDIO_SAMPLE_RATE=16000
AUDIO_FRAME_DURATION=60
```

## Protocol

### WebSocket Message Types

**Handshake:**
```json
{
  "type": "hello",
  "transport": "websocket",
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "frame_duration": 60
  }
}
```

**Listen Events:**
```json
{
  "type": "listen",
  "state": "start"
}
```

```json
{
  "type": "listen",
  "state": "stop",
  "text": "transcribed text"
}
```

**TTS Events:**
```json
{
  "type": "tts",
  "state": "start",
  "text": "response text"
}
```

```json
{
  "type": "tts",
  "state": "stop"
}
```

## Architecture

```
XiaoZhi ESP32 ←→ WebSocket Server ←→ OpenClaw Channel ←→ AI Agent
     ↓                ↓                    ↓              ↓
  Microphone    Port 8080          xiaozhiclaw      PocketAI
     ↓                ↓                    ↓              ↓
  Speaker      Opus Audio         Message Router   Response
                     ↓
              Doubao STT/TTS
```

## Notes

1. **Network:** Ensure port 8080 is open on your firewall
2. **Latency:** Use wired connection or high-speed Wi-Fi for best results
3. **API Credentials:** Volcengine Doubao API credentials required for STT/TTS
4. **Audio Format:** Opus encoding, 16kHz sample rate, 60ms frame duration

## Troubleshooting

### Connection Refused
- Check if port 8080 is open
- Verify XiaoZhi device network settings
- Check firewall settings

### Audio Lag
- Check network latency
- Use wired connection if possible
- Ensure good Wi-Fi signal strength

### STT/TTS Not Working
- Verify Volcengine API credentials
- Check API quota and billing
- Verify network connectivity to Volcengine API

### Device Not Connecting
- Verify WebSocket URL format: `ws://IP:PORT`
- Check XiaoZhi firmware configuration
- Ensure OpenClaw gateway is running

## Resources

- [XiaoZhi AI ESP32 Project](https://github.com/xiaozhi-ai)
- [Volcengine Doubao API](https://www.volcengine.com/)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [Opus Audio Codec](https://opus-codec.org/)

## Changelog

### v1.0.0 (2026-03-12)
- ✅ Initial release
- ✅ WebSocket server implementation
- ✅ Volcengine Doubao STT/TTS integration
- ✅ Opus audio encoding/decoding
- ✅ Real-time voice conversation
- ✅ OpenClaw channel integration

## License

MIT License

## Author

PocketAI for Leo - OpenClaw Community

## Credits

- OpenClaw Team
- XiaoZhi AI ESP32 Project
- Volcengine Doubao
- PocketAI 🧤
