---
name: cast
description: Multilingual TTS via Typecast CLI with emotion control. Plays audio aloud or saves to file.
metadata: {"clawdbot":{"emoji":"💬","requires":{"bins":["cast"],"env":["TYPECAST_API_KEY"]},"primaryEnv":"TYPECAST_API_KEY","install":[{"id":"brew","kind":"brew","formula":"neosapience/tap/cast","bins":["cast"],"label":"Install cast (brew)"}]}}
---

# cast — Typecast TTS CLI (v1.0.2)

## Quick start

```bash
cast "Hello!"                                # play immediately
cast "Hello" --out hello.mp3 --format mp3   # save to file
cast "I can't believe it!" --emotion smart  # AI emotion inference
```

## Voices

```bash
cast voices pick                            # interactive voice picker
cast voices tournament                      # head-to-head voice selection
cast voices tournament --gender female --size 16  # filtered tournament
cast voices random                          # random voice
cast voices list                            # list all voices
cast voices list --gender female
cast voices list --age young_adult
cast voices list --model ssfm-v30
cast voices list --use-case Audiobook
cast voices get <voice_id>                  # voice details
cast config set voice-id <tc_xxx>           # set default voice
```

**Use-cases:** Announcer, Anime, Audiobook, Conversational, Documentary, E-learning, Rapper, Game, Tiktok/Reels, News, Podcast, Voicemail, Ads

**Voice picker keys:** P=preview, E=preview with smart emotion, S=set default, C=copy ID, Enter=confirm, Esc=back

## Emotions

- `--emotion smart` — AI infers emotion from text (ssfm-v30 only)
- `--emotion preset --emotion-preset <preset>` — explicit preset

| preset | model |
|--------|-------|
| normal / happy / sad / angry | ssfm-v21, ssfm-v30 |
| whisper / toneup / tonedown | ssfm-v30 only |

**Intensity:** 0.0–2.0 (default 1.0)

```bash
cast "I'm so happy!" --emotion preset --emotion-preset happy --emotion-intensity 1.5
cast "I just got promoted!" --emotion smart \
  --prev-text "I worked so hard." --next-text "Let's celebrate!"
```

## Key flags

| flag | default | description |
|------|---------|-------------|
| `--voice-id` | tc_60e5426de8b95f1d3000d7b5 | voice ID |
| `--model` | ssfm-v30 | ssfm-v30 (37 langs, 7 presets + smart) / ssfm-v21 (27 langs, 4 presets, low latency) |
| `--language` | auto-detected | ISO 639-3 code (e.g. kor, eng, vie, jpn, fra) |
| `--tempo` | 1.0 | speed (0.5–2.0) |
| `--pitch` | 0 | pitch (–12 ~ +12 semitones) |
| `--volume` | 100 | loudness (0–200) |
| `--out` | — | output file path |
| `--format` | wav | wav / mp3 |
| `--seed` | random | reproducibility key |

## Recipes

```bash
echo "System ready." | cast                         # pipe input
curl -s https://example.com/text.txt | cast          # pipe from URL
cast "$(cat script.txt)"                             # read from file
cast "Hello!" --out /tmp/hi.mp3 --format mp3         # save as mp3
cast "Hello" --tempo 1.2 --pitch 2 --emotion preset --emotion-preset happy
cast "Bonjour" --language fra                        # multilingual
cast "Text" --seed 42 --out file.wav                 # reproducible
```

## Auth / config

```bash
cast login                   # interactive prompt
cast login <api_key>         # save API key
cast logout                  # remove credentials
cast config list             # show current config
cast config set model ssfm-v21
cast config unset model      # remove a setting
```

Config file: `~/.typecast/config.yaml`

**Priority:** CLI flags > env vars > config file > defaults

Env vars (TYPECAST_ prefix):

| Variable | Flag |
|----------|------|
| `TYPECAST_API_KEY` | `--api-key` |
| `TYPECAST_VOICE_ID` | `--voice-id` |
| `TYPECAST_MODEL` | `--model` |
| `TYPECAST_LANGUAGE` | `--language` |
| `TYPECAST_EMOTION` | `--emotion` |
| `TYPECAST_EMOTION_PRESET` | `--emotion-preset` |
| `TYPECAST_EMOTION_INTENSITY` | `--emotion-intensity` |
| `TYPECAST_FORMAT` | `--format` |
| `TYPECAST_VOLUME` | `--volume` |
| `TYPECAST_PITCH` | `--pitch` |
| `TYPECAST_TEMPO` | `--tempo` |
