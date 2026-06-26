---
name: song-recognition
description: Recognize songs by singing or audio file using iFlytek's Query By ACRCloud technology.
homepage: https://www.xfyun.cn/doc/voiceservice/music_recognition/API.html
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": {
          "bins": ["python3"],
          "env": ["XF_SONG_APP_ID", "XF_SONG_API_KEY", "XF_SONG_API_SECRET"]
        },
        "primaryEnv": "XF_SONG_APP_ID"
      }
  }
---

# 🎵 Song Recognition

Recognize songs by singing, or audio file using iFlytek's advanced Query By ACRCloud technology.

Designed for music identification, song discovery, and audio recognition scenarios.

---

## ✨ Features

- Singing recognition
- Audio file recognition
- High-accuracy song matching
- Real-time synchronous detection
- Multiple audio format support
- URL and file path input support

---

## 🚀 Usage

**Using audio file path:**
```bash
python {baseDir}/scripts/index.py "<audio_path>"
```

Examples:

```
python {baseDir}/scripts/index.py "humming.wav"
```

## 📋 Input Specification

### Audio Requirements

- Supported formats: MP3
- Sample rate: 16000Hz
- Audio encoding: lame
- Duration: 5-30 seconds recommended
- singing melody

---

## ⚠ Constraints

- Audio must contain clear melody
- API credentials must be configured
- Network connection required
- Synchronous processing - instant results
- Audio quality affects recognition accuracy

---

## 🔧 Environment Setup

Required:

- Python available in PATH
- Environment variables configured:

```bash
export XF_SONG_APP_ID=your_app_id
export XF_SONG_API_KEY=your_api_key
export XF_SONG_API_SECRET=your_api_secret
```

Or configure it in `~/.openclaw/openclaw.json`:

```json
{
	"env": {
		"XF_SONG_APP_ID": "your_app_id",
        "XF_SONG_API_KEY": "your_api_key",
		"XF_SONG_API_SECRET": "your_api_secret"
	}
}
```



---

## 📦 Output

Returns JSON response with:
- Song name
- Artist name
- Album information
- Confidence score
- Match details

---

## 🎯 Target Use Cases

- Music identification apps
- Song discovery platforms
- Karaoke applications
- Music education tools
- Audio content recognition
- Copyright detection
- Music search engines

---

## 🛠 Extensibility

Future enhancements may include:

- Batch audio processing
- Real-time streaming recognition
- Custom music library
- Multi-language song support
- Genre classification

---

Built for automation workflows and AI-driven music recognition.
