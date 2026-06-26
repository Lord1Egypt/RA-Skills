---
name: talkies
description: Self-hosted OpenAI-compatible speech service. /v1/audio/transcriptions fronts seven open ASR models (Whisper, Parakeet, Canary); /v1/audio/speech fronts two TTS engines — Kokoro-82M (41 baked voices) and Qwen3-TTS-0.6B (CUDA-only voice cloning from user-mounted .wav reference clips). Same wire format as OpenAI — change the base URL + slug. Stereo diarization, URL fetching, MCP endpoint, bearer auth.
homepage: https://github.com/psyb0t/docker-talkies
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🎙️", "primaryEnv": "TALKIES_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# talkies

Self-hosted speech service — ASR and TTS, one container. OpenAI-compatible wire shape on both endpoints; point an OpenAI client at it, change the model slug, done.

ASR (`POST /v1/audio/transcriptions`): six backends — `whisper-large-v3`, `whisper-large-v3-turbo`, `parakeet-tdt-0.6b-v3`, `canary-180m-flash`, `canary-1b-flash`, `canary-qwen-2.5b`.

TTS (`POST /v1/audio/speech`): two engines — `kokoro-82m` with 41 baked voices across en/es/fr/hi/it/pt, and `qwen3-tts-0.6b` for CUDA-only voice cloning from reference clips (three builtin samples plus any `.wav` you drop into `/data/custom-voices/`, including nested subdirs). Both discovered via `GET /v1/audio/voices`.

Extras: stereo diarization on transcription, URL `file_path` fetching, server-side file staging, MCP endpoint with 6 ASR-side tools, optional bearer-token auth.

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## When To Use

- Transcribe audio files (any format ffmpeg decodes — WAV, MP3, M4A, FLAC, OGG, WebM, Opus, MP4 audio).
- Generate SRT/VTT subtitles for video.
- Transcribe podcasts, lectures, interviews, voicemails, calls.
- Stereo two-mic recordings → per-speaker diarized output (`L:` / `R:` channel tagging).
- German/French/Spanish ↔ English speech-to-text translation via Canary-1B-Flash.
- Synthesize speech from text via Kokoro-82M — English (American + British), Spanish, French, Hindi, Italian, Portuguese.
- Voice-clone speech via Qwen3-TTS-0.6B from a reference `.wav` you provide — drop into `/data/custom-voices/`, immediately appears under `GET /v1/audio/voices` with `origin=custom`.
- Drop-in replacement for `api.openai.com/v1/audio/transcriptions` and `api.openai.com/v1/audio/speech` in existing client code.

## When NOT To Use

- Real-time / streaming output — both endpoints are request/response only.
- Speaker identification from voice (only stereo-channel diarization is supported, not voice clustering).
- Per-request `prompt` / `temperature` (transcribe) or `instructions` (speech) injection — fields accepted for compat, **ignored**.
- Japanese / Chinese TTS — Kokoro upstream supports them but talkies filters those voices out (they need the `misaki[ja]` / `misaki[zh]` extras).
- Kokoro on OpenAI aliases (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`) — Kokoro exposes its native voice names only (`af_*`, `bm_*`, etc.). Map client-side. (Qwen3-TTS does ship `alloy` / `echo` / `fable` as builtin voice slugs, but they're voice-cloned samples, not OpenAI's voices — there's no audio compatibility.)
- `qwen3-tts-0.6b` on CPU — voice cloning hard-fails without CUDA at load time. The `faster_qwen3_tts` upstream raises `ValueError` on non-CUDA devices; talkies surfaces this as a load failure on the first request.
- `qwen3-tts-0.6b` `speed` parameter — Qwen3-TTS has no playback-rate control. Field is accepted for OpenAI compat but **ignored** (only Kokoro honors `speed`).
- arm64 hosts — `linux/amd64` only.

## Setup

The container should already be running. Set the base URL:

```bash
export TALKIES_URL=http://localhost:8000
```

If the server has `TALKIES_AUTH_TOKEN` set, export it too:

```bash
export TALKIES_AUTH_TOKEN=<your-token>
# every request below needs: -H "Authorization: Bearer $TALKIES_AUTH_TOKEN"
```

**Verify:** `curl $TALKIES_URL/healthz` returns `{"ok": true, "device": "...", "models": [...]}`.

For install / configuration / env vars / CPU vs CUDA images / custom model registry, see [references/setup.md](references/setup.md).

## Quick Start

```bash
# Discover what's available.
curl -s $TALKIES_URL/v1/models | jq

# Simplest transcribe — file upload, JSON response.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-large-v3-turbo" | jq

# Same call, but the audio lives at a URL — talkies downloads + caches it.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file_path=https://example.com/podcasts/ep-042.mp3" \
  -F "model=whisper-large-v3-turbo" | jq

# Full Whisper-shape JSON with per-segment + per-word timestamps.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json" | jq

# SRT subtitles.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@lecture.mp3" \
  -F "model=whisper-large-v3" \
  -F "response_format=srt" > lecture.srt

# Discover TTS voices, then synthesize an MP3.
curl -s $TALKIES_URL/v1/audio/voices | jq
curl -s $TALKIES_URL/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "kokoro-82m",
        "input": "Hello from talkies.",
        "voice": "af_heart",
        "response_format": "mp3"
      }' \
  --output hello.mp3
