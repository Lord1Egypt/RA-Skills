# MiniMax Media Plugin

> Media generation plugin for OpenClaw - images, videos, TTS, and music

## Features

| Feature | Model | Description |
|---------|-------|-------------|
| 🖼️ Image | `image-01` | Interactive prompt input |
| 🎬 Video | `MiniMax-Hailuo-2.3` / `2.3-Fast` | Optional model selection |
| 🔊 TTS | `speech-2.8-hd` | 3 voice options |
| 🎵 Music | `music-2.6` / `music-2.5` | Optional model selection |

## Requirements

- OpenClaw gateway installed
- MiniMax API Key (configured during installation)

## Installation

### 1. Place the plugin
```bash
cp -r rocky-minimax-media/ ~/.openclaw/skills/
```

### 2. Add to openclaw.json
Add to `skills.entries`:
```json
"rocky-minimax-media": {
  "enabled": true
}
```

### 3. Run installation script
```bash
cd ~/.openclaw/skills/rocky-minimax-media/scripts
./install.sh
```
→ Enter your MiniMax API Key when prompted
→ Key will be automatically saved to openclaw.json

### 4. Restart gateway
```bash
openclaw gateway restart
```

## Configuration

### Get MiniMax API Key
Visit https://platform.minimaxi.com/ to register and get your API key.

The plugin reads the API key from `~/.openclaw/openclaw.json`. During installation, the script will automatically add the necessary configuration.

### Output Directory
```bash
# Default: ~/.openclaw/output
MINIMAX_OUTPUT_DIR=/path/to/output ~/.openclaw/skills/rocky-minimax-media/scripts/minimax.sh image
```

## Usage

```bash
./minimax.sh test   # Test all APIs
./minimax.sh image  # Generate image
./minimax.sh tts    # TTS voice synthesis
./minimax.sh video  # Video generation
./minimax.sh music  # Music generation
```

## Interactive Options

### Video Model
```
1) MiniMax-Hailuo-2.3        - Text-to-video, upgraded physical performance
2) MiniMax-Hailuo-2.3-Fast  - Image-to-video, faster generation
```

### Music Model
```
1) music-2.6  - Latest version, better quality
2) music-2.5  - Classic version
```

### TTS Voice
```
1) male-qn-qingse   - Male, young, inexperienced
2) female-tianmei   - Female, sweet
3) female-yujie     - Female, mature
```

## API Endpoints

- **Base URL**: `https://api.minimaxi.com`
- **TTS**: `POST /v1/t2a_v2`
- **Image**: `POST /v1/image_generation`
- **Video**: `POST /v1/video_generation`
- **Music**: `POST /v1/music_generation`

## Uninstall

Remove from `skills.entries` in openclaw.json and delete the plugin directory:
```bash
rm -rf ~/.openclaw/skills/rocky-minimax-media
```

Then restart the gateway.

---

**Version**: 1.3.0  
**For OpenClaw**: https://openclaw.ai
