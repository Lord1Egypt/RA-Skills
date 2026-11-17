---
name: whatsapp-voice-note
description: "Send real WhatsApp VOICE NOTES (not audio files) from an OpenClaw agent. Use when the user asks the agent to 'send a voice message/note', reply by voice, or read something out loud to a chat. Pipeline: ElevenLabs (natural, multilingual incl. Hebrew) or macOS `say` (free fallback) -> ffmpeg opus/ogg -> `openclaw message send --media`. Requires ffmpeg; ElevenLabs key optional but strongly recommended for non-English."
metadata: { "openclaw": { "emoji": "🎙️" } }
---

# WhatsApp Voice Note

Turns text into a real WhatsApp **voice note** (the kind with the waveform, `ptt:true`) and
sends it through your OpenClaw WhatsApp channel. The plugin auto-sends any audio attachment
as a voice note; this skill hands it clean opus/ogg for best quality.

## Usage

```bash
./voice.sh --target +15555550100 --text "Hi, on my way."
./voice.sh --target +15555550100 --text-file /path/to/note.txt
./voice.sh --text "test" --out-only /tmp/note.ogg     # build the file, don't send
./voice.sh --target +15555550100 --text "hello" --dry-run
```

## Engines (auto-selected)

- **elevenlabs** — natural, multilingual. Used automatically when `ELEVENLABS_API_KEY` is
  set. Model is picked per language: most languages use `eleven_multilingual_v2`; Hebrew
  text auto-switches to `eleven_v3` (the only model that speaks it properly — learned the
  hard way).
- **say** — macOS built-in, free, robotic. Fallback when no key. Force either with
  `--engine elevenlabs|say`.

## Config (`.env` next to the script, or env vars)

```
ELEVENLABS_API_KEY=...            # enables the good engine
ELEVENLABS_VOICE_ID=...           # default: Daniel (male multilingual)
ELEVENLABS_MODEL=...              # override auto model pick (e.g. eleven_flash_v2_5 = ~half credits)
```

## Hard-won notes

- WhatsApp voice notes must be **opus in ogg, mono** — ffmpeg flags in the script are the
  ones that survive WhatsApp's transcoder without artifacts.
- Put a policy line in your agent's rules about WHO may receive voice notes. An agent that
  can voice-message anyone in your contacts is a liability, not a feature.
- `--out-only` is great for piping into other channels (Telegram, casting to a speaker).

---
*From the **Build Your Own Chief** starter kit — skills, configs, and gotchas from a real
24/7 household agent: https://chief.natalicot.com/kit/?utm=clawhub*