```

## Supported Models

### ASR

| Slug | Family | CPU | CUDA | Languages | Strength |
|---|---|---|---|---|---|
| `whisper-large-v3` | faster-whisper | yes | yes | 99 auto-detect | best accuracy, slowest |
| `whisper-large-v3-turbo` | faster-whisper | yes | yes | 99 auto-detect | sweet spot — fast, accurate |
| `parakeet-tdt-0.6b-v3` | NeMo TDT | no | yes | English only | very fast on GPU |
| `canary-180m-flash` | NeMo Canary | yes | yes | English only (small) | smallest, runs anywhere |
| `canary-1b-flash` | NeMo Canary | no | yes | en/de/fr/es + translation | multilingual, translation |
| `canary-qwen-2.5b` | NeMo SALM | no | yes | English only | best English accuracy (no timestamps) |

Pick by use case:
- **General-purpose:** `whisper-large-v3-turbo`.
- **English-only, max accuracy on GPU:** `canary-qwen-2.5b` (but no per-segment timestamps).
- **Translation EN↔DE/FR/ES:** `canary-1b-flash` (requires custom model registry — see [Translation](#translation)).

### TTS

| Slug | Family | CPU | CUDA | Languages | Voices |
|---|---|---|---|---|---|
| `kokoro-82m` | Kokoro (in-process, 24 kHz) | yes | yes | en (US + UK), es, fr, hi, it, pt | 41 baked (discover via `GET /v1/audio/voices`) |
| `qwen3-tts-0.6b` | Qwen3-TTS (voice clone, 12 kHz) | no | yes | en, zh, ko, ja, fr, de, ru, es, it, pt, pl, nl, ar, vi, th, id, ms (17) | 3 builtin samples + any `.wav` under `/data/custom-voices/` |

Pick by use case:
- **General-purpose multi-voice TTS:** `kokoro-82m` — fast, 41 baked voices, runs on CPU.
- **Voice cloning from a reference clip:** `qwen3-tts-0.6b` — drop a `.wav` into `/data/custom-voices/`, immediately usable. CUDA required.

`canary-qwen-2.5b` produces no segment/word timestamps — `verbose_json.segments` and `.words` come back empty, `srt`/`vtt` collapse to a single full-duration cue. Transcription itself is whole-file. Use a Whisper or Canary multitask slug if you need timing.

## API — `POST /v1/audio/transcriptions`

Multipart form. Same field names as OpenAI's transcription endpoint where they overlap.

### Request Fields

| Field | Required | Default | Notes |
|---|---|---|---|
| `file` | one of `file`/`file_path` | — | Audio file. Capped at `TALKIES_MAX_UPLOAD_BYTES` (default 100 MB). |
| `file_path` | one of `file`/`file_path` | — | Either a path under the staging area (`/v1/files`) or an `http(s)://` URL (downloaded + cached server-side). Not subject to the 100 MB upload cap; URL downloads capped by `TALKIES_MAX_DOWNLOAD_BYTES` (default 1 GiB). |
| `model` | yes | — | One of the configured slugs (see `GET /v1/models`). Unknown → 404. |
| `language` | no | model default | ISO-639-1 code. Whisper auto-detects when omitted; Canary uses its `default_source_lang`. |
| `response_format` | no | `json` | `json` / `text` / `verbose_json` / `srt` / `vtt`. |
| `timestamp_granularities[]` | no | — | Accepted for OpenAI compat; ignored — `verbose_json` always emits both segment + word. |
| `prompt` | no | — | **Accepted, ignored.** |
| `temperature` | no | — | **Accepted, ignored.** |
| `diarization` | no | `false` | Stereo-channel diarization. Requires 2-channel input — mono returns 400. |

