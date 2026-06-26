---
name: short-drama-publisher
version: 1.0.0
description: >
  Automated short drama video publisher. Downloads drama content from MoboBoost,
  uses AI to identify highlight moments, clips 15-second vertical videos with 
  text overlays, and auto-publishes to Facebook. Strawberry TV workflow clone.
  Triggers: "短剧发布", "short drama", "MoboBoost", "video publisher",
  "自动发布", "剪辑短剧".
tags: [video, automation, short-drama, facebook, social-media, content, publisher, chinese]
env:
  MOBOBOOST_COOKIES: "MoboBoost login cookies (JSON format, exported from browser)"
  FACEBOOK_COOKIES: "Facebook login cookies (JSON format, exported from browser)"
requires:
  - ffmpeg
  - python3
  - playwright
---

# Short Drama Publisher (短剧自动化发布)

Automated short drama promotion video workflow, inspired by **Strawberry TV** model:

1. 📥 Download drama content from MoboBoost
2. 🎯 AI-powered highlight detection (scene changes, audio peaks, subtitle emotion)
3. ✂️ Clip 15-second vertical videos with white English title overlay
4. 📤 Auto-publish to Facebook

---

## Prerequisites

### System Dependencies
```bash
# macOS
brew install ffmpeg

# Python dependencies
pip install playwright opencv-python librosa numpy pyyaml
playwright install chromium
```

### Credentials Setup

1. **MoboBoost Cookies**
   - Login to https://ckoc.cdreader.com
   - Export cookies using browser extension (e.g., "EditThisCookie")
   - Save as `config/moboboost_cookies.json`

2. **Facebook Cookies**
   - Login to Facebook
   - Export cookies using browser extension
   - Save as `config/facebook_cookies.json`

---

## Usage

### Full Automated Workflow
```bash
python scripts/daily_workflow.py
```

### Individual Modules

**Download content:**
```bash
python scripts/moboboost_downloader.py --drama-code 613815
```

**Detect highlights:**
```bash
python scripts/highlight_detector.py --input data/downloads/video.mp4
```

**Clip video:**
```bash
python scripts/video_editor.py --input video.mp4 --start 01:23 --title "Drama Name"
```

**Publish to Facebook:**
```bash
python scripts/facebook_publisher.py --video data/outputs/clip.mp4 --drama-code 613815 --drama-name "DramaName"
```

### Daily Cron Job
```bash
# Run daily at 9am
0 9 * * * cd /path/to/short-drama-publisher && python scripts/daily_workflow.py >> logs/cron.log 2>&1
```

---

## Configuration

### settings.yaml
```yaml
# Video settings
video:
  duration: 15          # Clip duration (seconds)
  width: 1080           # Width
  height: 1920          # Height (9:16 vertical)

# Text overlay settings
text_overlay:
  font: "Arial-Bold"
  size_ratio: 0.05      # Font size as ratio of video width
  color: "#FFFFFF"
  border_color: "#000000"
  border_width: 2
  position_y: 0.75      # Vertical position (ratio from top)

# AI highlight detection weights
highlight_weights:
  scene_change: 0.30
  audio_peak: 0.25
  subtitle_emotion: 0.25
  motion_intensity: 0.20

# Publishing settings
publishing:
  videos_per_day: 3     # Number of videos per day
  interval_minutes: 120 # Interval between posts (minutes)
```

---

## Directory Structure

```
short-drama-publisher/
├── SKILL.md                    # This file
├── config/
│   ├── settings.yaml           # Configuration
│   ├── moboboost_cookies.json  # MoboBoost credentials
│   └── facebook_cookies.json   # Facebook credentials
├── scripts/
│   ├── moboboost_downloader.py # Content downloader
│   ├── highlight_detector.py   # AI highlight detection
│   ├── video_editor.py         # Video clipping
│   ├── facebook_publisher.py   # Facebook publisher
│   └── daily_workflow.py       # Main workflow
├── data/
│   ├── downloads/              # Raw downloaded content
│   ├── outputs/                # Clipped videos
│   └── history.json            # Publishing history
├── fonts/                      # Font files
└── logs/                       # Log files
```

---

## AI Highlight Detection

The highlight detector uses multiple signals to find the most engaging moments:

| Signal | Weight | Method |
|--------|--------|--------|
| Scene Change | 30% | OpenCV frame-by-frame difference analysis |
| Audio Peak | 25% | Librosa audio amplitude analysis |
| Subtitle Emotion | 25% | Text sentiment analysis on subtitles |
| Motion Intensity | 20% | Optical flow magnitude calculation |

Each frame gets a composite score, and the highest-scoring 15-second segment is selected.

---

## Important Notes

> [!WARNING]
> - MoboBoost and Facebook websites may update, requiring script adjustments
> - Recommend 1-3 videos per day to simulate organic posting rhythm
> - Ensure you have rights to use MoboBoost content for promotion
> - Cookie-based auth may expire; re-export periodically
