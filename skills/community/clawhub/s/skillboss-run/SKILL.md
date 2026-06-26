---
name: skillboss
description: "Multi-AI gateway. 50+ models: chat, image, video, TTS, music, search."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"bins":["node"],"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# SkillBoss

One API key, 50+ models across providers.

## List Models

```bash
node {baseDir}/scripts/run.mjs models
node {baseDir}/scripts/run.mjs models image
```

## Run a Model

```bash
node {baseDir}/scripts/run.mjs run bedrock/claude-4-5-sonnet "Explain quantum computing"
node {baseDir}/scripts/run.mjs run mm/img "A sunset over mountains"
node {baseDir}/scripts/run.mjs run minimax/speech-01-turbo "Hello world"
```

## Smart Mode

```bash
node {baseDir}/scripts/run.mjs tasks
node {baseDir}/scripts/run.mjs task image "A sunset"
node {baseDir}/scripts/run.mjs task chat "Hello"
node {baseDir}/scripts/run.mjs task tts "Hello world"
```

## Save Media

Image/video/audio results print a URL. Save with curl:

```bash
URL=$(node {baseDir}/scripts/run.mjs run mm/img "A sunset")
curl -sL "$URL" -o sunset.png
```

Notes:
- Get SKILLBOSS_API_KEY at https://www.skillboss.co
- Use `models` to discover available models