Exactly one of `file` or `file_path` must be set — passing both or neither returns 400.

### Response Formats

| `response_format` | Content-Type | Shape |
|---|---|---|
| `json` (default) | `application/json` | `{"text": "..."}` — just the transcript. |
| `text` | `text/plain` | The transcript as plain text. |
| `verbose_json` | `application/json` | Full Whisper shape — `task`, `language`, `duration`, `text`, `segments[]`, `words[]`. |
| `srt` | `application/x-subrip` | SubRip subtitle file, one cue per VAD-segmented chunk. |
| `vtt` | `text/vtt` | WebVTT subtitle file, one cue per VAD-segmented chunk. |

`json` shape:
```json
{ "text": " full transcript as a single string" }
```

`verbose_json` shape — `segments` and `words` are always present (empty arrays for backends with no alignment output):
```json
{
  "task": "transcribe",
  "language": "en",
  "duration": 6.42,
  "text": " full transcript",
  "segments": [{ "id": 0, "start": 0.0, "end": 2.31, "text": " ...", "tokens": [], "temperature": 0.0, "avg_logprob": null, "compression_ratio": null, "no_speech_prob": null }],
  "words": [{ "word": " the", "start": 0.0, "end": 0.12 }]
}
```

Whisper-only confidence fields (`avg_logprob`, `compression_ratio`, `no_speech_prob`) are emitted as `null` regardless of backend so clients reading them don't crash. `tokens` is always `[]`.

### Stereo Diarization

Pass `diarization=true` and upload a 2-channel file. Left channel = speaker `L`, right channel = speaker `R`. Each channel is transcribed independently, the two timelines are merged chronologically by segment start time.

```bash
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@interview-stereo.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "diarization=true" \
  -F "response_format=verbose_json" | jq
```

What changes:
- `verbose_json` — every segment/word gets `"channel": "L"` or `"R"`. Segments re-numbered after merge.
- `text` / `response_format=text` — rebuilt as alternating turn lines: `L: ...\nR: ...\n...`. Consecutive same-channel segments collapsed into one line per turn.
- `srt` / `vtt` — each cue prefixed with `L:` / `R:`.

Caveats:
- Exactly **2 channels** required. Mono → 400. >2 channels → 400.
- Latency ~2× the mono case (model runs sequentially on each channel).
- The technique is exact for true two-mic setups (interview rigs, podcast splits). It does NOT magically separate speakers from a single-mic recording that's been rendered to stereo.

### Translation

