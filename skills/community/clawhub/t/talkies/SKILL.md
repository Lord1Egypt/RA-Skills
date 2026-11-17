---
name: talkies
description: Self-hosted OpenAI-compatible speech service. /v1/audio/transcriptions fronts 14 open ASR models (Whisper, Parakeet, Nemotron-3.5-ASR, Canary, Sherpa-ONNX, Vosk, plus wav2vec2 and ZIPA phoneme recognizers that emit IPA); /v1/audio/transcriptions/stream accepts live PCM over WebSocket. /v1/audio/speech fronts 3 TTS engines / 4 backends — Kokoro-82M (41 baked voices, PyTorch + ONNX runtimes), the CUDA-only Qwen3-TTS family (voice cloning, preset speakers, voice design), and the CUDA-only Chatterbox Turbo (English, 19 inline emotion tags, transcript-free cloning). Stereo diarization, URL fetching, six ASR/file-staging MCP tools, bearer auth.
homepage: https://github.com/psyb0t/docker-talkies
user-invocable: true
permissions:
  network: "Outbound HTTP to the configured TALKIES_URL; the Talkies server also fetches URLs supplied as file_path."
  shell: "Documented setup and workflow examples invoke local curl, ffmpeg, and docker commands."
  filesystem: "Reads and writes server-side staged files through /v1/files; the skill itself does not access the local filesystem."
