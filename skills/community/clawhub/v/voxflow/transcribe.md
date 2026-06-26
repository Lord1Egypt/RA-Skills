
# VoxFlow Transcribe / Dub / Translate Skill

Audio/video → text → other languages → re-voiced video. Five tightly-related commands:

| Command | What it does | Output |
|---|---|---|
| `asr` (alias `transcribe`) | Audio/video → text. Cloud (Tencent), local (Whisper), or **Azure Batch** for 30-min+ files. | SRT / TXT / JSON |
| `asr-jobs` | Browse, inspect, cancel, or download long-running Azure jobs | list / show / cancel / download |
| `translate` | Translate SRT / text / file | SRT / TXT |
| `dub` | SRT → timeline-aligned TTS, optionally merged into video | WAV / MP4 |
| `video-translate` | End-to-end: ASR → translate → dub → merge MP4 | MP4 in target language |
| `summarize` | Audio/video/text → summary slides (PPTX, optional video) | PPTX / MP4 |

## Prerequisites

- `npm install -g voxflow` and `voxflow login`
- `ffmpeg` installed (`brew install ffmpeg` / `sudo apt install ffmpeg`) — required for `dub --video`, `video-translate`, audio extraction
- Optional: `whisper.cpp` for local engine (no quota cost). Install via `brew install whisper-cpp` or compile from source.
- Optional: `sox` / `rec` for `--mic` recording.


## 🎙 asr — speech recognition

Transcribe a local file, remote URL, or live mic input. Cloud (Tencent ASR) or local (Whisper).

### Quick start

```bash
voxflow asr --input recording.mp3                                        # default cloud, zh
voxflow asr --input meeting.wav --speakers --speaker-number 3            # speaker diarization
voxflow asr --input video.mp4 --format srt --lang 16k_zh -o out.srt     # video → SRT
voxflow asr --input recording.mp3 --engine local --model small           # offline Whisper
voxflow asr --url https://example.com/audio.mp3                          # remote URL
voxflow asr --mic --lang 16k_en                                          # live mic
```

### Engines

| `--engine` | Backend | Cost | When |
|---|---|---|---|
| `auto` *(default)* | Whisper local if installed, else Tencent cloud | API or free | Default |
| `cloud` | Tencent ASR | per call | ≤2-hour files, fast turnaround |
| `local` | whisper.cpp | Free | No quota, offline, slower |
| `azure` | **Azure Speech Batch (R2-uploaded)** | 150 / min, ceil to next minute | **30-min+ recordings, word-level timestamps, speaker diarization, multi-locale auto-detect** |

#### Azure path (durable jobs)

The `azure` engine is the right choice when a file would time out on Tencent's flash mode (anything over ~2 hours, or anything you want word-level timestamps on). The CLI:

1. Probes duration with `ffprobe`.
2. Extracts to 16 kHz mono WAV with `ffmpeg` to save uplink bandwidth (falls through to original file if `ffmpeg` is missing).
3. Uploads to Cloudflare R2 via backend-signed URLs (multipart for files >100 MiB).
4. Creates an `asr_jobs` row server-side, charges quota (per audio minute, see below), submits to Azure.
5. Polls the backend until terminal state.

**Ctrl+C is safe** — the server-side job keeps running and `~/.config/voxflow/jobs/asr-<jobId>.json` lets you resume later via `--job-id <uuid>` or `voxflow asr-jobs show <jobId>`. Quota is automatically refunded on failure or cancel.

```bash
# 30-min Japanese meeting with speaker diarization → word-timed SRT
voxflow asr --input meeting-2h.mp4 --engine azure --lang ja-JP --diarize --speaker-number 4 --format srt

# Auto-detect language across the four Azure default candidates (en/zh/ja/ko)
voxflow asr --input multilang.mp3 --engine azure --lang auto

# Resume a job after closing the terminal
voxflow asr --engine azure --job-id 6f3c2798-87bf-4367-bb4c-08b872e12bef
```

> **Language codes**: Azure uses BCP-47 (`ja-JP`, `zh-CN`, `en-US`, `ko-KR`). Tencent codes (`16k_zh`, `16k_ja`, …) are auto-mapped, so you can keep `--lang 16k_zh` working across engines.