Canary multitask models can translate speech → text in a non-source language. `canary-1b-flash` covers en↔de, en↔fr, en↔es. **The task is baked into the model slug**, not passed per-request — you add a translation-specific slug via custom `models.json` (see [Customizing the model registry](references/setup.md#customizing-the-model-registry)):

```json
{
  "models": {
    "canary-1b-flash-de2en": {
      "repo": "nvidia/canary-1b-flash",
      "executor": "canary_multitask",
      "default_source_lang": "de",
      "default_target_lang": "en",
      "default_task": "s2t_translation",
      "languages": ["de"]
    }
  }
}
```

Then call it normally — `text` carries the English translation:

```bash
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@german-clip.wav" \
  -F "model=canary-1b-flash-de2en" | jq
```

`canary-180m-flash` is English-ASR-only — don't point a translation slug at it. `canary-qwen-2.5b` is English ASR only too.

### Long Files + VAD Chunking

Audio longer than 30 s (`TALKIES_VAD_CHUNK_THRESHOLD`) gets sliced through Silero VAD into ≤28 s speech regions before being handed to the backend. Timestamps are re-assembled by offsetting each chunk's segment/word timings — you get one continuous `segments` list spanning the whole file.

No client-side change. Long files just work. Verify by checking `duration` in `verbose_json`.

### Error Contract

| Status | Shape | When |
|---|---|---|
| 200 | per `response_format` | success |
| 400 | `{"detail": "..."}` | bad audio, mono+diarization, >2 ch+diarization, both/neither of `file`/`file_path`, invalid file_path, URL download failure (DNS, HTTP error, size exceeded, SSRF blocked) |
| 401 | `{"detail": "..."}` | only when `TALKIES_AUTH_TOKEN` is set: missing/wrong bearer. Includes `WWW-Authenticate: Bearer`. |
| 404 | `{"detail": "..."}` | unknown model slug, `file_path` references missing file, `DELETE /api/ps/{slug}` on unloaded model, `/v1/files/{path}` GET/DELETE on missing |
| 413 | `{"detail": "..."}` | upload exceeded `TALKIES_MAX_UPLOAD_BYTES` (multipart `file` and `PUT /v1/files/{path}` only — not `file_path` URL) |
| 422 | `{"detail": [...]}` | Pydantic validation (missing fields, wrong types) |
| 500 | `{"detail": "..."}` | unhandled backend failure |

## API — `POST /v1/audio/speech` (TTS)

JSON body (not multipart). Returns the encoded audio bytes in the body with the matching `Content-Type` — no JSON envelope.

```bash
curl -s $TALKIES_URL/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "kokoro-82m",
        "input": "The quick brown fox jumps over the lazy dog.",
        "voice": "af_heart",
        "response_format": "mp3",
        "speed": 1.0
      }' \
  --output fox.mp3
```

### Request Body

| Field | Required | Default | Notes |
|---|---|---|---|
| `model` | yes | — | TTS model slug. `kokoro-82m` or `qwen3-tts-0.6b`. Unknown → 404. ASR slug → 400. |
| `input` | yes | — | Text to synthesize. Empty / whitespace-only → 400. No fixed length cap; for very long inputs split client-side. |
| `voice` | no | model `default_voice` (`af_heart` for `kokoro-82m`; `alloy` for `qwen3-tts-0.6b`) | Voice catalog per model — call `GET /v1/audio/voices` and filter by `.model`. Unknown → 400 with catalog listed. |
| `response_format` | no | `mp3` | `mp3` / `opus` / `aac` / `flac` / `wav` / `pcm`. |
| `speed` | no | `1.0` | Playback rate, Kokoro only. Clamped to `[0.25, 4.0]`. **Ignored** by `qwen3-tts-0.6b` (no speed control in Qwen3-TTS). |
| `instructions` | no | — | **Accepted, ignored** (neither engine has an instruction-conditioning input). |

### Output Formats

`response_format` picks the encoder applied to Kokoro's raw 24 kHz mono PCM. ffmpeg does the conversion in-process; no temp files.

| `response_format` | Content-Type | Codec / container | Notes |
|---|---|---|---|
| `mp3` (default) | `audio/mpeg` | libmp3lame, 128 kbps CBR | Most universal. |
| `opus` | `audio/ogg` | libopus, 64 kbps VBR, Ogg container | Best quality-per-byte for speech. |
| `aac` | `audio/aac` | AAC-LC, 128 kbps, ADTS | iOS-friendly. |
| `flac` | `audio/flac` | FLAC | Lossless. |
| `wav` | `audio/wav` | PCM s16le, 24 kHz mono, RIFF header | Lossless, largest. |
| `pcm` | `application/octet-stream` | Raw PCM s16le, 24 kHz mono — no container, no header | Real-time chaining. Caller must know sample rate / format. |

### Voices

```bash
curl -s $TALKIES_URL/v1/audio/voices | jq
```

Returns `{"voices": [{"voice", "model", "default", "origin"}]}`. The `origin` field is only present for engines that distinguish baked-in vs user-supplied voices (currently `qwen3-tts-0.6b` — `"builtin"` for image-baked samples, `"custom"` for `/data/custom-voices/` mounts). Kokoro entries omit `origin`.

**Kokoro voices** encode `<lang_code><gender>_<name>`:

| Prefix | Language |
|---|---|
| `af_` / `am_` | American English (female / male) |
| `bf_` / `bm_` | British English (female / male) |
| `ef_` / `em_` | Spanish |
| `ff_` | French |
| `hf_` / `hm_` | Hindi |
| `if_` / `im_` | Italian |
| `pf_` / `pm_` | Portuguese (Brazilian) |

41 voices ship in the image. Japanese (`jf_*` / `jm_*`) and Chinese (`zf_*` / `zm_*`) are filtered out because they need the optional `misaki[ja]` / `misaki[zh]` extras (MeCab + pypinyin chains).

**Qwen3-TTS voices** come from two on-disk dirs merged into one catalog:

- `/opt/talkies/qwen3-voices/` — baked into the CUDA image. Ships three curated samples (`alloy`, `echo`, `fable`) so voice cloning works out-of-the-box. `origin=builtin`.
- `/data/custom-voices/` — host-mounted via the data volume. Drop `foo/bar/me.wav` and voice `foo/bar/me` immediately appears in `GET /v1/audio/voices` (catalog is rescanned per request — no restart). `origin=custom`.

Voice names are the wav's path relative to its parent dir with `.wav` stripped — nested subdirs are preserved. `custom-voices/team-a/jane.wav` → voice `team-a/jane`. Custom voices shadow builtin voices with the same name; dropping a `custom-voices/alloy.wav` overrides the builtin `alloy` sample (its `origin` flips to `custom`).

Optional sibling metadata next to each `<name>.wav`:
- `<name>.txt` — reference transcript for the clip (ICL voice cloning works without it, but clone fidelity is noticeably better with a faithful transcript).
- `<name>.lang` — language label string (defaults to `English`).

Path-traversal guard: hostile symlinks whose `resolve()` escapes the voices dir are skipped (the wav can't be used to read arbitrary host files as a voice prompt).

```bash
# Add a custom clone voice (server picks it up on next request — no restart).
mkdir -p ~/talkies-data/custom-voices/team-a
cp jane-reading.wav ~/talkies-data/custom-voices/team-a/jane.wav
echo "And the silken sad uncertain rustling of each purple curtain." \
  > ~/talkies-data/custom-voices/team-a/jane.txt

# Use it.
curl -s $TALKIES_URL/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen3-tts-0.6b",
        "input": "Hello from a cloned voice.",
        "voice": "team-a/jane",
        "response_format": "wav"
      }' \
  --output cloned.wav
```

**First synth is slow** on Qwen3-TTS — the predictor + talker CUDA graphs are captured on first call (~30-60 s on a mid-range GPU). Subsequent generations are sub-second. The model and graphs stay resident until evicted by sibling load or the idle sweeper.

### Error Contract (TTS)

| Status | When |
|---|---|
| 200 | success (audio bytes in body) |
| 400 | empty `input`, unknown `voice`, unsupported `response_format`, model isn't TTS (e.g. POSTing `whisper-large-v3` here) |
| 401 | `TALKIES_AUTH_TOKEN` set, missing / wrong bearer |
| 404 | unknown `model` slug |
| 422 | Pydantic validation (missing required fields, wrong types) |
| 500 | unhandled ffmpeg or kokoro internal failure |
| 503 | TTS snapshot files missing under `${TALKIES_DATA_DIR}/models/<slug>/` (slug excluded from `TALKIES_ENABLED_MODELS` but still being called); or `qwen3-tts-0.6b` requested on a non-CUDA device (the backend hard-fails at load time) |

## Resource-Management Endpoints (Ollama-Style)

talkies mirrors a subset of [speaches](https://github.com/speaches-ai/speaches) / Ollama, so a LiteLLM proxy can drive both.

| Endpoint | Behavior |
|---|---|
| `GET /healthz` | Unauthenticated liveness. Returns `{ok, device, models}`. |
| `GET /v1/models` | OpenAI-style list of configured slugs. Each entry includes a `modality` field (`asr` or `tts`) so clients can filter. |
| `GET /api/ps` | Currently-loaded models with per-model `idle_seconds`. |
| `DELETE /api/ps/{model_id}` | Evict one model. Slug can be URL-encoded (`/` → `%2F`). 404 if not loaded. |
| `POST /unload` | Evict every loaded model. Returns the list actually unloaded. |

Behind these: an **idle sweeper** runs every `TALKIES_SWEEPER_INTERVAL` s (default 60) and unloads anything not used in `TALKIES_MODEL_TTL` s (default 600). Set `TALKIES_MODEL_TTL=0` to disable.

There's also **sibling eviction at request time** — every transcribe or speech request evicts other loaded models so VRAM doesn't get split. ASR and TTS share the same pool; loading Kokoro evicts a resident Whisper and vice versa. One model resident at a time, per container. If you need two models simultaneously, run two containers.

```bash
# Which models are loaded right now.
curl -s $TALKIES_URL/api/ps | jq

# Free VRAM after a job — evict one model.
curl -s -X DELETE "$TALKIES_URL/api/ps/whisper-large-v3-turbo"

# Or evict everything.
curl -s -X POST $TALKIES_URL/unload | jq
```

## Server-Side File Staging (`/v1/files`)

For repeated transcribes of the same file (different `response_format`, different model, iterating on params), stage the file once and reference it by path. Files land under `${TALKIES_DATA_DIR}/files/<path>`.

| Endpoint | Behavior |
|---|---|
| `GET /v1/files` | List every staged file. Returns `{"files": [{"path", "size", "modified"}]}`. |
| `PUT /v1/files/{path}` | Upload raw bytes (`--data-binary @local-file`). Capped at `TALKIES_MAX_UPLOAD_BYTES`. Atomic write (`.part` → rename). |
| `GET /v1/files/{path}` | Streams file back. Content-Type guessed by extension. 404 if missing. |
| `DELETE /v1/files/{path}` | Removes file and prunes empty parent dirs. 404 if missing. |

```bash
# Stage once.
curl -X PUT --data-binary @lecture.mp3 \
  -H "Content-Type: audio/mpeg" \
  $TALKIES_URL/v1/files/lectures/2026-03-15/lecture.mp3

# Reuse across multiple transcribe calls.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file_path=lectures/2026-03-15/lecture.mp3" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json" | jq

# Cleanup.
curl -X DELETE $TALKIES_URL/v1/files/lectures/2026-03-15/lecture.mp3
```

Path safety: null bytes, backslashes, `.` / `..` segments and double slashes are rejected (400). Symlinks pointing outside the root are refused. Leading `/` is stripped — `/foo/bar.mp3` and `foo/bar.mp3` resolve identically.

### URL `file_path` (Download + Cache)

`file_path` also accepts `http://` / `https://` URLs. First request downloads to `${TALKIES_DATA_DIR}/files/downloads/<sha256(url)[:16]>-<basename>`, subsequent requests with the same URL hit the cache.

```bash
# First call: downloads, transcribes off the cached copy.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file_path=https://example.com/podcasts/ep-042.mp3" \
  -F "model=whisper-large-v3-turbo" | jq

# Second call: same URL → cache hit, no re-download.
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file_path=https://example.com/podcasts/ep-042.mp3" \
  -F "model=canary-1b-flash" \
  -F "response_format=srt" > ep-042.srt
```

Downloads appear in `GET /v1/files` listings under `downloads/`. Invalidate a single cached URL with `DELETE /v1/files/downloads/<key>`.

Constraints applied during download:
- Size capped by `TALKIES_MAX_DOWNLOAD_BYTES` (default 1 GiB).
- 5 redirect hops max; SSRF guard re-applied at every hop.
- 10 s connect, 300 s per-chunk read timeout.
- SSRF off by default. Set `TALKIES_BLOCK_PRIVATE_DOWNLOADS=true` to reject URLs whose hostname resolves to private/loopback/link-local/multicast/reserved IPs.

## MCP Endpoint (`/v1/mcp`)

talkies exposes a [Model Context Protocol](https://modelcontextprotocol.io) server over Streamable HTTP at `/v1/mcp`. Same FastAPI process, same `BACKENDS` / `REGISTRY`, same auth middleware — a model loaded by the MCP `transcribe` tool is the same instance the HTTP endpoint sees.

MCP exposes the ASR surface only. TTS (`/v1/audio/speech`) is HTTP-only — generated audio bytes don't round-trip through JSON-RPC cleanly. `list_models` filters out TTS slugs so `transcribe` only ever sees ASR backends.

| Tool | What it does |
|---|---|
| `list_models` | Discover ASR slugs (TTS slugs are filtered out). Returns `[{slug, executor, default_source_lang, default_target_lang, default_task, loaded}]`. |
| `transcribe` | Run ASR on a `file_path` (URL or staged path). Args: `model`, `language?`, `response_format?` (`json`/`verbose_json`/`text`/`srt`/`vtt`), `diarization?`. JSON formats return a JSON-encoded string; text/srt/vtt return raw. |
| `list_files` | Same payload as `GET /v1/files`. |
| `put_file` | Upload to staging. Body is base64 (`content_base64`). Decoded size capped at `TALKIES_MAX_UPLOAD_BYTES`. **For big files, prefer `PUT /v1/files/{path}` over HTTP** — JSON-RPC + base64 chews token budget. |
| `get_file` | Read a staged file as base64. Same size cap. Same advice — for big bytes, hit `GET /v1/files/{path}` over HTTP. |
| `delete_file` | Remove a staged file, prune empty parents. |

The transport requires `Accept: application/json, text/event-stream`. Wire it into Claude Code:

```bash
claude mcp add --transport http talkies $TALKIES_URL/v1/mcp
```

With auth:

```bash
claude mcp add --transport http talkies $TALKIES_URL/v1/mcp \
  --header "Authorization: Bearer $TALKIES_AUTH_TOKEN"
```

Note: the canonical mount path is `/v1/mcp/` (trailing slash). Bare `/v1/mcp` is rewritten internally to `/v1/mcp/` so clients that don't follow Starlette's 307 redirect work too.

### Raw JSON-RPC

For debugging or non-MCP-aware callers, hit it as JSON-RPC over HTTP POST:

```bash
# tools/list
curl -s $TALKIES_URL/v1/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# tools/call
curl -s $TALKIES_URL/v1/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
    "params": {
      "name": "transcribe",
      "arguments": {
        "file_path": "https://example.com/clip.mp3",
        "model": "whisper-large-v3-turbo",
        "response_format": "json"
      }
    }
  }'
```

## Bearer-Token Auth

If `TALKIES_AUTH_TOKEN` is set on the server, every route except `/healthz` and CORS preflight (`OPTIONS`) requires `Authorization: Bearer <token>`. Wrong/missing token returns 401 with `WWW-Authenticate: Bearer`. Compared with `hmac.compare_digest` (constant-time).

```bash
curl -H "Authorization: Bearer $TALKIES_AUTH_TOKEN" $TALKIES_URL/v1/models
```

Empty / unset token = wide open. For untrusted networks, combine the token with a reverse proxy doing TLS + rate limiting.

## Typical Workflows

### Quick one-off transcribe

```bash
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-large-v3-turbo" | jq -r .text
```

### Generate subtitles for a video

```bash
ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=whisper-large-v3" \
  -F "response_format=srt" > video.srt
# burn in:  ffmpeg -i video.mp4 -vf subtitles=video.srt -c:a copy video-subbed.mp4
```

### Iterate on the same file with different settings

```bash
# Stage once.
curl -X PUT --data-binary @lecture.mp3 \
  -H "Content-Type: audio/mpeg" \
  $TALKIES_URL/v1/files/work/lecture.mp3

# Try different models / formats without re-uploading.
for fmt in json verbose_json srt; do
  curl -s $TALKIES_URL/v1/audio/transcriptions \
    -F "file_path=work/lecture.mp3" \
    -F "model=whisper-large-v3-turbo" \
    -F "response_format=$fmt" > "lecture.$fmt"
done

# Cleanup.
curl -X DELETE $TALKIES_URL/v1/files/work/lecture.mp3
```

### Diarized interview transcript

```bash
curl -s $TALKIES_URL/v1/audio/transcriptions \
  -F "file=@interview-stereo.wav" \
  -F "model=whisper-large-v3-turbo" \
  -F "diarization=true" \
  -F "response_format=text"
# stdout:
#   L: hi how's it going
#   R: not bad you
#   L: cool man
```

### Synthesize speech from text

```bash
# Default voice, MP3 output.
curl -s $TALKIES_URL/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"kokoro-82m","input":"Greetings, human."}' \
  --output greetings.mp3

# Pick a voice from GET /v1/audio/voices, choose a format.
curl -s $TALKIES_URL/v1/audio/voices | jq -r '.voices[].voice'
curl -s $TALKIES_URL/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "kokoro-82m",
        "input": "Buongiorno, mondo.",
        "voice": "if_sara",
        "response_format": "opus"
      }' \
  --output ciao.opus
```

### Free VRAM after a job

```bash
curl -s -X POST $TALKIES_URL/unload | jq
```

### Bulk transcribe from URLs

```bash
for url in $(cat urls.txt); do
  curl -s $TALKIES_URL/v1/audio/transcriptions \
    -F "file_path=$url" \
    -F "model=whisper-large-v3-turbo" \
    -F "response_format=text"
  echo "---"
done
```

The first hit on each URL downloads + caches; re-running the loop is free.

For a fuller bulk-transcribe driver (mix of local paths + URLs, per-input output files, error reporting, optional diarization) see [`scripts/bulk_transcribe.sh`](scripts/bulk_transcribe.sh):

```bash
TALKIES_URL=http://localhost:8000 \
TALKIES_MODEL=whisper-large-v3-turbo \
TALKIES_FORMAT=srt \
TALKIES_OUTDIR=./subs \
  bash scripts/bulk_transcribe.sh inputs.txt
```

## Tips

1. **Use `whisper-large-v3-turbo`** as your default — it's the speed/quality sweet spot for general-purpose ASR. Switch to `whisper-large-v3` only when you need the last few % of accuracy on hard audio.
2. **URL `file_path` over multipart upload** — if the audio is already at a URL, send the URL. Saves bandwidth (the file isn't going up and then back down), gets cached server-side, no upload size cap.
3. **Stage repeated files** via `PUT /v1/files/{path}` and call with `file_path=` to avoid re-uploading on every retry/iteration.
4. **`response_format=text`** for the "just give me the string" case — no `jq -r .text` needed, content-type is `text/plain`.
5. **One model at a time** — every transcribe request evicts other loaded models. Don't try to fan out two calls against two different models on the same container; the second one evicts the first and reloads. Use two containers if you actually need concurrency on different models.
6. **`POST /unload` after a job** — explicit eviction frees VRAM/RAM faster than waiting for the 10-min idle sweeper. Useful in CI / batch scripts.
7. **`canary-qwen-2.5b` has no timestamps** — `verbose_json.segments` / `.words` come back empty, `srt`/`vtt` collapse to one cue. Use a Whisper or Canary multitask slug if you need timing data.
8. **Diarization requires true stereo** — if your "stereo" file is the same mono signal copied to both channels, diarization won't separate speakers. The technique is exact for two-mic setups, useless otherwise.
9. **Long files just work** — VAD chunking happens transparently. Don't pre-split. Send the whole file.
10. **`prompt` / `temperature` / `instructions` are ignored** even though the request schemas accept them. Don't expect them to do anything.
11. **Watch `/api/ps`** to see what's resident. A request that hangs at "loading model" is doing the first cold load — subsequent calls are fast.
12. **Customizing the model registry** for translation slugs or to restrict the served set — see [references/setup.md](references/setup.md#customizing-the-model-registry).
13. **Kokoro uses native voice names** — no OpenAI aliases. Hit `GET /v1/audio/voices` once to discover what's shipped; pass the `voice` field accordingly. The 41 voices cover en (US + UK), es, fr, hi, it, pt; ja/zh are filtered out.
14. **Voice cloning is `qwen3-tts-0.6b`** — drop a `.wav` (10-30 s of clean speech is plenty) into `/data/custom-voices/<anywhere>.wav`. Optionally drop a sibling `.txt` with a faithful transcript for higher clone fidelity. The voice appears in `GET /v1/audio/voices` on the next request — no restart. CUDA required.
15. **Qwen3-TTS first synth is slow** — CUDA graph capture runs once after model load (~30-60 s). Subsequent synths are sub-second. If you're benchmarking, throw away the first call.
16. **Qwen3-TTS ignores `speed`** — the model has no playback-rate control. Pass it for OpenAI compat; nothing happens. Only Kokoro honors `speed`.
17. **Different TTS sample rates** — Kokoro emits 24 kHz mono PCM; Qwen3-TTS emits 12 kHz mono PCM. ffmpeg re-encodes both into your chosen `response_format`, but if you select `pcm` (raw, no container), you must know the source rate per model to play it back correctly.
18. **TTS `response_format=pcm` is for chaining** — raw int16 mono PCM, no container, no header. Use it when piping into another encoder or a real-time playback path. Otherwise stick with `mp3` (default) or `opus` for size.
19. **TTS evicts loaded ASR and vice versa** — they share the same one-model-resident pool. Synthesizing with Kokoro after a transcribe burst incurs Kokoro's cold load. Same applies to Qwen3-TTS (plus the CUDA-graph capture re-runs on cold reload).
