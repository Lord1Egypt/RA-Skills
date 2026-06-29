---
name: telegram-voice-stt
description: "Transcribe Telegram voice notes to text before the assistant replies. Use when the user sends a voice message on Telegram (@AadiAssistantbot), or mentions voice note, speech to text, STT, audio to text, or whisper on Telegram. OpenClaw auto-transcribes inbound .ogg voice files; treat the transcript as the user's question and answer it directly."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎙️"
    os: ["win32"]
    requires:
      env:
        - GOOGLE_APPLICATION_CREDENTIALS
        - GOOGLE_CLOUD_PROJECT
    primaryEnv: GOOGLE_APPLICATION_CREDENTIALS
---

# Telegram Voice → Text (STT)

When a user sends a **voice note** on Telegram, OpenClaw transcribes it **before** the model runs.

## How it works

1. Telegram delivers `.ogg` voice file to `.openclaw/media/inbound/`
2. Gateway runs `transcribe-audio-cli.js` (Google Cloud Speech-to-Text)
3. Transcript replaces `<media:audio>` in the user message
4. Optional echo: user sees `📝 Heard: "..."` in Telegram
5. Assistant answers the transcribed text via Bifrost → genapp-proxy → Dialogflow

## Rules for the assistant

- **Never** say "I cannot process audio" if a transcript is present
- Reply to the **transcript content** as the user's actual question
- For Hindi/English mix, answer in the language the user spoke or ask which they prefer
- If transcription is empty, ask the user to type their message or re-record

## Stack

- OpenClaw: `tools.media.audio` CLI model → `~/.openclaw/gcp/transcribe-audio-cli.js`
- Fallback: genapp-proxy also transcribes voice before Dialogflow (8192 token limit)

## Manual test (gateway machine)

```powershell
node "$env:USERPROFILE\.openclaw\gcp\transcribe-audio-cli.js" "C:\path\to\voice.ogg"
```
