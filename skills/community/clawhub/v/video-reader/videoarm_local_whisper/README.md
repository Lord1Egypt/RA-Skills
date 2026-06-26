# Local Whisper Service

Minimal FastAPI service using faster-whisper, compatible with OpenAI Whisper API format.

## Installation

```bash
pip install -e ".[whisper-local]"
```

## Setup

```bash
videoarm-setup-whisper
```

This will:
- Download whisper base model to `~/.cache/whisper/`
- Update `.env` with `OPENAI_BASE_URL=http://127.0.0.1:8765/v1`

## Usage

### Manual start
```bash
python -m videoarm_local_whisper.server
```

### Auto-start with launchd (macOS)
```bash
cp scripts/videoarm-whisper.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/videoarm-whisper.plist
```

### Stop service
```bash
launchctl unload ~/Library/LaunchAgents/videoarm-whisper.plist
```

## API Endpoint

Compatible with OpenAI Whisper API:
- POST `/v1/audio/transcriptions`
- GET `/health`

Service runs on `http://127.0.0.1:8765`
