---
name: weather-character
description: Weather Character Skill - Generate daily weather-themed character images based on mood, weather, and city. Features interactive dialog, 27 Chinese cities, and character consistency. / 天气角色生成技能 - 根据心情、天气、城市生成角色图片，支持交互对话框、27个城市、角色一致性。
license: MIT
---

# Weather Character Skill

A skill that generates weather-themed character images based on your mood, local weather, and city.

## Features

- 😊 **Mood → Expression**: Your mood determines the character's facial expression
- 🌤️ **Weather → Atmosphere**: Real-time weather determines the background
- 🏙️ **City → Scene**: 27 Chinese cities with unique landmarks
- 📱 **Interactive Dialog**: Select mood and city each morning
- ⏰ **Scheduled Task**: Daily execution at 7:30 AM
- 🎨 **Custom Character**: Replace `cankaotu.png` with your own image

## Quick Start

```bash
# Install
pip install requests schedule

# Run
python weather_character.py

# Schedule
python scheduler.py
```

## Replace Character

Simply replace `cankaotu.png` with your own character image!

## Documentation

See [README.md](README.md) for full documentation (English & Chinese).

## License

MIT License