### Modes (cloud only)

| `--mode` | Use |
|---|---|
| `auto` *(default)* | Picks based on duration |
| `sentence` | <60s clips, lowest latency |
| `flash` | 1-min to ~30 min, fast batch |
| `file` | Long files, async with polling, supports diarization |

### Options

| Flag | Default | Notes |
|---|---|---|
| `--input <file>` / `--url <url>` / `--mic` | one required | input source. azure engine: `--input` only |
| `--engine` | `auto` | `auto` \| `cloud` \| `local` \| `azure` |
| `--model` | `base` | local Whisper: `tiny` \| `base` \| `small` \| `medium` \| `large` |
| `--mode` | `auto` | cloud (Tencent) only — see modes above |
| `--lang` | `16k_zh` | Tencent: `16k_zh`, `16k_en`, `16k_zh_en`, `16k_ja`, `16k_ko`. Azure: `auto`, `ja-JP`, `zh-CN`, `en-US`, … (BCP-47) |
| `--format` | `srt` | `srt` \| `txt` \| `json` |
| `--speakers` / `--diarize` | false | Speaker diarization — cloud (`flash`/`file`) and azure |
| `--speaker-number <n>` | — | Hint expected speaker count |
| `--task-id <id>` | — | Resume polling a Tencent async task (numeric) |
| `--job-id <uuid>` | — | Resume polling an Azure job (UUID) |
| `--output <path>` | `<input>.<format>` | |

### Common scenarios

**Meeting → SRT with speakers**
```bash
voxflow asr --input meeting.mp4 --speakers --speaker-number 4 --format srt -o meeting.srt
```

**Quick transcript (no quota cost)**
```bash
voxflow asr --input recording.mp3 --engine local --model small --format txt
```

**Mixed Chinese + English audio**
```bash
voxflow asr --input bilingual.mp3 --lang 16k_zh_en
```


## 📋 asr-jobs — browse Azure ASR job history

Azure batch jobs run server-side and survive across CLI sessions, so this command is the dashboard for them. All four subcommands talk to `/api/asr/jobs/*` directly.

```bash
# List the 20 most recent jobs (server-side, paginated)
voxflow asr-jobs list

# Show one job (with transcript preview if succeeded)
voxflow asr-jobs show 6f3c2798-87bf-4367-bb4c-08b872e12bef

# Re-emit the transcript locally without re-running ASR
voxflow asr-jobs download 6f3c2798-87bf-4367-bb4c-08b872e12bef --format srt -o meeting.srt

# Cancel a running job (refunds quota, deletes Azure-side transcription)
voxflow asr-jobs cancel 6f3c2798-87bf-4367-bb4c-08b872e12bef

# Machine-readable
voxflow asr-jobs list --json
voxflow asr-jobs show <jobId> --json
```

| Flag | Default | Notes |
|---|---|---|
| `--limit <n>` | 20 | (list) max 100 |
| `--format srt\|txt\|json` | srt | (download) output format |
| `--output, -o <path>` | `asr-<jobId>.<ext>` | (download) target file |
| `--json` | — | (list, show) raw JSON to stdout |

> The `download` subcommand is idempotent — handy if you ran `asr` long ago and want to re-emit in a different format without paying again. The transcript is stored in `result_json` server-side for at least 30 days (RLS-scoped, only the owner can read it).


## 🌐 translate — SRT / text / file translation

LLM batch translation. Accepts SRT (preserves timing), inline text, or a `.txt` / `.md` file.

```bash
# Translate subtitles, preserve timing
voxflow translate --srt en.srt --to zh -o zh.srt

# Inline text
voxflow translate --text "你好世界" --to en

# File
voxflow translate --input article.md --to en -o article-en.md

# Smart re-timing for length-mismatched languages
voxflow translate --srt zh.srt --to en --realign

# Smaller batches for very long subtitle files
voxflow translate --srt long.srt --to ja --batch-size 5
```

### Options

| Flag | Default | Notes |
|---|---|---|
| `--srt <file>` / `--text <text>` / `--input <file>` | one required | input |
| `--to <lang>` | required | `en`, `zh`, `ja`, `ko`, `es`, `fr`, ... (ISO codes) |
| `--from <lang>` | auto-detect | source language |
| `--realign` | false | Adjust subtitle timing for target-language length expansion (e.g. EN→ZH usually shrinks; EN→JA usually grows) |
| `--batch-size <n>` | `10` | Captions per LLM call, 1–20 |
| `--output <path>` | auto-named | |

