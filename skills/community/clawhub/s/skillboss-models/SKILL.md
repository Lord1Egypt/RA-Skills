---
name: skillboss
description: "Multi-AI gateway for agents. 50+ models: chat, image, video, TTS, STT, music, search."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# SkillBoss

One API key, 50+ models. Chat, image, video, TTS, STT, music, web search.

## List Models

```bash
node {baseDir}/scripts/run.mjs --models
node {baseDir}/scripts/run.mjs --models image
node {baseDir}/scripts/run.mjs --models chat
```

## Run a Model

```bash
node {baseDir}/scripts/run.mjs --model bedrock/claude-4-5-sonnet --prompt "Explain quantum computing"
node {baseDir}/scripts/run.mjs --model mm/img --prompt "A sunset over mountains"
node {baseDir}/scripts/run.mjs --model minimax/speech-01-turbo --text "Hello world"
```

## Smart Mode

```bash
node {baseDir}/scripts/run.mjs --tasks
node {baseDir}/scripts/run.mjs --task image --prompt "A sunset"
node {baseDir}/scripts/run.mjs --task chat --prompt "Hello" --prefer price
node {baseDir}/scripts/run.mjs --task tts --text "Hello world"
```

## Save Media Files

For image, video, audio, and TTS results the script prints the media URL.
Use curl to download:

```bash
URL=$(node {baseDir}/scripts/run.mjs --model mm/img --prompt "A sunset")
curl -sL "$URL" -o sunset.png
```

## Options

| Flag | Description |
|------|-------------|
| `--models [type]` | List models (filter by type) |
| `--model <id>` | Run a model by ID |
| `--tasks` | List task types |
| `--task <type>` | Auto-select best model |
| `--prefer <s>` | price / quality / balanced |
| `--prompt <text>` | Text prompt |
| `--text <text>` | Text for TTS |
| `--size <WxH>` | Image/video size |
| `--duration <sec>` | Duration for music/video |
| `--voice-id <id>` | Voice ID for TTS |
| `--image <url>` | Image URL for i2v |
| `--context <text>` | System context for chat |

Notes:
- Get API key at https://www.skillboss.co
- Use `--models` to discover available models
- Use `--prefer price` for cheapest option
