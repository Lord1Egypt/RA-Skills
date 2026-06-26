---
name: voice-clone-tts
description: Voice cloning and TTS using MiniMax API. User must provide a voice name when cloning; after success, voice_name->voice_id is written back to this skill doc for reuse.
install: instruction-only; Python script requires Python 3.7+ and dependencies in requirements.txt (see Install section).
requiredEnv:
  - MINIMAX_API_KEY
optionalEnv:
  - MINIMAX_KEY
  - MINIMAX_GROUP_API_KEY
envNote: At least one of MINIMAX_API_KEY, MINIMAX_KEY, or MINIMAX_GROUP_API_KEY must be set for API auth.
---

# Voice Clone + TTS

## Scope

This skill is narrowly scoped to: (1) uploading clone audio to MiniMax, (2) creating a cloned voice, (3) TTS with cloned or existing voices, and (4) updating the cloned-voice mapping block in this `SKILL.md`. The script only reads/writes this skill’s `SKILL.md`; it does not read unrelated system files or other environment variables beyond the MiniMax API key(s) above.

## When to Use

- Use this skill when you need to clone user-provided audio into a reusable voice.
- Use this skill when you need text-to-speech (TTS) with an already cloned voice.
- For long-term maintenance, cloned results are written back to this file to reduce repeated setup.

## API Reference (MiniMax)

- Upload clone audio: `POST /v1/files/upload`, `purpose=voice_clone`, `multipart/form-data`.
- Create cloned voice: `POST /v1/voice_clone`.
- Speech synthesis: `POST /v1/t2a_v2`.
- Audio requirements: `mp3/m4a/wav`, duration `10 seconds–5 minutes`, file size `<=20MB`.

## Install

- **Runtime:** Python 3.7+.
- **Dependencies:** The script uses the `requests` library. Install with:
  ```bash
  pip install -r requirements.txt
  ```
  or `pip install requests`.
- **Network:** The script calls MiniMax APIs over HTTPS; it does not read unrelated system files. It only reads/writes this skill’s `SKILL.md` to update the cloned-voice mapping block.

## Required environment variables (credentials)

At least **one** of the following must be set for MiniMax API authentication (see frontmatter `requiredEnv` / `optionalEnv`):

| Variable | Required | Notes |
|----------|----------|--------|
| `MINIMAX_API_KEY` | preferred | Primary API key |
| `MINIMAX_KEY` | alternative | Accepted if set |
| `MINIMAX_GROUP_API_KEY` | alternative | Accepted if set |

The script will fail with a clear error if none are set.

## Prerequisites

1. **Credentials:** Set one of the env vars above (see “Required environment variables”).
2. Prepare clone audio (format/duration/size limits above).
3. **Before cloning, confirm the voice name (voice_name) with the user**, e.g. `liuyang_narration_v1`.

## Usage

1. Go to the skill directory: `cd workspace/skills/voice-clone-tts`
2. Run the script (clone + synthesize):

```bash
python scripts/minimax_voice_clone_tts.py \
  --audio "/absolute/path/to/voice.wav" \
  --voice-name "yangtuo_demo_v1" \
  --display-name "Alpaca Demo" \
  --text "Hello, this is a cloned voice test." \
  --output "./output/voice_test.mp3"
```

3. To clone only (no synthesis), omit `--text`.
4. To synthesize only (by display name or voice_id):

```bash
# Resolve by display name
python scripts/minimax_voice_clone_tts.py \
  --voice "voice_v2" \
  --text "This is TTS using an existing cloned voice." \
  --output "./output/reuse_voice.mp3"

# Or specify voice_id directly
python scripts/minimax_voice_clone_tts.py \
  --voice-id "yangtuo_demo_v1" \
  --text "This is TTS using an existing cloned voice." \
  --output "./output/reuse_voice.mp3"
```

## Common Options

- `--audio`: Path to clone audio (required for cloning).
- `--voice-name`: Required when cloning; API voice ID (letters, digits, underscores, e.g. `yangtuo_demo_v1`).
- `--display-name`: Optional when cloning; **display name** written to SKILL (e.g. `Alpaca Demo`). Defaults to `--voice-name` if omitted.
- `--voice-id`: For synthesis, specify API voice_id directly (skips mapping table).
- `--voice`: For synthesis, specify **display name or voice_id**; resolved from the mapping table below (e.g. `voice_v2` or `yangtuo_demo_v1`).
- `--text`: Text to synthesize (omit for clone-only).
- `--output`: Output audio path (default `./output/minimax_tts.mp3`).
- `--model`: Speech model (default `speech-2.8-turbo`).
- `--format`: Output format (`mp3/pcm/flac/wav`).
- `--speed --vol --pitch --emotion`: Speech expression parameters.

## Write-Back (Important)

- After a successful clone, the script writes **display name → voice_id** to the “Cloned Voice Mapping” section below.
- Use a display name with `--voice "display name"` so you don't need to remember voice_id.

## Cloned Voice Mapping

- Left: **display name**; right: API **voice_id**. For TTS use `--voice "display name"` or `--voice-id voice_id`.

<!-- CLONED_VOICES:START -->
- `test_voice_1772187110`: `test_voice_1772187110` (updated: 2026-02-27 18:12:00)
- `voice_v1`: `shuangyue_test` (updated: 2026-02-28 16:47:01)
- `voice_v2`: `yangtuo_demo_v1` (updated: 2026-02-27 18:19:39)
- `voice_v3`: `dong_yuhui_voice_v1` (updated: 2026-03-02 19:51:44)
<!-- CLONED_VOICES:END -->

## Troubleshooting

- 401 / auth failure: Check that `MINIMAX_API_KEY` is correct.
- Parameter errors: Check `voice_name` rules, audio format/size, and text length.
- Clone succeeded but not written back: Ensure `SKILL.md` exists and contains the write-back marker block.