> Use `--realign` when translating between languages with very different word density (CJK ↔ Latin) so subs don't crash into each other.


## 🎬 dub — SRT → timeline-aligned TTS

Re-voice a video using its SRT. Per-caption TTS placed at the exact timestamp. Optional speed compensation when speech overflows the slot.

```bash
# Basic — output WAV
voxflow dub --srt subtitles.srt -o dubbed.wav

# Merge into video (requires ffmpeg)
voxflow dub --srt subtitles.srt --video input.mp4 -o dubbed.mp4

# Multi-speaker (SRT lines tagged `[Speaker: Name]`)
voxflow dub --srt show.srt --voices speakers.json --speed-auto -o dubbed.wav

# With background music ducked under speech
voxflow dub --srt narration.srt --bgm music.mp3 --ducking 0.3 -o final.wav

# Patch mode — re-synthesize one caption without full re-run
voxflow dub --srt subtitles.srt --patch 5 -o dub-existing.wav
```

### `speakers.json` format

```json
{
  "Alice": "v-female-R2s4N9qJ",
  "Bob":   "v-male-s5NqE0rZ",
  "Narrator": "v-female-T8m4WxP7"
}
```

SRT captions tag speaker inline:
```
1
00:00:01,000 --> 00:00:03,500
[Speaker: Alice] Hello from Alice!
```

Unmatched speakers fall back to `--voice`.

### `--speed-auto` (overflow protection)

When TTS audio is longer than the SRT time slot, dub computes `alpha = T_raw / T_target` and re-synthesizes at `speed × alpha`. If `alpha > 2.0`, prints `OVERFLOW_WARNING` and tries at speed `2.0` (max).

### Options

| Flag | Default | Notes |
|---|---|---|
| `--srt <file>` | required | |
| `--video <file>` | — | Merge dub into the original video |
| `--voice <id>` | `v-female-R2s4N9qJ` | Default voice |
| `--voices <file>` | — | JSON speaker→voiceId map |
| `--speed <n>` | `1.0` | 0.5–2.0 |
| `--speed-auto` | false | Auto-compensate per-caption overflow |
| `--bgm <file>` | — | Background music |
| `--ducking <n>` | `0.2` | BGM volume when speech is active (0–1) |
| `--patch <id>` | — | Re-synthesize a single caption by ID |
| `--output <path>` | `./dub-<ts>.wav` | `.wav` or `.mp4` |

### Pipeline

```
SRT → parseSrt() → captions[]
  ↓
per-caption TTS (with voice mapping + speed compensation)
  ↓
buildTimelineAudio(segments) → 24kHz / 16-bit / mono WAV
  ↓ optional
mixWithBgm() → mixed WAV
  ↓ optional
mergeAudioVideo() → MP4
```


## 🌍 video-translate — end-to-end pipeline

ASR → translate → dub → burn subtitles → auto-open. The "translate this video into another language" one-shot.

**Pipeline (5 stages):**
```
[1/5] FFmpeg check
[2/5] ASR (flash mode → Azure fallback) → fine-grained per-sentence SRT
[3/5] Translate → quality check → auto-retry untranslated captions
[4/5] TTS dub (speed-auto) → merge audio into video
[5/5] Burn subtitles into video → auto-open output
```

**Output:** `<input>-<lang>.mp4` (with burned subtitles) + `<input>-<lang>.srt` (standalone subtitle file)

```bash
# Auto-detect source, dub to English
voxflow video-translate --input video.mp4 --to en

# Explicit source, with re-timing
voxflow video-translate --input video.mp4 --from zh --to en --realign

# Specific voice for dubbed track
voxflow video-translate --input video.mp4 --to ja --voice v-male-Bk7vD3xP

# All-local (no quota cost — uses Whisper for ASR; LLM still consumes quota for translation)
voxflow video-translate --input video.mp4 --to en --engine local

# Keep SRT + audio intermediates for inspection
voxflow video-translate --input video.mp4 --to en --keep-intermediates
```

