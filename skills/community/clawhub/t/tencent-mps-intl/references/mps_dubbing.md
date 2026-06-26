# Voice Synthesis & Voice Cloning Parameters & Examples — `mps_dubbing.py`

**Function**: AI voice synthesis and voice cloning, suitable for audiobooks, podcasts, audio/video dubbing, and similar scenarios.
Supports 40+ languages including Chinese, English, Japanese, Korean, and more. Can clone a real human voice or use built-in system voices.

> ⚠️ This script is responsible for **voice synthesis and voice cloning** only — it does not handle subtitles, watermarks, or other visual elements. For visual erasure, use `mps_erase.py`; for subtitle generation, use `mps_subtitle.py`.

## Operation Modes

| Mode | API | Description |
|------|-----|-------------|
| `clone` | SyncDubbing (sync) | Submit cloning audio, returns a VoiceId. Recommended audio length: 10–20 s, single speaker, clear speech |
| `tts` | SyncDubbing (sync) | Submit text + VoiceId, returns a synthesized WAV audio file. Text ≤ 2000 chars uses sync; beyond that the script **auto-switches** to `async-tts` |
| `async-tts` | ProcessMedia (async) | Long-text TTS — asynchronously synthesizes speech and writes output to COS |
| `async-sts` | ProcessMedia (async) | Speech-to-speech — replaces the voice in an input audio/video file, asynchronously writes output to COS |

## Parameter Description

### General Parameters

| Parameter | Description |
|-----------|-------------|
| `--mode` | Operation mode (required): `clone` / `tts` / `async-tts` / `async-sts` |
| `--voice-id` | Voice ID (system voice or custom VoiceId returned by `clone` mode). Used by `tts` / `async-tts` / `async-sts` |
| `--verbose` / `-v` | Output detailed information (includes full request parameters and response) |
| `--dry-run` | Print request parameters only; do not call the API |
| `--region` | MPS service region (reads `TENCENTCLOUD_API_REGION` env var first, default `ap-guangzhou`). Can be omitted in sync mode |

### Text Parameters (`tts` / `async-tts`)

| Parameter | Description |
|-----------|-------------|
| `--text` | Text to synthesize. In `tts` mode, ≤ 2000 chars uses sync; longer text auto-switches to async (no need to change `--mode` manually) |
| `--text-lang` | Text language (default `zh` for Chinese). E.g. `en` / `ja` / `ko` / `fr` |

### Clone Audio Parameters (`clone` sync mode)

| Parameter | Description |
|-----------|-------------|
| `--audio-file` | Local cloning audio file path (WAV / MP3 / MP4, etc. supported). Recommended: 10–20 s, single speaker, clear speech |
| `--audio-url` | Cloning audio URL (used when `--audio-file` is not provided) |
| `--audio-lang` | Language of the cloning audio (default `zh`) |
| `--time-ranges` | Time ranges to use for cloning, format `start,end` (seconds, e.g. `5.2,20`). Can be specified multiple times |

### Async Mode Clone Video Parameters (`async-tts` / `async-sts`)

| Parameter | Description |
|-----------|-------------|
| `--clone-video-url` | Video/audio URL to clone the voice from (must be ≥ 5 s, single speaker) |
| `--clone-video-lang` | Language of the cloning video/audio (default `zh`) |
| `--src-lang` | Language of the source video/audio (used by `async-sts`) |

### Async Task Input Source (`async-tts` / `async-sts`)

| Parameter | Description |
|-----------|-------------|
| `--url` | Input video/audio URL. `async-tts` can omit this (or use any accessible URL as a placeholder); `async-sts` requires a real URL |
| `--cos-input-bucket` | Input COS Bucket name (used together with `--cos-input-key`) |
| `--cos-input-region` | Input COS Bucket region |
| `--cos-input-key` | Input COS object Key (e.g. `/input/video.mp4`) |

### Audio Quality Parameters (optional)

| Parameter | Description |
|-----------|-------------|
| `--sample-rate` | Output sample rate. Supported values: `8000` / `16000` / `22050` / `32000` / `44100` (default `16000`). Not supported by `async-sts` |
| `--pitch` | Pitch adjustment, range `[-12, 12]`, default `0` (original pitch) |
| `--duration` | Target duration of synthesized audio (seconds, e.g. `5.2`). Sync mode only |

### Sync Task Output (`clone` / `tts`)

