---
name: Xiaomi-MiMo-V2-TTS
version: 2.0.0
description: |
  小米 MiMo V2 TTS 文字转语音模型（官网目前免费）。支持中文/英文，内置情感风格（开心/悲伤/生气）、角色扮演（孙悟空/林黛玉）、方言（东北话/四川话/粤语/河南话）、语速控制及唱歌能力。mp3/opus 格式可直接发送至微信/飞书。

  **配置（必需）**：在 `openclaw.json` 的 `skills.entries.Xiaomi-MiMo-V2-TTS.env.MIMO_API_KEY` 中设置 API Key。
category: audio-generation
tags:
  - tts
  - voice
  - audio
  - mimo
  - xiaomi
---

# 🎙️ MiMo TTS — 快速上手

小米 MiMo V2 TTS 语音合成，支持中文、英文及多种风格（情感、方言、角色扮演等）。

## ⚡ 快速开始

```bash
# 安装依赖
pip install requests && apt install ffmpeg

# 配置 API Key（在 openclaw.json 中添加）
# "skills.entries.Xiaomi-MiMo-V2-TTS.env.MIMO_API_KEY": "your-key"

# 合成语音
python3 /root/.openclaw/skills/mimo-tts/scripts/tts.py --text "你好，世界！" --output hello.wav
```

---

## 📌 必知参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--text` | ✅ | 要合成的文字（单条模式） |
| `--batch` | — | 批量模式：文本文件路径（每行一条） |
| `--output` | — | 输出路径，默认 `output.wav` |
| `--format` | — | 输出格式：`wav`(默认) / `mp3` / `pcm16` / `opus` |

## 🎨 风格与音色

### 音色

| voice 参数 | 说明 |
|-----------|------|
| `mimo_default` | MiMo-默认 |
| `default_zh` | 中文女声 |
| `default_en` | 英文女声 |

### 风格控制

> 💡 格式：`<style>风格1 风格2</style>待合成内容`（风格标签放文字**开头**）

| 类型 | 可用风格 |
|------|---------|
| 语速 | 变快、变慢 |
| 情绪 | 开心、悲伤、生气 |
| 方言 | 东北话、四川话、河南话、粤语 |
| 角色 | 孙悟空、林黛玉 |
| 风格 | 悄悄话、夹子音、台湾腔 |
| 其他 | 唱歌、叙事、讲故事 |

> ⚠️ **唱歌**必须在文本最开头加 `<style>唱歌</style>`

### 🎭 音频标签（细粒度控制）

在文本中插入音频标签，可精准控制停顿、呼吸、语速变化等：

```
（紧张，深呼吸）呼……冷静，冷静。不就是一个面试吗……（语速加快，碎碎念）
（极其疲惫，有气无力）师傅……到地方了叫我一声……
（提高音量喊话）大姐！这鱼新鲜着呢！
```

---

## 💬 常用示例

```bash
# 情感风格
python3 tts.py --text "明天就是周五了，真开心！" --style 开心 --output happy.wav

# 角色扮演
python3 tts.py --text "俺老孙来也！" --style 孙悟空 --output wukong.wav

# 方言
python3 tts.py --text "哎呀妈呀，这天儿也太冷了！" --style 东北话 --output dongbei.wav

# 英文
python3 tts.py --text "Hello world!" --voice default_en --output hello_en.wav

# 唱歌（必须加 <style>唱歌</style>）
python3 tts.py --text "<style>唱歌</style>原谅我这一生不羁放纵爱自由" --output song.wav

# 发微信/飞书 → 用 mp3 或 opus 格式
python3 tts.py --text "你好呀" --format opus --output hello.opus

# 多风格组合
python3 tts.py --text "好开心呀" --style "开心 四川话" --output happy_sichuan.opus

# 批量合成
python3 tts.py --batch texts.txt --output-dir ./voices --format opus
```

---

## 📋 参数完整列表

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text` | 要合成的文字 | — |
| `--batch` | 批量模式：文本文件路径 | — |
| `--output` | 输出文件路径 | `output.wav` |
| `--output-dir` | 输出目录（批量模式） | `./voices` |
| `--voice` | 音色 | `mimo_default` |
| `--style` | 语音风格（可多次指定组合） | — |
| `--format` | 输出格式 | `wav` |
| `--user-text` | 用户侧消息（辅助上下文） | — |

---

## ❌ 常见问题

| 问题 | 解决 |
|------|------|
| `未设置 MIMO_API_KEY` | 在 `openclaw.json` 的 `skills.entries.Xiaomi-MiMo-V2-TTS.env` 中配置 |
| API 返回异常 | Key 无效或过期 |
| `ImportError: requests` | `pip install requests` |
| `ffmpeg 未安装` | `apt install ffmpeg` |
| 唱歌风格无效 | 必须加 `<style>唱歌</style>` 在文本**最开头** |

---

## 🔧 技术细节

- **模型**：mimo-v2-tts
- **API**：`https://api.xiaomimimo.com/v1/chat/completions`
- **采样率**：24kHz
- **自动重试**：失败自动重试 3 次（间隔 2 秒）
- **风格标签**：` <style>风格</style>` 放在文字开头