### Options

| Flag | Default | Notes |
|---|---|---|
| `--input <file>` | required | source video |
| `--to <lang>` | required | target language code |
| `--from <lang>` | auto | source language |
| `--voice <id>` | default | TTS voice for dubbed track |
| `--voices <file>` | — | Multi-speaker map |
| `--realign` | false | Adjust subtitle timing for target length |
| `--speed <n>` | `1.0` | TTS speed |
| `--batch-size <n>` | `10` | Translation batch size |
| `--keep-intermediates` | false | Keep SRT, raw audio |
| `--asr-mode <mode>` | auto | Override ASR mode |
| `--asr-lang <engine>` | auto | Override ASR engine code |
| `--engine` | `auto` | ASR engine: `auto` \| `local` \| `cloud` |
| `--model` | `base` | Whisper model for local engine |
| `--output <path>` | `<input>-<lang>.mp4` | |

> For multi-speaker dubbing, run `asr` separately first with `--speakers`, then edit the resulting SRT to tag `[Speaker: Name]` lines, then run `dub` with `--voices` — `video-translate` doesn't preserve speaker tags through translation by default.


## 🚀 publish — one-shot end-to-end (recommended for agents)

`publish` bundles ASR / translation / dubbing / merge into a single command and emits a structured JSON result via `--json`. Use this instead of stitching `asr` + `translate` + `dub` yourself when an agent or web orchestrator drives the run.

Three build modes (auto-selected from inputs):

| Mode | Use when | Inputs |
|---|---|---|
| `video-translate` | Source video → translated dubbed video | `--input <video> --to <lang>` |
| `srt-dub` | You already have an SRT and want it dubbed onto a video | `--input <video> --srt <subs.srt>` |
| `merge-existing` | Video + audio already produced; just merge + deliver | `--video <v.mp4> --audio <a.wav>` |

Publish targets:

- `--publish local` (default) — copy artifact to `./published/<base>-<platform>-<ts>.mp4`
- `--publish webhook --publish-webhook <url>` — POST artifact metadata to webhook, return URL
- `--publish none` — skip publish step, return final MP4 path only

Always pass **`--json`** when invoking from a Skill — stdout becomes a single JSON doc (`artifact.path` / `artifact.durationSec` / `artifact.sizeBytes` / `publish.publishUrl` / `quotaUsed`, etc.) instead of human-readable progress.

```bash
# End-to-end: source video → translated dubbed publish
voxflow publish --input talk.mp4 --to en --json

# Hand off to webhook publisher
voxflow publish --input talk.mp4 --to ja --publish webhook --publish-webhook https://hook.example.com/in --json
```


## 📋 summarize — content → slides (and optional video)

Long video/audio/text → ASR (if needed) → LLM summary → PPTX deck. Optional TTS narration and Remotion video render.

```bash
voxflow summarize --input lecture.mp4
voxflow summarize --input meeting.mp4 --lang zh --slides 10
voxflow summarize --input podcast.mp3 --engine local --tts
voxflow summarize --input lecture.mp4 --video --scheme aurora
voxflow summarize --text "长篇文章内容..." --slides 6 --lang zh
```

| Flag | Default | Notes |
|---|---|---|
| `--input <file>` / `--text <text>` | one required | |
| `--slides <n>` | `8` | 4–12 |
| `--lang` | `en` | Output language |
| `--engine` | `auto` | ASR engine for `--input` |
| `--model` | `base` | Whisper model for local ASR |
| `--tts` | false | Add TTS narration audio per slide |
| `--video` | false | Also render an MP4 (needs `remotion-cards/`) |
| `--scheme` | `aurora` | Video scheme — see [video.md](video.md) skill for full table |
| `--voice <id>` | `v-female-R2s4N9qJ` | |
| `--output <path>` | `<input>-summary.pptx` | |

> `summarize --video` overlaps with `present`. Use `summarize` when starting from a long video/audio source; use `present` when starting from a topic / pasted article.


## Common workflows

### Translate a YouTube video to Chinese (full pipeline)

```bash
# 1. Download (yt-dlp / etc.) → video.mp4
# 2. One-shot:
voxflow video-translate --input video.mp4 --to zh --realign --keep-intermediates
# Output: video-zh.mp4 + intermediate .srt files
```