metadata:
  { "openclaw": { "emoji": "🎙️", "primaryEnv": "TALKIES_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# talkies

Self-hosted speech service — ASR and TTS, one container. OpenAI-compatible wire shape on both endpoints; point an OpenAI client at it, change the model slug, done.

ASR (`POST /v1/audio/transcriptions`): fourteen bundled slugs — `whisper-large-v3`, `whisper-large-v3-turbo`, `parakeet-tdt-0.6b-v3`, `nemotron-3.5-asr-0.6b`, `canary-180m-flash`, `canary-1b-flash`, `canary-qwen-2.5b`, four selectable English Sherpa Zipformer variants, `vosk-small-en-us-0.15`, and two phoneme recognizers, `wav2vec2-xlsr-53-espeak` and `zipa-ipa`, that return the IPA phones spoken instead of words.

TTS (`POST /v1/audio/speech`): 3 engines / 4 backends across 8 slugs — `kokoro-82m` (PyTorch) and `kokoro-82m-nvidia` (ONNX/ORT) with 41 baked voices across en/es/fr/hi/it/pt, plus the CUDA-only Qwen3-TTS family: `qwen3-tts-0.6b` / `qwen3-tts-1.7b` (voice cloning from reference clips), `qwen3-tts-0.6b-custom` / `qwen3-tts-1.7b-custom` (9 preset speakers), `qwen3-tts-1.7b-design` (voice from an NL description), plus the CUDA-only `chatterbox-turbo` (English only; 19 inline emotion tags; clones from a reference `.wav` with no transcript). Discover voices via `GET /v1/audio/voices`.

Extras: live PCM ASR over WebSocket, stereo diarization on transcription, URL `file_path` fetching, server-side file staging, MCP endpoint with 6 ASR-side tools, optional bearer-token auth.

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

This skill is **not** low-risk to orchestrate blindly — it issues local shell commands (`curl`, `ffmpeg`, `docker` in the typical deployment/setup path) and outbound HTTP requests to whatever `$TALKIES_URL` points at:

- **Outbound HTTP to an operator-chosen host — data leaves your host.** Every command in this skill, including TTS `input` text and voice-cloning reference samples, is sent to whatever `$TALKIES_URL` points at — a server the skill does not control or vet. Point it only at an instance you run or explicitly trust; prefer HTTPS.
- **`file_path` URL fetches happen server-side, not client-side.** Passing a URL causes the *talkies server* to download it — see [URL `file_path` (Download + Cache)](#url-file_path-download--cache) below.
- **Staged files persist server-side until explicitly deleted**, and are enumerable by anyone who can reach the API — see [Server-Side File Staging](#server-side-file-staging-v1files) below.
- **Shared file staging** — staged files (`/v1/files`) live in one namespace with no per-caller ownership: any caller can see or remove any staged file. Only remove paths you staged in the current task, and treat file management as admin-only on a shared instance — see [Server-Side File Staging](#server-side-file-staging-v1files) below.
- **No auth by default** — `TALKIES_AUTH_TOKEN` is opt-in; an unconfigured server is wide open to anyone who can reach the port. Require the token and least-privilege network exposure in any non-trusted environment.
- **Voice cloning requires consent.** Only clone or synthesize a voice you have explicit authorization/consent to use — synthesized speech of a real person can be used for impersonation, fraud, or deception. See [Qwen3-TTS Custom Voices](references/setup.md#qwen3-tts-custom-voices).
- **Local shell execution.** `references/setup.md` and workflow examples run `docker`, `curl`, and `ffmpeg` directly on the local host — review commands before running them against unfamiliar hosts/images.

## When To Use

- Transcribe audio files (any format ffmpeg decodes — WAV, MP3, M4A, FLAC, OGG, WebM, Opus, MP4 audio).
- Generate SRT/VTT subtitles for video.
- Transcribe podcasts, lectures, interviews, voicemails, calls.
- Stream 16 kHz mono PCM from a microphone or decoded live-audio source through `WS /v1/audio/transcriptions/stream`.
- Stereo two-mic recordings → per-speaker diarized output (`L:` / `R:` channel tagging).
- German/French/Spanish ↔ English speech-to-text translation via Canary-1B-Flash.
- Synthesize speech from text via Kokoro-82M — English (American + British), Spanish, French, Hindi, Italian, Portuguese.
- Voice-clone speech via Qwen3-TTS-0.6B from a reference `.wav` you provide — drop into `/data/custom-voices/`, immediately appears under `GET /v1/audio/voices` with `origin=custom`. **Only clone voices you're authorized to use, with the speaker's consent** — see [Qwen3-TTS Custom Voices](references/setup.md#qwen3-tts-custom-voices).
- Voice-clone via `chatterbox-turbo` from the same `/data/custom-voices/` drop — no sibling transcript needed, but the clip must be longer than 5 seconds. Same consent requirement applies.
- Emotive English delivery via `chatterbox-turbo` — write tags inline in `input`, e.g. `Oh no [sigh] not again.` The tokenizer defines exactly 19: `[angry]` `[fear]` `[surprised]` `[whispering]` `[advertisement]` `[dramatic]` `[narration]` `[crying]` `[happy]` `[sarcastic]` `[clear throat]` `[sigh]` `[shush]` `[cough]` `[groan]` `[sniff]` `[gasp]` `[chuckle]` `[laugh]`. Anything else is read as literal text.
- Drop-in replacement for `api.openai.com/v1/audio/transcriptions` and `api.openai.com/v1/audio/speech` in existing client code.

## When NOT To Use

- OpenAI-compatible live ASR — `/v1/audio/transcriptions` remains request/response only. Use talkies-specific `WS /v1/audio/transcriptions/stream` for raw PCM. (TTS has one streaming exception: `qwen3-tts-*` + `response_format=pcm` streams chunked PCM — see [Streaming PCM (Qwen3-TTS)](#streaming-pcm-qwen3-tts).)
- Speaker identification from voice (only stereo-channel diarization is supported, not voice clustering).
- Per-request `prompt` / `temperature` on `/v1/audio/transcriptions` — accepted for OpenAI compat, **ignored**. (`instructions` on `/v1/audio/speech` is different: Kokoro ignores it, but Qwen3-TTS honors it in most modes — see [Request Body](#request-body).)
- Japanese / Chinese TTS — Kokoro upstream supports them but talkies filters those voices out (they need the `misaki[ja]` / `misaki[zh]` extras).
- Kokoro on OpenAI aliases (`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`) — Kokoro exposes its native voice names only (`af_*`, `bm_*`, etc.). Map client-side. (Qwen3-TTS does ship `alloy` / `echo` / `fable` as builtin voice slugs, but they're voice-cloned samples, not OpenAI's voices — there's no audio compatibility.)
- `qwen3-tts-0.6b` on CPU — voice cloning hard-fails without CUDA at load time. The `faster_qwen3_tts` upstream raises `ValueError` on non-CUDA devices; talkies surfaces this as a load failure on the first request.
- `qwen3-tts-0.6b` `speed` parameter — Qwen3-TTS has no playback-rate control. Field is accepted for OpenAI compat but **ignored** (only Kokoro honors `speed`; `chatterbox-turbo` ignores it too).
- `chatterbox-turbo` for anything but English — it is an English-only checkpoint. Use Kokoro or Qwen3-TTS for other languages.
- `chatterbox-turbo` on CPU — the slug is registered in the CUDA image only. The model does run on CPU but measures roughly 5-10x slower than realtime, so it is not offered as a CPU slug.
- `chatterbox-turbo` with default settings where output must be unwatermarked. Every waveform carries Resemble AI's PerTh neural watermark, which the upstream package applies unconditionally. The server can turn it off: set `TALKIES_CHATTERBOX_WATERMARK=false` on the container. That is an operator-side setting, not a per-request one, so a caller cannot change it through the API.
- `chatterbox-turbo` reference clips of 5 seconds or shorter — rejected with a 400. Supply a longer clip.
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
# WARNING: the URL is fetched by the talkies SERVER, not this client, and the
# download is cached persistently on disk (see "URL file_path" below). Don't
# pass URLs to private/sensitive media unless you trust the server operator.
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

## Live streaming ASR

`WS /v1/audio/transcriptions/stream` is talkies-specific rather than an OpenAI
endpoint. It accepts headerless 16 kHz, mono, signed 16-bit little-endian PCM.
Send one JSON `start` message, wait for `ready`, stream binary PCM frames, then
send `{"type":"end"}` for `final` and `stats` (or `{"type":"cancel"}` to
discard the stream). Use a configured ASR slug with streaming support; native
sessions are available through parakeet.cpp, Sherpa-ONNX, and Vosk, while
faster-whisper uses a bounded rolling window. When authentication is enabled,
send the bearer token in the WebSocket upgrade header, never in the URL.

See the repository's [`docs/streaming.md`](https://github.com/psyb0t/docker-talkies/blob/main/docs/streaming.md)
for the exact start/event shapes, a Python client, limits, and custom Sherpa or
Vosk model-registry entries.

## Supported Models

### ASR

| Slug | Family | CPU | CUDA | Languages | Strength |
|---|---|---|---|---|---|
| `whisper-large-v3` | faster-whisper | yes | yes | 99 auto-detect | best accuracy, slowest |
| `whisper-large-v3-turbo` | faster-whisper | yes | yes | 99 auto-detect | sweet spot — fast, accurate |
| `parakeet-tdt-0.6b-v3` | NeMo TDT | no | yes | English only | very fast on GPU |
| `nemotron-3.5-asr-0.6b` | parakeet.cpp / ggml | yes | yes | 40+ locales, auto-detect | CPU or CUDA multilingual; pin via `language=` |
| `canary-180m-flash` | NeMo Canary | yes | yes | English only (small) | smallest, runs anywhere |
| `canary-1b-flash` | NeMo Canary | no | yes | en/de/fr/es + translation | multilingual, translation |
| `canary-qwen-2.5b` | NeMo SALM | no | yes | English only | best English accuracy (no timestamps) |
| `sherpa-zipformer-en-left-64` | Sherpa-ONNX Zipformer | yes | yes | English only | native live ASR, lower left context |
| `sherpa-zipformer-en-left-128` | Sherpa-ONNX Zipformer | yes | yes | English only | native live ASR, higher left context |
| `sherpa-zipformer-en-int8-left-64` | Sherpa-ONNX Zipformer INT8 | yes | yes | English only | smaller native live ASR variant |
| `sherpa-zipformer-en-int8-left-128` | Sherpa-ONNX Zipformer INT8 | yes | yes | English only | smaller native live ASR variant |
| `vosk-small-en-us-0.15` | Vosk | yes | yes | English only | native live ASR; CPU decoder |
| `wav2vec2-xlsr-53-espeak` | wav2vec2 CTC phoneme | yes | yes | multilingual | IPA phones, not words; eSpeak alphabet |
| `zipa-ipa` | ZIPA (Zipformer CTC phoneme) | yes | yes | multilingual | IPA phones, not words; 71 MB, very fast |

Pick by use case:
- **General-purpose:** `whisper-large-v3-turbo`.
- **English-only, max accuracy on GPU:** `canary-qwen-2.5b` (but no per-segment timestamps).
- **Translation EN↔DE/FR/ES:** `canary-1b-flash` (requires custom model registry — see [Translation](#translation)).
- **Low-overhead live English ASR:** one of the Sherpa Zipformer variants or `vosk-small-en-us-0.15`; Sherpa uses CUDA in the CUDA image, while Vosk remains CPU-decoded.
- **Phones, not words (pronunciation checks, phonetics):** `wav2vec2-xlsr-53-espeak` or `zipa-ipa`. Both return a space-separated IPA stream with per-phone timestamps and run no language model, so mispronunciations are not corrected away. `zipa-ipa` is the small fast pick; `wav2vec2-xlsr-53-espeak` is the larger transformers-native one.

### TTS

3 engines / 4 backends across 8 slugs. Kokoro ships in two runtimes (`kokoro-82m` PyTorch, `kokoro-82m-nvidia` ONNX/ORT) — same weights, same voice catalog, same wire format. Qwen3-TTS ships 5 CUDA-only slugs across three modes (base cloning / custom_voice preset speakers / voice_design). Mode is implicit in the slug — see [Qwen3-TTS Modes](#qwen3-tts-modes). `chatterbox-turbo` (CUDA-only, English) rounds out the set — 19 inline emotion tags, transcript-free voice cloning; see [When To Use](#when-to-use) above.

| Slug | Family | Mode | CPU | CUDA | Languages | Voices |
|---|---|---|---|---|---|---|
| `kokoro-82m` | Kokoro (PyTorch in-process, 24 kHz) | — | yes | yes | en (US + UK), es, fr, hi, it, pt | 41 baked (discover via `GET /v1/audio/voices`) |
| `kokoro-82m-nvidia` | Kokoro (ONNX via ORT, 24 kHz) | — | yes | yes | en (US + UK), es, fr, hi, it, pt | 41 baked (same catalog as `kokoro-82m`) |
| `qwen3-tts-0.6b` | Qwen3-TTS (24 kHz) | base | no | yes | 17 (en, zh, ja, ko, fr, de, es, it, pt, ru, vi, th, id, ar, tr, pl, nl) | 3 builtin samples + any `.wav` under `/data/custom-voices/` |
| `qwen3-tts-1.7b` | Qwen3-TTS (24 kHz) | base | no | yes | 10 (en, zh, ja, ko, fr, de, es, it, pt, ru) | 3 builtin samples + any `.wav` under `/data/custom-voices/` |
| `qwen3-tts-0.6b-custom` | Qwen3-TTS (24 kHz) | custom_voice | no | yes | en, zh, ja, ko | 9 preset speakers (`instructions` dropped — 0.6B limitation) |
| `qwen3-tts-1.7b-custom` | Qwen3-TTS (24 kHz) | custom_voice | no | yes | en, zh, ja, ko | 9 preset speakers + emotion via `instructions` |
| `qwen3-tts-1.7b-design` | Qwen3-TTS (24 kHz) | voice_design | no | yes | en, zh, ja, ko | voice synthesized from NL description in `instructions` (required) |
| `chatterbox-turbo` | Chatterbox Turbo (24 kHz, buffered only) | — | no | yes | English only | `builtin` speaker, or any `.wav` (>5s) under `/data/custom-voices/` |

Pick by use case:
- **General-purpose multi-voice TTS:** `kokoro-82m` — fast, 41 baked voices, runs on CPU. Use `kokoro-82m-nvidia` for the ONNX/ORT execution path (CUDA EP on the CUDA image, CPU EP otherwise).
- **Voice cloning from a reference clip:** `qwen3-tts-0.6b` / `qwen3-tts-1.7b` — drop a `.wav` into `/data/custom-voices/`, immediately usable. CUDA required.
- **Preset speakers (no reference WAV):** `qwen3-tts-0.6b-custom` / `qwen3-tts-1.7b-custom` — 9 baked speakers; the 1.7B honours `instructions` for emotion. CUDA required.
- **Invent a voice from a description:** `qwen3-tts-1.7b-design` — the NL description goes in `instructions`. CUDA required.
- **Expressive English delivery, transcript-free cloning:** `chatterbox-turbo` — 19 inline emotion tags in `input`, clones from a bare `.wav` (no sibling transcript needed, clip must be longer than 5 seconds). English only, CUDA required, output always carries a neural watermark.

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

The `sherpa` and `vosk` executors add a per-word `confidence` in the 0–1 range to each entry in `words` — Vosk reports the decoder's own score, Sherpa derives one from the model's per-token acoustic log-probabilities. No other backend emits it, so treat the field as optional.

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
| 404 | `{"detail": "..."}` | unknown model slug, `file_path` references missing file, model-evict on an unloaded model, file op on a missing `/v1/files` path |
| 413 | `{"detail": "..."}` | upload exceeded `TALKIES_MAX_UPLOAD_BYTES` (multipart `file` and `PUT /v1/files/{path}` only — not `file_path` URL) |
| 422 | `{"detail": [...]}` | Pydantic validation (missing fields, wrong types) |
| 500 | `{"detail": "..."}` | unhandled backend failure |

## API — `POST /v1/audio/speech` (TTS)

JSON body (not multipart). Returns the encoded audio bytes in the body with the matching `Content-Type` — no JSON envelope.

**Every call sends your `input` text (and, for voice-cloning slugs, the referenced voice sample) to whatever `$TALKIES_URL` points at — that data leaves your host.** Point `$TALKIES_URL` only at a talkies instance you run or explicitly trust; prefer HTTPS when it's not localhost/LAN. Don't synthesize sensitive or confidential text through a server you don't control.

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
| `model` | yes | — | TTS model slug. Kokoro: `kokoro-82m`, `kokoro-82m-nvidia`. Qwen3-TTS: `qwen3-tts-0.6b`, `qwen3-tts-1.7b` (base/cloning), `qwen3-tts-0.6b-custom`, `qwen3-tts-1.7b-custom` (preset speakers), `qwen3-tts-1.7b-design` (voice from NL description). Chatterbox: `chatterbox-turbo` (English only). Unknown → 404. ASR slug → 400. |
| `input` | yes | — | Text to synthesize. Empty / whitespace-only → 400. No fixed length cap; for very long inputs split client-side. |
| `voice` | no | model `default_voice` | Semantics shift per Qwen3 mode (see [Qwen3-TTS Modes](#qwen3-tts-modes)). Kokoro: voice name (default `af_heart`). Qwen3 `base`: path of a reference WAV (default `alloy`). Qwen3 `custom_voice`: one of the 9 preset speakers (default `Vivian`). Qwen3 `voice_design`: ignored — sentinel `"design"`. `chatterbox-turbo`: `builtin` (default) or the name of a `.wav` under `/data/custom-voices/`, longer than 5 seconds — shorter clips → 400. Unknown → 400 with catalog listed. |
| `response_format` | no | `mp3` | `mp3` / `opus` / `aac` / `flac` / `wav` / `pcm`. |
| `speed` | no | `1.0` | Playback rate, Kokoro only. Clamped to `[0.25, 4.0]`. **Ignored** by every Qwen3-TTS slug (no speed control in Qwen3-TTS) and by `chatterbox-turbo`. |
| `instructions` | no | — | Free-form style prompt. **Required** for `qwen3-tts-1.7b-design` (the NL voice description; empty → 400). **Honoured** by Qwen3-TTS `base` mode and `qwen3-tts-1.7b-custom` (threaded as `instruct`). **Dropped** by `qwen3-tts-0.6b-custom` (0.6B CustomVoice checkpoint limitation — logs a WARNING) and both Kokoro slugs (no instruction input). Accepted on every slug for OpenAI parity. |
| `language` | no | model `default_language` (`English`) | **Non-OpenAI extra field** (send via `extra_body={"language": "..."}` on official SDKs). Selects the spoken language for Qwen3 `custom_voice` / `voice_design`; `base` mode reads it from the voice's sibling `.lang` file. Silently ignored by Kokoro. |
| `temperature` | no | `0.9` | **Non-OpenAI extra, Qwen3-TTS only** (`extra_body`). Sampler temperature, `[0.0, 2.0]`. Ignored by Kokoro. |
| `top_k` | no | `50` | **Non-OpenAI extra, Qwen3-TTS only.** Top-k truncation, `[1, 1000]`. Ignored by Kokoro. |
| `top_p` | no | `1.0` | **Non-OpenAI extra, Qwen3-TTS only.** Nucleus sampling, `[0.0, 1.0]`. Ignored by Kokoro. |
| `repetition_penalty` | no | `1.05` | **Non-OpenAI extra, Qwen3-TTS only.** Penalizes codec-token repeats, `[0.5, 2.0]`. Ignored by Kokoro. |
| `max_new_tokens` | no | `2048` (model max) | **Non-OpenAI extra, Qwen3-TTS only.** Codec-step cap, `[1, 2048]`. Ignored by Kokoro. |
| `do_sample` | no | `true` | **Non-OpenAI extra, Qwen3-TTS only.** `false` = greedy decode. Ignored by Kokoro. |

Out-of-range sampling values → 422 (Pydantic validation).

### Qwen3-TTS Modes

The Qwen3-TTS mode is implicit in the model slug — the OpenAI wire format stays pure (`model` / `voice` / `instructions` / `input`), with `voice` and `instructions` carrying mode-specific semantics. No new endpoints.

| Mode | Slugs | What `voice` means | What `instructions` means |
|---|---|---|---|
| **base** (voice cloning) | `qwen3-tts-0.6b`, `qwen3-tts-1.7b` | Path of a reference `.wav` under the voices dirs (`.wav` stripped) | Optional style hint (passed as `instruct`) |
| **custom_voice** (preset speakers) | `qwen3-tts-0.6b-custom`, `qwen3-tts-1.7b-custom` | One of 9 preset speaker names | Emotion / style cue — 1.7B honours it; 0.6B drops it (checkpoint limitation, logs a WARNING) |
| **voice_design** (NL description) | `qwen3-tts-1.7b-design` | Ignored — sentinel `"design"` | **Required.** NL description of the voice (e.g. "A warm, friendly young female voice"). Empty → 400. |

The 9 `custom_voice` preset speakers (also returned by `GET /v1/audio/voices` for the chosen slug): `Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric` (Chinese), `Ryan`, `Aiden` (English), `Ono_Anna` (Japanese), `Sohee` (Korean).

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

### Streaming PCM (Qwen3-TTS)

`qwen3-tts-*` slugs stream `response_format=pcm` requests as chunked int16 PCM instead of buffering the whole utterance — first-audio latency drops from seconds to sub-second. Kokoro and every non-`pcm` format are unaffected (buffered as normal). Response carries an `X-Sample-Rate` header; chunk size (codec steps per yielded chunk) is tunable via `TALKIES_QWEN3_STREAM_CHUNK_SIZE` (default 8) — see [references/setup.md](references/setup.md).

```bash
curl -s $TALKIES_URL/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-tts-0.6b","input":"Streaming test.","response_format":"pcm"}' \
  --output stream.pcm
```

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
| `DELETE /api/ps/{model_id}` | Evict one model from memory. Slug can be URL-encoded (`/` → `%2F`). 404 if not loaded. |
| `POST /unload` | Evict every loaded model. Returns the list actually unloaded. |

Model eviction (`DELETE /api/ps/...`, `POST /unload`) forces a cold-load for anyone mid-request, so only do it for explicit maintenance the user asked for (e.g. "free up VRAM"). Auth is only enforced when `TALKIES_AUTH_TOKEN` is set — require it on shared deployments and don't expose these routes on an unauthenticated network.

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

**Staged files persist until explicitly removed** — nothing auto-expires them — and `GET /v1/files` enumerates every staged path to anyone who can reach the API. Don't stage sensitive/private media on a server without auth enabled (`TALKIES_AUTH_TOKEN`); clean up staged files when done.

**Guardrail — this is a shared, unisolated bucket, not a private workspace.** There's no per-caller ownership: any path any caller staged is listable and readable by any other caller with API access. An agent must:
- only read or delete paths it staged itself in the current, user-approved workflow;
- never call `GET /v1/files` to browse/enumerate what other callers have staged, and never delete a path it didn't create;
- clean up what it staged once the workflow is done, since nothing expires automatically.

At the deployment level: require `TALKIES_AUTH_TOKEN` by default, treat per-caller isolation and retention limits as the operator's responsibility (talkies itself provides neither).

| Endpoint | Behavior |
|---|---|
| `GET /v1/files` | List every staged file. Returns `{"files": [{"path", "size", "modified"}]}`. **Enumerable by anyone with API access — no per-file ownership/isolation.** |
| `PUT /v1/files/{path}` | Upload raw bytes (`--data-binary @local-file`). Capped at `TALKIES_MAX_UPLOAD_BYTES`. Atomic write (`.part` → rename). |
| `GET /v1/files/{path}` | Streams file back. Content-Type guessed by extension. 404 if missing. |
| `DELETE /v1/files/{path}` | Removes a staged file and prunes empty parent dirs (404 if missing). Files don't self-expire, so call this to clean up when done. On a shared bucket every path is listable by any caller, so only remove paths you staged yourself. |

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

**The download happens server-side, and the result is cached persistently on the talkies server's disk** — not a transient client-side fetch. Anyone who can reach the API can later list/read that cached copy via `GET /v1/files` (see [Server-Side File Staging](#server-side-file-staging-v1files) above). Don't pass URLs to private/sensitive media unless the talkies server itself is trusted and access-controlled (`TALKIES_AUTH_TOKEN`); invalidate the cache entry when done.

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

Downloads appear in `GET /v1/files` listings under `downloads/`. Invalidate a single cached URL by removing it from `/v1/files/downloads/`.

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

# Clean up the staged file when done (see the /v1/files reference above).
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
For local files, replace the `file_path` form field with `file=@path/to/audio`
in the same request shape.

## Tips

1. **Use `whisper-large-v3-turbo`** as your default — it's the speed/quality sweet spot for general-purpose ASR. Switch to `whisper-large-v3` only when you need the last few % of accuracy on hard audio.
2. **URL `file_path` over multipart upload** — if the audio is already at a URL, send the URL. Saves bandwidth (the file isn't going up and then back down), gets cached server-side, no upload size cap.
3. **Stage repeated files** via `PUT /v1/files/{path}` and call with `file_path=` to avoid re-uploading on every retry/iteration.
4. **`response_format=text`** for the "just give me the string" case — no `jq -r .text` needed, content-type is `text/plain`.
5. **One active model family at a time** — every transcribe request evicts other loaded models. Multiple live streams may share one pinned model up to `TALKIES_STREAM_MAX_CONNECTIONS`; a request or stream for a different model receives a conflict until the streams end. Use two containers if you need concurrent models.
6. **`POST /unload` after a job** — explicit eviction frees VRAM/RAM faster than waiting for the 10-min idle sweeper. Useful in CI / batch scripts.
7. **`canary-qwen-2.5b` has no timestamps** — `verbose_json.segments` / `.words` come back empty, `srt`/`vtt` collapse to one cue. Use a Whisper or Canary multitask slug if you need timing data.
8. **Diarization requires true stereo** — if your "stereo" file is the same mono signal copied to both channels, diarization won't separate speakers. The technique is exact for two-mic setups, useless otherwise.
9. **Long files just work** — VAD chunking happens transparently. Don't pre-split. Send the whole file.
10. **ASR's `prompt` / `temperature` are ignored** even though the request schema accepts them. TTS's `instructions` is different — Kokoro ignores it, but Qwen3-TTS honors it in `base` mode and `*-custom` (except the 0.6B checkpoint) and requires it for `*-design`.
11. **Watch `/api/ps`** to see what's resident. A request that hangs at "loading model" is doing the first cold load — subsequent calls are fast.
12. **Customizing the model registry** for translation slugs or to restrict the served set — see [references/setup.md](references/setup.md#customizing-the-model-registry).
13. **Kokoro uses native voice names** — no OpenAI aliases. Hit `GET /v1/audio/voices` once to discover what's shipped; pass the `voice` field accordingly. The 41 voices cover en (US + UK), es, fr, hi, it, pt; ja/zh are filtered out.
14. **Voice cloning is `qwen3-tts-0.6b`** — drop a `.wav` (10-30 s of clean speech is plenty) into `/data/custom-voices/<anywhere>.wav`. Optionally drop a sibling `.txt` with a faithful transcript for higher clone fidelity. The voice appears in `GET /v1/audio/voices` on the next request — no restart. CUDA required.
15. **Qwen3-TTS first synth is slow** — CUDA graph capture runs once after model load (~30-60 s). Subsequent synths are sub-second. If you're benchmarking, throw away the first call.
16. **Qwen3-TTS ignores `speed`** — the model has no playback-rate control. Pass it for OpenAI compat; nothing happens. Only Kokoro honors `speed`.
17. **Both TTS engines emit 24 kHz mono PCM** — Kokoro and Qwen3-TTS both output int16 24 kHz mono. ffmpeg re-encodes into your chosen `response_format`; `pcm` (raw, no container) hands back that same rate directly — check the `X-Sample-Rate` response header on Qwen3-TTS streaming responses if you need it confirmed per-request.
18. **TTS `response_format=pcm` is for chaining** — raw int16 mono PCM, no container, no header. Use it when piping into another encoder or a real-time playback path. Otherwise stick with `mp3` (default) or `opus` for size.
19. **TTS evicts loaded ASR and vice versa** — they share the same one-model-resident pool. Synthesizing with Kokoro after a transcribe burst incurs Kokoro's cold load. Same applies to Qwen3-TTS (plus the CUDA-graph capture re-runs on cold reload).
