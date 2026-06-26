---
name: audio-transcribe
description: 语音转文字 Skill。使用本地 Whisper (openai-whisper) 将音频文件转录为文本、字幕(SRT)或 JSON。适用于会议记录、播客转录、语音备忘录等场景。触发方式：转写音频、转录语音、音频转文字、语音转文本、whisper、生成字幕。
---

# Audio Transcribe Skill

语音转文字，使用本地 Whisper 模型，完全离线、隐私安全。

## 前置条件

**安装 Whisper（只需一次）：**

```bash
# macOS
brew install whisper

# 或者 Python 包（更推荐，自动装模型）
pip3 install openai-whisper
```

## 使用方法

### 基本转录（中文音频）

当用户说"转录这个音频"时，运行：

```bash
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/audio.wav"
```

### 指定格式

```bash
# 输出 SRT 字幕
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/audio.wav" srt

# 输出 JSON（含时间戳）
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/audio.wav" json

# 指定语言
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/audio.wav" txt zh

# 英文音频
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/audio.wav" txt en
```

### 支持的格式

| 格式 | 说明 | 适用场景 |
|------|------|----------|
| `txt` | 纯文本（默认） | 快速阅读、存档 |
| `srt` | 字幕文件 | 视频压制、外语学习 |
| `json` | 结构化结果 | 二次处理、时间戳提取 |

### 支持的音频格式

`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.opus`, `.mp4`, `.mov` 等ffmpeg支持的格式

## 脚本参数

```
python3 transcribe.py <audio_file> [output_format] [language]

参数：
  audio_file      音频文件路径（必填）
  output_format   输出格式：txt, srt, json（默认: txt）
  language        语言代码：zh, en, ja, ko 等（默认: 自动检测）
```

## 注意事项

- **首次运行会下载模型**（~500MB），耐心等待
- 音频质量越高转录越准
- Whisper 模型可选：`tiny`, `base`, `small`, `medium`, `large`，默认 `base`
- 如果想换模型，修改脚本中 `whisper.load_model('base')` 为其他选项
- 长音频会自动分段处理