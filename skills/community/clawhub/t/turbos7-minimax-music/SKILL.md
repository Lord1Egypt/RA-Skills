---
name: minimax-music
description: MiniMax 音乐创作技能。集成歌词生成与音乐生成，支持完整歌曲创作流程。触发场景：(1) 用户请求创作歌词或生成歌曲，(2) 用户提供主题或歌词生成完整音乐，(3) 用户想要歌词和音乐一站式生成，(4) 用户想要续写或编辑歌词，(5) 用户想要生成纯音乐或翻唱版本。支持端点：歌词生成 `/v1/lyrics_generation`，音乐生成 `/v1/music_generation`。支持模型：music-2.6（推荐）、music-cover（翻唱）、music-2.6-free、music-cover-free。
---

# MiniMax 音乐创作技能

## 功能概览

| 功能 | API 端点 | 说明 |
|------|----------|------|
| 歌词生成 | `/v1/lyrics_generation` | 创作完整歌词或编辑/续写 |
| 音乐生成 | `/v1/music_generation` | 基于歌词生成完整歌曲 |

## 工作流程

### 一站式创作

```
主题/风格 → 歌词生成 → 保存歌词(.txt) → 音乐生成 → 保存音频 → 完整歌曲
```

1. **收集需求**：确定歌曲主题、风格、是否指定标题
2. **生成歌词**：调用 `/v1/lyrics_generation`
3. **保存歌词**：自动保存为 `.txt` 文件
4. **生成音乐**：将歌词与描述传入 `/v1/music_generation`
5. **保存音频**：自动下载到本地
6. **返回结果**：返回歌名、歌词路径、音频路径

## 输出目录

- 歌词：`~/.openclaw/workspace/assets/music/lyrics/`
- 音频：`~/.openclaw/workspace/assets/music/`

### 文件命名

- 歌词：`{歌曲名}_{timestamp}.txt`
- 音频：`{歌曲名}_{timestamp}.mp3`

## 快速开始

### 一站式创作歌曲

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

# 生成歌词
lyrics_response = requests.post(
    "https://api.minimaxi.com/v1/lyrics_generation",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "mode": "write_full_song",
        "prompt": "一首关于夏日星空的浪漫抒情歌曲"
    }
)

lyrics_result = lyrics_response.json()
song_title = lyrics_result["song_title"]
style_tags = lyrics_result["style_tags"]
lyrics = lyrics_result["lyrics"]

# 保存歌词
lyrics_dir = os.path.expanduser("~/.openclaw/workspace/assets/music/lyrics")
os.makedirs(lyrics_dir, exist_ok=True)
lyrics_path = os.path.join(lyrics_dir, f"{song_title}.txt")
with open(lyrics_path, 'w', encoding='utf-8') as f:
    f.write(f"# {song_title}\n# 风格: {style_tags}\n\n{lyrics}")

# 生成音乐
music_response = requests.post(
    "https://api.minimaxi.com/v1/music_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "music-2.6",
        "prompt": f"{style_tags}",
        "lyrics": lyrics,
        "output_format": "url"
    }
)

music_result = music_response.json()
audio_url = music_result["data"]["audio"]

# 下载音频
audio_dir = os.path.expanduser("~/.openclaw/workspace/assets/music")
audio_path = os.path.join(audio_dir, f"{song_title}.mp3")
audio_resp = requests.get(audio_url)
with open(audio_path, 'wb') as f:
    f.write(audio_resp.content)

print(f"歌词: {lyrics_path}")
print(f"音频: {audio_path}")
```

## 歌词生成参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mode` | string | 是 | `write_full_song` 或 `edit` |
| `prompt` | string | 否 | 歌曲主题/风格，最长 2000 字符 |
| `lyrics` | string | 否 | 现有歌词（edit 模式用） |
| `title` | string | 否 | 指定歌曲标题 |

### 支持的结构标签

`[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Hook]`, `[Drop]`, `[Bridge]`, `[Solo]`, `[Build-up]`, `[Instrumental]`, `[Breakdown]`, `[Break]`, `[Interlude]`, `[Outro]`

## 音乐生成参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称 |
| `prompt` | string | 是* | 音乐描述（纯音乐必填） |
| `lyrics` | string | 是* | 歌词（非纯音乐必填） |
| `is_instrumental` | boolean | 否 | 是否生成纯音乐 |
| `audio_url` | string | 否 | 参考音频（翻唱用） |
| `output_format` | string | 否 | `url` 或 `hex` |

### 支持的模型

| 模型 | 说明 | 适用场景 |
|------|------|----------|
| `music-2.6` | 文本生成音乐（推荐） | Token Plan/付费用户 |
| `music-cover` | 基于参考音频生成翻唱 | Token Plan/付费用户 |
| `music-2.6-free` | 限免版 | 所有用户 |
| `music-cover-free` | 翻唱限免版 | 所有用户 |

### 音频设置

| 参数 | 可选值 |
|------|--------|
| `sample_rate` | 16000, 24000, 32000, 44100 |
| `bitrate` | 32000, 64000, 128000, 256000 |
| `format` | mp3, wav, pcm |

## 脚本工具

- `scripts/generate_lyrics.py` - 歌词生成工具（自动保存 .txt）
- `scripts/generate_music.py` - 音乐生成工具（自动保存音频）
- `scripts/create_song.py` - 一站式创作（歌词+音乐，自动保存两者）

### 命令行用法

```bash
# 一站式创作
python create_song.py "一首关于星空的歌"

# 仅生成歌词
python generate_lyrics.py "一首关于星空的歌" --title "星空之梦"

# 仅生成音乐（需提供歌词）
python generate_music.py "流行音乐,欢快" --lyrics "$(cat lyrics.txt)"
```

## API 参考

- [references/lyrics-api.md](references/lyrics-api.md) - 歌词生成 API
- [references/music-api.md](references/music-api.md) - 音乐生成 API