| Parameter | Description |
|-----------|-------------|
| `--output` / `-o` | Local path to save the synthesized audio (e.g. `/tmp/output.wav`). If not specified, auto-generates a filename and saves to the current directory |
| `--output-url` | Request the API to return an audio URL (valid for 24 hours) instead of base64 data |

### Async Task Output Configuration (`async-tts` / `async-sts`)

| Parameter | Description |
|-----------|-------------|
| `--output-bucket` | Output COS Bucket name (defaults to `TENCENTCLOUD_COS_BUCKET` env var) |
| `--output-region` | Output COS Bucket region (defaults to `TENCENTCLOUD_COS_REGION` env var) |
| `--output-dir` | Output directory (default `/output/dubbing/`), must start and end with `/` |
| `--output-pattern` | Output filename prefix; supports placeholders `{taskType}` and `{timestamp}` |
| `--no-wait` | Submit task only, do not wait for results (auto-polls until completion by default) |
| `--poll-interval` | Polling interval (seconds), default `10` |
| `--max-wait` | Maximum wait time (seconds), default `3600` (1 hour) |
| `--download-dir` | After async task completes, automatically download results to the specified local directory |
| `--notify-url` | Task completion callback URL (optional) |
| `--resource-id` | Resource ID (defaults to account's primary resource ID) |

## Supported Languages (`--text-lang` / `--audio-lang` / `--src-lang` / `--clone-video-lang`)

| Code | Language | Code | Language | Code | Language |
|------|----------|------|----------|------|----------|
| `zh` | Chinese | `en` | English | `ja` | Japanese |
| `ko` | Korean | `de` | German | `fr` | French |
| `es` | Spanish | `it` | Italian | `ru` | Russian |
| `pt` | Portuguese | `ar` | Arabic | `hi` | Hindi |
| `th` | Thai | `vi` | Vietnamese | `id` | Indonesian |
| `ms` | Malay | `tr` | Turkish | `nl` | Dutch |
| `pl` | Polish | `sv` | Swedish | `fi` | Finnish |
| `yue` | Cantonese | `he` | Hebrew | `fa` | Persian |

> Full list (40+ languages) available in the `SUPPORTED_LANGS` dict inside `mps_dubbing.py`.

## Mandatory Rules

> ⚠️ **Priority Note**: Rules are listed in descending priority order. When multiple rules apply simultaneously, **use the lower-numbered rule first**.

- **[Highest Priority — Mode Selection] Determine the task type first**:
  - ✅ Need to "obtain a VoiceId" → use `--mode clone`; **must** provide `--audio-file` or `--audio-url`
  - ✅ Need "short-text TTS (≤ 2000 chars)" → use `--mode tts`; **must** provide `--voice-id`
  - ✅ Need "long-text TTS (> 2000 chars)" → use `--mode tts` directly; the script **auto-switches** to async (do **not** manually specify `async-tts`)
  - ✅ Need "replace voice in an existing audio/video file" → use `--mode async-sts`; **must** provide `--url` or COS input, and **must** provide `--voice-id` or `--clone-video-url`

- **VoiceId must be the full encrypted base64 format**: correct format is similar to `v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/...` (~80+ characters). Truncated IDs from documentation examples (e.g. `s1_2GSzVAf00hl`) are **invalid** and will return `decode encrypt voiceId failed`. Always obtain the real VoiceId via `--mode clone` before use.

- **`async-tts` `--url` parameter must be an accessible link**: this parameter is only a placeholder (TextToSpeech does not depend on the input file content), but if the URL returns 404 the task will immediately fail. Recommended: use the URL of any existing file in your own COS bucket.

- **`--output-dir` must start and end with `/`**: required by the API. The script auto-appends a trailing `/`, but it is recommended to specify it explicitly, e.g. `--output-dir /output/dubbing/`.

- **Async mode requires a COS Bucket to be configured**: `async-tts` / `async-sts` write output to COS. The output bucket must be specified via `--output-bucket` or the `TENCENTCLOUD_COS_BUCKET` env var.

- **Async-only parameters must not be used in sync modes**: `--clone-video-url`, `--output-dir`, `--no-wait`, `--download-dir`, etc. will cause an error in `clone` / `tts` mode; they are only valid for `async-tts` / `async-sts`.

## Typical Workflows

```
1. Voice cloning workflow (clone first, then tts):
   clone → returns VoiceId → tts --voice-id <VoiceId>

2. Use a system voice directly:
   tts --voice-id <system-voice-id> --text "..."

3. Long-text synthesis (auto-switches to async):
   tts --text "Text longer than 2000 characters..." --voice-id <VoiceId>
   (script auto-switches to async-tts; no manual mode change needed)

4. Audio/video voice replacement:
   async-sts --url <video-URL> --voice-id <VoiceId>
```

## Example Commands

```bash
# ── Voice Cloning (clone) ─────────────────────────────────────────────────────

# Clone voice from a local audio file (recommended: 10–20 s, single speaker, clear speech)
python scripts/mps_dubbing.py --mode clone --audio-file /path/to/voice.wav

# Clone voice from an audio URL
python scripts/mps_dubbing.py --mode clone --audio-url https://example.com/voice.wav

# Clone voice from an audio URL, specifying the audio language
python scripts/mps_dubbing.py --mode clone \
    --audio-url https://example.com/voice.mp4 --audio-lang en

# ── Short-text TTS (tts) ──────────────────────────────────────────────────────

# Minimal call (using a system voice)
python scripts/mps_dubbing.py --mode tts \
    --text "Hello, welcome to Tencent Cloud voice synthesis!" \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..."

# Specify output file path
python scripts/mps_dubbing.py --mode tts \
    --text "Hello, welcome!" \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --output /tmp/output.wav

# Adjust sample rate and pitch
python scripts/mps_dubbing.py --mode tts \
    --text "Hello" \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --sample-rate 44100 --pitch 2 --output /tmp/out.wav

# English synthesis
python scripts/mps_dubbing.py --mode tts \
    --text "Artificial intelligence changes the world." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --text-lang en

# Long text auto-switches to async (no need to change --mode)
python scripts/mps_dubbing.py --mode tts \
    --text "This is a very long text exceeding 2000 characters..." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --download-dir ./output/

# ── Clone voice then synthesize ───────────────────────────────────────────────

# Step 1: Clone voice — note the returned VoiceId
python scripts/mps_dubbing.py --mode clone --audio-file voice.wav

# Step 2: Synthesize speech using the obtained VoiceId
python scripts/mps_dubbing.py --mode tts \
    --text "Hello, this is the cloned voice." \
    --voice-id "v1_<VoiceId from previous step>"

# ── Long-text TTS (async-tts) ─────────────────────────────────────────────────

# Specify VoiceId, write output to COS, then download locally after completion
python scripts/mps_dubbing.py --mode async-tts \
    --text "This is a long text, suitable for async processing..." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --url "https://<bucket>.cos.ap-guangzhou.myqcloud.com/input/placeholder.wav" \
    --output-dir /output/tts/ \
    --download-dir ./output/

# Use a COS file as input, clone voice from video
python scripts/mps_dubbing.py --mode async-tts \
    --text "Long text..." \
    --clone-video-url https://example.com/train.mp4 \
    --cos-input-key /input/placeholder.wav \
    --output-dir /output/tts/

# Submit task only, do not wait (query manually later)
python scripts/mps_dubbing.py --mode async-tts \
    --text "Long text..." \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --url "https://example.com/any_accessible.mp4" \
    --no-wait

# ── Speech-to-Speech (async-sts) ──────────────────────────────────────────────

# Replace voice in a video using a specified VoiceId
python scripts/mps_dubbing.py --mode async-sts \
    --url https://example.com/video.mp4 \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --output-dir /output/sts/ \
    --download-dir ./output/

# Replace voice in a video by cloning from a reference video on the fly
python scripts/mps_dubbing.py --mode async-sts \
    --url https://example.com/video.mp4 \
    --clone-video-url https://example.com/train.mp4 \
    --output-dir /output/sts/

# Use COS input file
python scripts/mps_dubbing.py --mode async-sts \
    --cos-input-key /input/video.mp4 \
    --voice-id "v1_Pi1pR9Q9UHqVOrQ0YpZFwL+Q/..." \
    --output-dir /output/sts/ \
    --download-dir ./output/

# ── Other ─────────────────────────────────────────────────────────────────────

# Query existing task results
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --verbose

# Query task and download results locally
python scripts/mps_get_video_task.py --task-id 2600011633-WorkflowTask-xxxxx --download-dir ./output/

# Dry run (print request parameters only, do not call the API)
python scripts/mps_dubbing.py --mode tts \
    --text "Hello" --voice-id "v1_xxx..." --dry-run
```
