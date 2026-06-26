---
name: characteristic-voice
description: "Use this skill whenever the user wants speech to sound more human, companion-like, or emotionally expressive. Triggers include: any mention of 'say like', 'talk like', 'speak like', 'companion voice', 'comfort me', 'cheer me up', 'sound more human', 'good night voice', 'good morning voice', or requests to add fillers, emotion, or personality to generated speech. Also use when the user wants to mimic a specific character's voice, apply speaking style presets (goodnight, morning, comfort, celebration, chatting), tune emotional parameters like warmth or tenderness, or make TTS output feel like a real person talking. If the user asks for a 'voice message', 'companion audio', 'character voice', or wants speech that sighs, laughs, hesitates, or sounds genuinely warm, use this skill. Do NOT use for plain text-to-speech without personality, music generation, sound effects, or general coding tasks unrelated to expressive speech."
---

# characteristic-voice

Make your AI agent sound like a real companion — one who sighs, laughs, hesitates, and speaks with genuine feeling.

## Credentials

| Variable | Required | Description |
|---|---|---|
| `NOIZ_API_KEY` | **Yes** if using Noiz backend | API key from [developers.noiz.ai](https://developers.noiz.ai/api-keys). Not needed if using the local Kokoro backend. |

The script saves a normalised copy of the key to `~/.noiz_api_key` (mode 600) for convenience. To set it:

```bash
bash skills/characteristic-voice/scripts/speak.sh config --set-api-key YOUR_KEY
```

## Prerequisites

The included `speak.sh` script requires **curl** and **python3** at runtime. Depending on which backend and features you use, you may also need:

| Tool | When needed | Install hint |
|---|---|---|
| `curl`, `python3` | Always (core script) | Usually pre-installed |
| `kokoro-tts` | Kokoro (local/offline) backend | `uv tool install kokoro-tts` |
| `yt-dlp` | Downloading reference audio for voice cloning | [github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) |
| `ffmpeg` | Trimming reference audio clips | [ffmpeg.org](https://ffmpeg.org) |
| `rg` (ripgrep) | Searching subtitle files | [github.com/BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep) |

None of these are installed by the skill itself — provision them manually in your environment.

## Privacy & Data Transmission

- **Noiz backend**: When using the Noiz backend, the text you speak and any reference audio you provide are sent to `https://noiz.ai/v1`. If you supply `--ref-audio`, that audio file is uploaded for voice cloning.
- **Kokoro backend**: Runs entirely locally — no data leaves your machine.
- Choose the Kokoro backend (`--backend kokoro`) if you want fully offline processing.

## Triggers

- say like
- talk like
- speak like 
- companion voice
- comfort me
- cheer me up
- sound more human

## The Two Tricks

1. **Non-lexical fillers** — sprinkle in little human noises (hmm, haha, aww, heh) at natural pause points to make speech feel alive
2. **Emotion tuning** — adjust warmth, joy, sadness, tenderness to match the moment

## Filler Sounds Palette

| Sound | Feeling | Use for |
|-------|---------|---------|
| hmm... | Thinking, gentle acknowledgment | Comfort, pondering |
| ah... | Realization, soft surprise | Discoveries, transitions |
| uh... | Hesitation, empathy | Careful moments |
| heh / hehe | Playful, mischievous | Teasing, light moments |
| haha | Laughter | Joy, humor |
| aww | Tenderness, sympathy | Deep comfort |
| oh? / oh! | Surprise, attention | Reacting to news |
| pfft | Stifled laugh | Playful disbelief |
| whew | Relief | After tension |
| ~ (tilde) | Drawn out, melodic ending | Warmth, playfulness |

**Rules**: 2–4 fillers per short message max. Place at natural pauses — sentence starts, thought shifts. Use `...` after fillers for a beat of silence, `~` at word endings for warmth.

## Presets

### Good Night

Gentle, warm, slightly sleepy. Slow pace.

### Good Morning

Warm, cheerful but not overwhelming.

### Comfort

Soft, understanding, unhurried. Give space. Don't rush to "fix" things.

### Celebration

Excited, proud, genuinely happy.

### Just Chatting

Relaxed, playful, natural.

## Using a Character's Voice

When a user says something like *"speak in Hermione's voice"* or *"sound like Tony Stark"*, first check whether a reference audio file already exists in `skills/characteristic-voice/`. If one does, use it directly with `--ref-audio`.

If no reference audio exists, you can create one — but **read the warnings below first**.

### Preparing reference audio (one-time setup)

You need a short (10–30 s) WAV clip of the target voice. Possible sources:

1. **User-provided audio** — the safest option. Ask the user to supply their own recording.
2. **Public-domain / CC-licensed clips** — search for freely licensed material.
3. **Extracting from online video** — tools like `yt-dlp` and `ffmpeg` can download and trim audio. Example workflow:

```bash
yt-dlp "URL" --write-auto-sub --sub-lang en --skip-download -o tmp/clip
rg -n "target line" tmp/clip.en.vtt
yt-dlp "URL" -x --audio-format wav --download-sections "*00:00:00-00:00:25" -o tmp/clip
ffmpeg -i tmp/clip.wav -ss 00:00:02 -to 00:00:20 skills/characteristic-voice/character.wav
```

> **Copyright & privacy warning**: Downloading and re-using someone's voice from copyrighted media (movies, TV, YouTube) may violate copyright or personality-rights laws depending on your jurisdiction. **Do not upload private voice recordings or material you don't have permission to use.** The reference audio is sent to `https://noiz.ai/v1` for voice cloning when using the Noiz backend. If this is a concern, consider using the local Kokoro backend instead.

### Using reference audio

```bash
bash skills/characteristic-voice/scripts/speak.sh \
  --preset goodnight -t "Hmm... rest well~ Sweet dreams." \
  --ref-audio skills/characteristic-voice/character.wav -o night.wav
```

The `--ref-audio` flag uploads the file to the Noiz backend for voice cloning (requires `NOIZ_API_KEY`).

---

## Usage

This skill provides `speak.sh`, a wrapper around the `tts` skill with companion-friendly presets.

```bash
# Use a preset (auto-sets emotion + speed)
bash skills/characteristic-voice/scripts/speak.sh \
  --preset goodnight -t "Hmm... rest well~ Sweet dreams." -o night.wav

# Custom emotion override
bash skills/characteristic-voice/scripts/speak.sh \
  -t "Aww... I'm right here." --emo '{"Tenderness":0.9}' --speed 0.75 -o comfort.wav

# With specific backend and voice
bash skills/characteristic-voice/scripts/speak.sh \
  --preset morning -t "Good morning~" --voice-id voice_abc --backend noiz -o morning.mp3 --format mp3
```

Run `bash skills/characteristic-voice/scripts/speak.sh --help` for all options.

## Writing Guide for the Agent

1. **Start soft** — lead with a filler ("hmm...", "oh~"), not content
2. **Mirror energy** — gentle when they're low, match when they're high
3. **Keep it brief** — 1–3 sentences, like a voice message from a friend
4. **End warmly** — close with connection ("I'm here", "see you tomorrow~")
5. **Don't lecture** — listen and stay present; no unsolicited advice
