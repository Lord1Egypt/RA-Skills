# xiaozhiclaw 🧤

** OpenClaw Channel for XiaoZhi AI Device (ESP32 hardware) **

Connect your XiaoZhi AI Device to OpenClaw agents for real-time voice interaction. Give your AI assistant a physical body!

## Features

- 🎤 **Real-time Voice Communication** - Talk to your AI assistant through XiaoZhi hardware
- 🔌 **WebSocket Bridge** - Simple WebSocket server for XiaoZhi firmware connection
- 🤖 **OpenClaw Integration** - Seamless integration with OpenClaw agent ecosystem
- 🎙️ **Volcengine Doubao STT/TTS** - High-quality speech-to-text and text-to-speech
- 🛠️ **Extensible** - Easy to add custom STT/TTS providers

## Quick Start

### Prerequisites

- Node.js v20+
- XiaoZhi ESP32 device with firmware flashed
- OpenClaw installed
- Volcengine Doubao API credentials (for STT/TTS)

### Installation

```bash
# Clone the repository
git clone https://github.com/leohuang8688/xiaozhiclaw.git
cd xiaozhiclaw

# Install dependencies
npm install

# Build the plugin
npm run build
```

### Configuration

#### 1. Set up Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

```bash
# Volcengine Doubao API Credentials
DOUBAO_APP_ID=your_app_id_here
DOUBAO_ACCESS_TOKEN=your_access_token_here

# WebSocket Server Configuration
XIAOZHI_PORT=8080
```

**⚠️ Security Notice:**
- NEVER commit your `.env` file to Git
- The `.env` file is already in `.gitignore`
- Use `.env.example` as a template for sharing

#### 2. Add to OpenClaw Configuration

```json
{
  "extensions": {
    "xiaozhiclaw": {
      "port": 8080
    }
  }
}
```

### Connect XiaoZhi Device

Configure your XiaoZhi firmware to connect to:
```
ws://YOUR_COMPUTER_IP:8080
```

### Restart OpenClaw

```bash
openclaw gateway restart
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

## Protocol

### WebSocket Messages

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

**Listen Start:**
```json
{
  "type": "listen",
  "state": "start"
}
```

**Listen Stop:**
```json
{
  "type": "listen",
  "state": "stop",
  "text": "transcribed text"
}
```

**TTS Start:**
```json
{
  "type": "tts",
  "state": "start",
  "text": "response text"
}
```

**TTS Stop:**
```json
{
  "type": "tts",
  "state": "stop"
}
```

## Development

```bash
# Watch mode for development
npm run dev

# Build for production
npm run build
```

## Roadmap

- [x] WebSocket server implementation
- [x] Basic handshake protocol
- [x] Text message support
- [x] Opus audio encoding/decoding
- [x] Volcengine Doubao STT integration
- [x] Volcengine Doubao TTS integration
- [x] Real-time voice conversation
- [ ] Hardware control (volume, brightness)
- [ ] Multi-device support
- [ ] Offline STT/TTS support

## License

MIT

## Credits

- OpenClaw Team
- XiaoZhi AI ESP32 Project
- Volcengine Doubao
- PocketAI 🧤
