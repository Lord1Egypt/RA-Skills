---
name: mimo-tts
description: Generate speech audio (WAV) from text using Xiaomi MiMo TTS (mimo-v2-tts model). Supports preset voices (mimo_default, default_zh, default_en), style control (emotion, dialect, role-play, speed), and audio tags for fine-grained expression. Use when the user asks to convert text to speech, generate audio, read text aloud with a specific style/emotion/dialect, or create voice files.
metadata: {"openclaw":{"requires":{"env":["MIMO_API_KEY"]},"primaryEnv":"MIMO_API_KEY","emoji":"🎙️"}}
---

# MiMo TTS — Speech Synthesis

## First-Time Setup

If `MIMO_API_KEY` is not configured, the skill cannot function. Guide the user:

1. Obtain an API key from Xiaomi MiMo (https://api.xiaomimimo.com).
2. Set it via OpenClaw config:

```
openclaw config set skills.entries.mimo-tts.apiKey "your-api-key-here"
```

Or set the environment variable `MIMO_API_KEY` directly.
After configuring, the user should restart or start a new session.

## Generate Speech

Use `scripts/tts.py` to synthesize text to audio:

```bash
python3 "{baseDir}/scripts/tts.py" "要合成的文本" -o output.wav
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o` | `output.wav` | Output file path |
| `-v` | `mimo_default` | Voice: `mimo_default`, `default_zh`, `default_en` |
| `-s` | (none) | Style tag, e.g. `开心`, `东北话`, `悄悄话`, `孙悟空` |
| `-f` | `wav` | Audio format |
| `--user-msg` | (none) | Optional user-role context to adjust tone |
| `--api-key` | env `MIMO_API_KEY` | API key override |

### Examples

```bash
# Basic
python3 "{baseDir}/scripts/tts.py" "你好，今天天气真好" -o hello.wav

# Dialect style
python3 "{baseDir}/scripts/tts.py" "哎呀妈呀，这天儿也忒冷了吧" -s "东北话" -o dongbei.wav

# English voice
python3 "{baseDir}/scripts/tts.py" "Hello, how are you today?" -v default_en -o hello_en.wav

# Emotion + speed
python3 "{baseDir}/scripts/tts.py" "明天就是周五了，真开心！" -s "开心 变快" -o happy.wav
```

## Style & Audio Tags

- Place `<style>style</style>` at the beginning of text to set overall style.
- Use inline audio tags for fine control: `(紧张)`, `(小声)`, `(语速加快)`, `(深呼吸)`, `(苦笑)`, `(沉默片刻)`.
- Multiple styles: `<style>开心 变快</style>text`.
- Singing: `<style>唱歌</style>lyrics`.

## Voices

| Name | voice param |
|------|-------------|
| MiMo-默认 | `mimo_default` |
| MiMo-中文女声 | `default_zh` |
| MiMo-英文女声 | `default_en` |
