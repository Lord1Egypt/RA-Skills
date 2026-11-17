---
name: smart-playlist-dj
description: 智慧情境 DJ，自動偵測心情/天氣/時段，生成最適合當下情境的播放列表並播放。支援 Morning/Work/Exercise/Sleep 等 10 種情境模式。
---

# 🎧 智慧播放列表 DJ（Smart Playlist DJ）

## 概述

根據**時間 + 天氣 + 心情**，自動為你生成最適合當下情境的播放列表。

**觸發關鍵字：** 放音樂、來點音樂、推薦歌、DJ、我想聽歌、現在聽什麼、天氣音樂、早安音樂、工作音樂、健身歌、睡覺前聽什麼

---

## 支援情境

| 情境 | 說明 |
|------|------|
| ☀️ morning | 晨間喚醒，能量充沛 |
| 🎯 work | 專注工作，心流狀態 |
| 💪 exercise | 健身打氣，高能量 |
| 🌿 relaxed | 晚間放鬆 |
| 🌙 sleepy | 睡前時光，平靜舒緩 |
| ☕ rainy | 雨天配咖啡，憂鬱浪漫 |
| 🎉 party | 派對嗨歌 |
| 💕 romantic | 浪漫時光 |
| 🚶 commute | 通勤陪伴 |
| ☕ cafe | 咖啡時光 |

---

## 腳本清單

| 腳本 | 用途 |
|------|------|
| `scripts/dj_main.py` | 主入口，一句話啟動完整 DJ 流程 |
| `scripts/mood_detector.py` | 情境偵測（時間+天氣+互動問答）|
| `scripts/playlist_generator.py` | 智能歌單生成（BPM評分+Genre+Rating）|
| `scripts/music_player.py` | Music.app 播放控制 |

---

## 環境要求

- **macOS**（使用 Music.app + osascript）
- 標準 Python 3，無需額外依賴

---

## 使用方式

```bash
# 最簡：一句話啟動（自動偵測情境）
python3 scripts/dj_main.py

# 指定情境
python3 scripts/dj_main.py work
python3 scripts/dj_main.py morning
python3 scripts/dj_main.py rainy

# 查看所有情境
python3 scripts/dj_main.py list

# 查看當前情境偵測
python3 scripts/mood_detector.py --json

# 生成歌單（不上播放）
python3 scripts/playlist_generator.py work -n 15

# 控制播放
python3 scripts/music_player.py play
python3 scripts/music_player.py next
python3 scripts/music_player.py vol 70
python3 scripts/music_player.py now

# TTS 朗讀歌單介紹（適合 Voice 命令）
python3 scripts/dj_main.py sleepy -j | jq -r '.tts_body'
```
