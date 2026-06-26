# TTS TopMediai

Text-to-Speech skill based on TopMediai API.

## Installation
1. Place this skill in your workspace:
   `~/.openclaw/workspace/skills/tts-topmediai/`
2. Copy `.env.example` to `.env`
3. Fill your key:
   - `TOPMEDIAI_API_KEY=YOUR_KEY`
   - `TOPMEDIAI_BASE_URL=https://api.topmediai.com` (optional)
4. Install dependencies:
   - `pip install -r requirements.txt`

## Main Command
```text
/tts_topmediai action=info|voices|tts text="..." speaker="..." emotion="..."
```

## Features
- Get current key entitlement information
- List official and cloned voices
- Convert input text to speech with selected speaker

## API Mapping
- `GET /v1/get_api_key_info`
- `GET /v1/voices_list`
- `GET /v1/clone_voices_list`
- `POST /v1/text2speech`