### Generate clean SRT from a recording

```bash
voxflow asr --input recording.mp3 --speakers --speaker-number 3 --format srt -o clean.srt
```

### Long meeting / lecture (1 hr+) → word-timed SRT

```bash
# Kick off — Ctrl+C is safe, the server keeps working.
voxflow asr --input lecture-2h.mp4 --engine azure --lang ja-JP --diarize --speaker-number 4

# Days later, browse what ran:
voxflow asr-jobs list

# Re-download in TXT instead of SRT — no extra quota:
voxflow asr-jobs download <jobId> --format txt -o lecture.txt
```

### Re-dub an existing SRT with different voices

```bash
voxflow dub --srt show.srt --video show.mp4 --voices new_cast.json --speed-auto -o new_cast.mp4
```

### Patch a single bad caption without re-rendering

```bash
# Edit clean.srt's caption 12, then:
voxflow dub --srt clean.srt --patch 12 -o updated.wav
```

### Lecture / podcast → summary deck

```bash
voxflow summarize --input lecture-2h.mp4 --slides 12 --lang zh --tts -o summary.pptx
```


## Quota cost

| Operation | Cost |
|---|---|
| `asr` cloud (Tencent, per call) | ~50–200 |
| `asr` local (Whisper) | 0 |
| `asr` azure (per audio minute, ceil) | 150 (78s = 2min = 300; 30-min = 4500; 1-hr = 9000) |
| `translate` (per 1K target chars) | ~50 |
| `dub` per caption (TTS) | ~50 |
| `video-translate` 5-min video | ~2,000–4,000 |
| `summarize` 1-hr video | ~4,000–6,000 |

Always `voxflow status` before long jobs.

## Rules

1. **Pick the right engine for the file:**
   - `local` — best when you have whisper.cpp installed and want zero quota.
   - `cloud` (Tencent) — best for short clips (≤2 hr), fast turnaround.
   - `azure` — best for **30-min+ recordings, word-level timestamps, multi-locale auto-detect, or anything you might need to resume after a disconnect**. Server-side jobs survive Ctrl+C.
2. **Translation batch size is critical:**
   - Default `--batch-size 5` is the sweet spot. Larger batches (10+) cause LLM to silently drop captions.
   - If you see untranslated lines in output, reduce to `--batch-size 3`.
   - The CLI auto-retries failed batches up to 2 times with validation.
3. **`--realign`** when translating between very different language families (EN ↔ JA / ZH).
4. **For multi-speaker dub**, generate the SRT with `--speakers` first, manually verify and tag, then `dub --voices`.
5. **Always test on a 1-minute clip** before running `video-translate` on a long video — it consumes quota linearly.
6. After completion, auto-play: `open output.mp4`.
7. Keep `--keep-intermediates` on for the first run of any pipeline so you can inspect what failed.
8. For Azure jobs that are still running, **don't re-submit** if the user closes the terminal — `voxflow asr-jobs list` to find the jobId, then `voxflow asr --engine azure --job-id <uuid>` (or `voxflow asr-jobs download <uuid>`) resumes free of charge.
9. **video-translate auto-enables `--speed-auto`** — if TTS audio overflows the time slot, it auto-adjusts. No manual flag needed.
10. **Quality self-check**: After translation, the CLI checks if >30% captions are unchanged (untranslated). If so, it warns you to use a smaller batch size.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Captions left untranslated (original language) | LLM dropped lines in large batch | Use `--batch-size 3` |
| `cloud` ASR returns 500 error | Tencent service transient failure | Switch to `--engine azure` |
| TTS audio overflows time slot | Translation text longer than source | Add `--speed-auto` (or use `video-translate` which enables it by default) |
| `ffmpeg` not found for `--video` | Not installed or not in PATH | `brew install ffmpeg` / install ffmpeg-full for subtitle burn-in |
| Azure job seems stuck | Still processing | `voxflow asr-jobs show <id>` to check status; don't re-submit |
| Subtitle timing drift after translation | Different word density between languages | Add `--realign` |
| Low subtitle quality in specific domain | ASR hot-words not tuned | Try `--engine azure --lang <exact BCP-47>` for better recognition |
