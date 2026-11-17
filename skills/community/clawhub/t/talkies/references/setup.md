# talkies setup

## Requirements

- Docker
- `linux/amd64` host (no arm64 images — `nemo_toolkit[asr]` + chain doesn't resolve cleanly on aarch64)
- Optional: NVIDIA GPU + NVIDIA Container Toolkit for the CUDA image (required for `qwen3-tts-0.6b` voice cloning)
- ~3 GB disk for the CPU image, ~11 GB for the CUDA image
- Additional disk for selected model weights; set `TALKIES_ENABLED_MODELS` to avoid downloading the full registry
- ~4 GB RAM minimum (whisper-large-v3 needs the working set + overhead); 12 GB+ VRAM for the GPU-only models

## Quick Install

### CPU

Serves 2× Whisper + `canary-180m-flash` + `nemotron-3.5-asr-0.6b` (CPU-optimized, via parakeet.cpp), four selectable Sherpa Zipformer variants, and `vosk-small-en-us-0.15` for ASR, plus `kokoro-82m` and `kokoro-82m-nvidia` for TTS. The CUDA-only ASR models aren't worth running on CPU, and the Qwen3-TTS family is CUDA-only.

```bash
docker run -d --name talkies \
  -v $HOME/talkies-data:/data \
  -p 127.0.0.1:8000:8000 \
  psyb0t/talkies:latest
```

### CUDA

Serves all fourteen ASR models plus all three TTS engines / 4 backends (`kokoro-82m`, `kokoro-82m-nvidia`, the 5 Qwen3-TTS slugs, and `chatterbox-turbo`). Requires the NVIDIA Container Toolkit on the host.

Nemotron runs through the SHA-256-pinned upstream parakeet.cpp v0.5.0 CUDA 12
bundle in this image, so both file transcription and native WebSocket sessions
use GPU offload. The matching CUDA 12.9 runtime libraries stay isolated under
`/opt/parakeet` from the image's Python ML stack.

```bash
docker run -d --name talkies \
  --gpus all \
  -v $HOME/talkies-data:/data \
  -p 127.0.0.1:8000:8000 \
  psyb0t/talkies:latest-cuda
```

The CUDA image expects `--gpus all`. Without a GPU assignment it retains its
`TALKIES_DEVICE=cuda` image default, so model loading fails rather than silently
falling back. To use its CPU-compatible subset for debugging, explicitly set
`-e TALKIES_DEVICE=cpu` and restrict `TALKIES_ENABLED_MODELS` to CPU-compatible
slugs; GPU-only Qwen3-TTS slugs remain unavailable.

**Verify:** `curl http://localhost:8000/healthz` returns `{"ok": true, "device": "...", "models": [...]}` once boot's done.

**First boot:** the entrypoint downloads every enabled model into `/data/models/<slug>/` and creates `/data/files/` + `/data/custom-voices/`. Bind-mount `/data` so subsequent restarts are no-ops. Restrict the download set with `TALKIES_ENABLED_MODELS` to avoid pulling everything.

## CPU vs CUDA Images

| Image | Tag | Platforms | Models served | Image size |
|---|---|---|---|---|
| CPU | `psyb0t/talkies:latest` | `linux/amd64` | 2× Whisper, Canary-180m-Flash, Nemotron-3.5-ASR, Sherpa Zipformer ×4, Vosk, wav2vec2 + ZIPA phoneme, Kokoro-82M ×2 runtimes | ~3 GB |
| CUDA | `psyb0t/talkies:latest-cuda` | `linux/amd64` | all fourteen ASR + Kokoro-82M ×2 runtimes + Qwen3-TTS ×5 + Chatterbox Turbo | ~11 GB |

The CPU image only ships ASR models that actually finish in a sane time without a GPU. Parakeet-TDT is autoregressive (slow on CPU). Canary-1B and Canary-Qwen-2.5B need the CUDA image with `--gpus all`; use the CPU image for CPU workloads. Kokoro-82M ships in both images — at 82M params it synthesizes faster than real-time on a 4-core CPU, no GPU needed. Chatterbox Turbo is CUDA-only for the same reason as the heavier ASR models: it runs on CPU but measures roughly 5-10x slower than real-time, so it is not registered as a CPU slug.

Both images bake `espeak-ng` into the runtime layer because Kokoro's G2P for es/fr/hi/it/pt routes through it via `misaki.espeak.EspeakG2P`. The Python `kokoro==0.9.4` package and its lightweight dependency chain (`misaki`, no `[ja]` / `[zh]` extras) are pinned alongside the rest of the ML stack in `Dockerfile` / `Dockerfile.cuda`.

The CUDA image additionally bakes the `faster-qwen3-tts==0.2.6` MIT wrapper and three builtin Qwen3 reference voices (`alloy`, `echo`, `fable`) under `/opt/talkies/qwen3-voices/`. The model weights (`Qwen/Qwen3-TTS-12Hz-0.6B-Base`, Apache-2.0) are downloaded into `/data/models/qwen3-tts-0.6b/` at first boot like every other model.

The CUDA image also bakes `chatterbox-tts==0.1.7` (MIT) and `s3tokenizer==0.3.0` (Apache-2.0) from a separate hash-pinned `requirements-chatterbox.txt`, installed `--no-deps` because their declared dependency metadata conflicts with the image's pinned torch/transformers and pulls tooling that has no place in a runtime image. The `ResembleAI/chatterbox-turbo` weights (MIT, ungated) land in `/data/models/chatterbox-turbo/` at first boot. Its voices come from `/data/custom-voices/` plus a `builtin` speaker shipped inside the checkpoint — the Qwen3 reference voices are deliberately not shared with it, since several are shorter than its 5-second reference-clip minimum.

## Environment Variables

### Auth + bind

| Var | Default | What it does |
|---|---|---|
| `TALKIES_AUTH_TOKEN` | (empty = no auth) | Bearer token required on every route except `/healthz`. Empty/unset = wide open (historical default — fine on private networks). When set, `Authorization: Bearer <token>` required on every HTTP request AND every MCP call. Compared with `hmac.compare_digest`. |

Container binds `0.0.0.0:8000` unconditionally. Control network exposure at `docker run` time:
- `-p 127.0.0.1:8000:8000` — loopback-only on the host.
- `-p 8000:8000` — all host interfaces.
- For untrusted networks, combine the token with a reverse proxy doing TLS + rate limiting.

### Device + model registry

| Var | Default | What it does |
|---|---|---|
| `TALKIES_DEVICE` | image default (`cpu` CPU / `cuda` CUDA) | `auto` picks `cuda` if available else `cpu`; it is an accepted override. Pin to a specific GPU with `cuda:N`. |
| `TALKIES_MODELS_FILE` | `/app/models.json` | Path to the model registry JSON. Override to ship a custom subset. The CPU image copies `models-cpu.json` to this path; the CUDA image copies `models.json` here. |
| `TALKIES_ENABLED_MODELS` | (empty = all from `models.json`) | Comma-separated slug whitelist. Restricts both the boot-time snapshot download and the queryable surface of `/v1/models`. Unknown slugs fail fast on startup. |
| `TALKIES_PRELOAD` | (empty) | Comma-separated slugs to load into RAM/VRAM at boot, before uvicorn accepts requests. Skips cold-load on first transcription. Must be a subset of `TALKIES_ENABLED_MODELS`. |
| `TALKIES_MODEL_MAX_CONCURRENCY` | `1` | Fallback number of simultaneous inference requests admitted per model across HTTP, MCP, WebSocket ASR, buffered TTS, and streaming TTS. Registry `max_concurrency` values take precedence. |
| `TALKIES_MODEL_CONCURRENCY` | (empty) | Comma-separated `model-slug=limit` overrides, for example `nemotron-3.5-asr-0.6b=2,kokoro-82m=4`. Unknown, disabled, duplicate, malformed, or out-of-range entries fail at startup. |

Each registry model may define `max_concurrency` from 1 through 1024. The
bundled Nemotron entry defaults to two in both images. Only one model may own
active inference slots at a time, which prevents sibling model eviction while
a request is still using its backend.

### Data dir

| Var | Default | What it does |
|---|---|---|
| `TALKIES_DATA_DIR` | `/data` | Base data dir. Model snapshots → `$TALKIES_DATA_DIR/models/<slug>/` (flat per-model dirs, no HF cache layout). Staged uploads + URL downloads → `$TALKIES_DATA_DIR/files/`. Qwen3-TTS custom clone voices → `$TALKIES_DATA_DIR/custom-voices/` (nested subdirs preserved as voice names). Bind-mount to persist across restarts. |

**Security note on `$TALKIES_DATA_DIR/files/`:** staged uploads and cached URL downloads persist here **indefinitely** — nothing auto-expires them — and are enumerable by any caller via `GET /v1/files` (no per-caller isolation; see [Server-Side File Staging](../SKILL.md#server-side-file-staging-v1files) in SKILL.md). This is a shared bucket: an agent must only read/delete paths it staged itself, must never enumerate or delete other callers' files, and should clean up after its own workflow. Deploy with `TALKIES_AUTH_TOKEN` set by default, add per-caller isolation and retention limits at the deployment/proxy level if the deployment isn't fully trusted, and least-privilege network exposure otherwise.

### Lifecycle (idle sweeper + load timeouts)

| Var | Default | What it does |
|---|---|---|
| `TALKIES_MODEL_TTL` | `600` (10 min) | Idle time before a loaded backend is unloaded by the sweeper. Bare number = seconds; also accepts Go-style `3h30m5s`, `45m`, `90s`. `0` disables auto-unload. |
| `TALKIES_SWEEPER_INTERVAL` | `60` | How often the sweeper checks for idle models. |
| `TALKIES_LOAD_TIMEOUT` | `300` | Parsed configuration reserved for a future model-load timeout; the current server does not apply it. |

### Upload + download caps

| Var | Default | What it does |
|---|---|---|
| `TALKIES_MAX_UPLOAD_BYTES` | `104857600` (100 MB) | Reject `POST /v1/audio/transcriptions` multipart `file` and `PUT /v1/files/{path}` bodies larger than this with 413. |
| `TALKIES_MAX_DOWNLOAD_BYTES` | `1073741824` (1 GiB) | Abort URL downloads (when `file_path` is an http(s) URL) larger than this. Larger default because downloads stream straight to disk, no in-memory buffering. |
| `TALKIES_BLOCK_PRIVATE_DOWNLOADS` | `false` | Set to `true` to refuse URL downloads whose hostname resolves to private/loopback/link-local/multicast/reserved IPs. Default `false` because the typical self-hosted deployment is a LAN box fetching from another LAN box. Flip to `true` if exposed to untrusted clients. |

### VAD knobs

Audio longer than `TALKIES_VAD_CHUNK_THRESHOLD` seconds gets sliced through Silero VAD into ≤`TALKIES_VAD_MAX_SPEECH`-second speech regions before being handed to the backend.

| Var | Default | What it does |
|---|---|---|
| `TALKIES_VAD_CHUNK_THRESHOLD` | `30.0` | Audio longer than this (seconds) goes through VAD chunking. Shorter clips skip it. |
| `TALKIES_VAD_MAX_SPEECH` | `28.0` | Max length of a single VAD-detected speech region (seconds). Should stay under Whisper's 30 s internal window. |
| `TALKIES_VAD_MIN_SILENCE_MS` | `500` | Silero VAD param — minimum gap (ms) to consider a region break. |
| `TALKIES_VAD_SPEECH_PAD_MS` | `200` | Silero VAD param — silence padding (ms) around each detected speech region. |
| `TALKIES_VAD_THRESHOLD` | `0.5` | Silero VAD speech-probability threshold. Lower = more aggressive. |

### Live ASR streaming

`WS /v1/audio/transcriptions/stream` accepts headerless 16 kHz mono PCM16LE.
It is separate from the OpenAI-compatible upload route. See the repository's
[`docs/streaming.md`](https://github.com/psyb0t/docker-talkies/blob/main/docs/streaming.md)
for the protocol and client examples.

| Var | Default | What it does |
|---|---|---|
| `TALKIES_STREAM_MAX_CONNECTIONS` | `4` | Maximum active ASR WebSockets per container. Streams may share one pinned model; attempts to switch models while one is active return a conflict. |
| `TALKIES_STREAM_MAX_FRAME_BYTES` | `65536` | Maximum binary PCM frame size. Frames must be non-empty, contain whole 16-bit samples, and be 2–16777216 bytes. |
| `TALKIES_STREAM_MAX_BUFFER_SECONDS` | `5` | Faster-whisper rolling-window budget. Must hold one configured maximum-size frame; native decoders process each frame directly. |
| `TALKIES_STREAM_IDLE_TIMEOUT` | `30s` | Maximum wait between client messages before close code 4408. |
| `TALKIES_STREAM_MAX_DURATION` | `4h` | Maximum accepted audio duration per WebSocket. |

### Qwen3-TTS streaming

| Var | Default | What it does |
|---|---|---|
| `TALKIES_QWEN3_STREAM_CHUNK_SIZE` | `8` | Codec steps decoded per yielded chunk when `response_format=pcm` streams from a `qwen3_tts` backend (~1 s of audio per 12 steps). Only relevant to that streaming path. |

### Logging

| Var | Default | What it does |
|---|---|---|
| `TALKIES_LOG_LEVEL` (falls back to `LOG_LEVEL`) | `info` | `debug` / `info` / `warn` / `error` / `fatal` (case-insensitive; `warning` / `critical` also accepted). Unrecognized values fail fast at startup. JSON structured logs on stdout. **`debug` logs full request/response bodies** (TTS input text, cloned-voice reference transcripts, ASR transcripts) — PII; a one-time WARNING fires at startup when active. |

### Internal

| Var | Default | What it does |
|---|---|---|
| `HF_HUB_OFFLINE` | `1` (in image) | Refuse network calls from HuggingFace Hub at runtime. The entrypoint transparently unsets it for the one-shot prefetch step so the initial download works; the server process itself runs offline. Don't touch unless debugging. |

## Common Configurations

```bash
# Restrict to just the small/fast models (saves first-boot download time).
docker run -d -p 127.0.0.1:8000:8000 \
  -e TALKIES_ENABLED_MODELS=whisper-large-v3-turbo,canary-180m-flash \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest

# Preload at boot so the first request doesn't pay the cold-load tax.
docker run -d -p 127.0.0.1:8000:8000 \
  -e TALKIES_ENABLED_MODELS=whisper-large-v3-turbo \
  -e TALKIES_PRELOAD=whisper-large-v3-turbo \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest

# Bearer auth on a public-facing deployment.
docker run -d -p 8000:8000 \
  -e TALKIES_AUTH_TOKEN=$(openssl rand -hex 32) \
  -e TALKIES_BLOCK_PRIVATE_DOWNLOADS=true \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest

# Loopback only (rely on reverse proxy for external access).
docker run -d -p 127.0.0.1:8000:8000 \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest

# Disable auto-unload (keep model resident forever).
docker run -d -p 127.0.0.1:8000:8000 \
  -e TALKIES_MODEL_TTL=0 \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest

# Bump upload + download caps for huge files.
docker run -d -p 127.0.0.1:8000:8000 \
  -e TALKIES_MAX_UPLOAD_BYTES=1073741824 \
  -e TALKIES_MAX_DOWNLOAD_BYTES=10737418240 \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest

# Pin to a specific GPU on a multi-GPU host.
docker run -d --gpus '"device=1"' -p 127.0.0.1:8000:8000 \
  -e TALKIES_DEVICE=cuda:0 \
  -v $HOME/talkies-data:/data \
  psyb0t/talkies:latest-cuda
```

## Ports

| Port | Service |
| ---- | ------- |
| 8000 | HTTP API + MCP (`/v1/mcp`) on the same port |

Container binds `0.0.0.0:8000` unconditionally — there are no `TALKIES_HOST` / `TALKIES_PORT` env vars (they were removed in v0.2.0). Use `-p` at `docker run` time for whatever host port mapping you want.

## Customizing the Model Registry

The image ships with `models.json` (CUDA) or `models-cpu.json` (CPU) baked in. Override without rebuilding by bind-mounting your own:

```bash
docker run -d --name talkies \
  -v $HOME/talkies-data:/data \
  -v $PWD/my-models.json:/app/models.json:ro \
  -p 127.0.0.1:8000:8000 \
  psyb0t/talkies:latest
```

Or point `TALKIES_MODELS_FILE` at a different path inside the container.

File structure:

```json
{
  "models": {
    "your-asr-slug": {
      "repo": "huggingface-org/repo-name",
      "executor": "whisper",
      "default_source_lang": "en",
      "default_target_lang": "en",
      "default_task": "asr",
      "languages": ["en"]
    },
    "your-tts-slug": {
      "repo": "huggingface-org/tts-repo-name",
      "executor": "kokoro",
      "modality": "tts",
      "default_voice": "af_heart",
      "languages": ["en"]
    }
  }
}
```

| Field | Required | Notes |
|---|---|---|
| `repo` | yes | HuggingFace repo id. Pulled via `snapshot_download(local_dir=$TALKIES_DATA_DIR/models/<slug>)` — flat directory keyed by slug, no HF cache indirection. |
| `revision` | no | Immutable Hugging Face commit SHA to download. Pin this for reproducible custom registries. |
| `executor` | yes | One of `whisper`, `parakeet`, `parakeet_cpp`, `canary_multitask`, `canary_salm`, `sherpa`, `sherpa_offline_ctc`, `vosk`, `kokoro`, `kokoro_nvidia`, `qwen3_tts`, `chatterbox`, `wav2vec2_phoneme`. Other values fail startup — the allowlist is `VALID_EXECUTORS` in `src/talkies/config.py`, and `load_registry()` runs at server import, so an unknown executor stops the whole process rather than disabling one model. |
| `modality` | no | `asr` (default) or `tts`. Drives endpoint guards (`/v1/audio/transcriptions` requires ASR; `/v1/audio/speech` requires TTS) and the `modality` field on `/v1/models` entries. The `kokoro`, `qwen3_tts` and `chatterbox` executors imply `tts`; the seven ASR executors imply `asr`. |
| `download_patterns` | no | Non-empty list of static repository-relative paths passed to Hugging Face `snapshot_download(..., allow_patterns=...)`. Use it to limit a multi-variant repository to the files selected by this registry entry. |
| `default_source_lang` | no | ASR only. Used when the request omits `language`. |
| `default_target_lang` | no | ASR only. Used by Canary multitask for translation tasks. |
| `default_task` | no | ASR only. `asr` (transcribe) or `s2t_translation` (Canary multitask only). Default `asr`. |
| `default_voice` | no | TTS only. Used when the request omits `voice`. Falls back to the first voice the backend reports. For `qwen3_tts`, the voice name is a path relative to the voices dir (`alloy`, `team-a/jane`). |
| `default_language` | no | `qwen3_tts` only. Default reference-clip language label (defaults to `English`). Overridden per-voice by a sibling `.lang` file next to the wav. |
| `languages` | no | Informational only — listed in error messages, not enforced. |
| `dependencies` | no | List of extra HuggingFace repo ids the executor needs at load time (e.g. `canary-qwen-2.5b` instantiates a Qwen3 tokenizer separately). Each is `snapshot_download`'d into the standard HF cache (`HF_HOME`) at entrypoint. |

### Common customization: translation slugs

The shipped `models.json` ships every Canary slug with `default_task=asr`, so out of the box the API only transcribes. To enable translation (Canary-1B-Flash covers en↔de/fr/es), add a translation-specific slug:

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
    },
    "canary-1b-flash-en2de": {
      "repo": "nvidia/canary-1b-flash",
      "executor": "canary_multitask",
      "default_source_lang": "en",
      "default_target_lang": "de",
      "default_task": "s2t_translation",
      "languages": ["en"]
    }
  }
}
```

Multiple slugs can point at the same HF repo — talkies loads the underlying weights once and changes the prompt format per slug.

### Common customization: restricting to one model

For a single-purpose deployment, ship a one-entry registry to skip pulling everything:

```json
{
  "models": {
    "whisper-large-v3-turbo": {
      "repo": "deepdml/faster-whisper-large-v3-turbo-ct2",
      "executor": "whisper",
      "default_source_lang": "en",
      "languages": ["en"]
    }
  }
}
```

Equivalent to setting `TALKIES_ENABLED_MODELS=whisper-large-v3-turbo` against the default registry — but with a custom registry you can add slugs that aren't in the shipped one.

## Qwen3-TTS Custom Voices

**Acceptable use:** only supply reference voice samples you're authorized to process, and only with the speaker's informed consent. Voice cloning reproduces someone's actual timbre/prosody — never use it to impersonate a real person without consent, or for fraud, deception, or any form of unauthorized voice replication.

`qwen3-tts-0.6b` is a voice-cloning TTS — it takes a reference `.wav` and clones the speaker's timbre / prosody onto whatever text you supply. The voice catalog is built from two on-disk dirs that are merged at request time (live, no restart):

| Dir | Where it lives | Origin tag | Purpose |
|---|---|---|---|
| Builtin | `/opt/talkies/qwen3-voices/` (baked into the CUDA image) | `builtin` | Three curated samples (`alloy`, `echo`, `fable`) so the model works out of the box. |
| Custom | `/data/custom-voices/` (host-mounted) | `custom` | Your reference clips. Drop in, get back. |

Voice names are the wav's path relative to the parent dir with `.wav` stripped. Nested subdirs are preserved:

```
$HOME/talkies-data/custom-voices/
├── jane.wav              → voice "jane"
├── jane.txt              # optional reference transcript
├── jane.lang             # optional language label (defaults "English")
└── team-a/
    └── narrator-bob.wav  → voice "team-a/narrator-bob"
```

Custom voices **shadow** builtin voices with the same name — dropping `custom-voices/alloy.wav` overrides the builtin `alloy` (its `origin` field on `/v1/audio/voices` flips from `builtin` to `custom`).

**Sibling metadata** next to each `<name>.wav`:
- `<name>.txt` — reference transcript for the clip. Optional; the model accepts an empty string. Clone fidelity is noticeably better with a faithful transcript.
- `<name>.lang` — language label string passed through to the model. Optional; defaults to `English`. Use this for non-English reference clips.

**Recommended reference clips:**
- 10-30 s of clean speech from the target speaker.
- No background music, no overlapping voices, low noise floor.
- 16+ kHz, mono preferred (model resamples internally but garbage-in-garbage-out applies).

**Use a custom voice:**

```bash
mkdir -p $HOME/talkies-data/custom-voices/team-a
cp jane-reading.wav $HOME/talkies-data/custom-voices/team-a/jane.wav
echo "And the silken sad uncertain rustling of each purple curtain." \
  > $HOME/talkies-data/custom-voices/team-a/jane.txt

curl -s http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen3-tts-0.6b",
        "voice": "team-a/jane",
        "input": "Hello from a cloned voice.",
        "response_format": "wav"
      }' \
  --output cloned.wav
```

**Path-traversal guard:** symlinks under `custom-voices/` whose `resolve()` escapes the dir are skipped at scan time, so a hostile mount can't be used to read arbitrary host files as a voice prompt. Symlinks pointing back into the same dir are fine.

**CUDA only.** Qwen3-TTS hard-fails on CPU (`FasterQwen3TTS.from_pretrained` raises `ValueError`). The model surfaces as `loaded: false` until the first request; first-request load includes CUDA-graph capture (~30-60 s on a mid-range GPU). Subsequent generations are sub-second.

## OpenClaw / ClawHub Config

```bash
export TALKIES_URL=http://localhost:8000
export TALKIES_AUTH_TOKEN=<token>  # only if the server requires it
```

Or via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "talkies": {
        "env": {
          "TALKIES_URL": "http://localhost:8000",
          "TALKIES_AUTH_TOKEN": "<token>"
        }
      }
    }
  }
}
```

## Management

```bash
docker logs -f talkies    # tail logs
docker stop talkies       # stop
docker rm talkies         # remove
docker pull psyb0t/talkies:latest  # update
```

Watch what's loaded right now:

```bash
curl -s http://localhost:8000/api/ps | jq
```

Free memory between jobs:

```bash
curl -s -X POST http://localhost:8000/unload | jq
```

## Logs

`docker logs talkies` covers everything. Look for:

- `entrypoint:` lines on boot — model snapshot downloads, device detection.
- `INFO talkies.server` lines on each request — model load events, transcribe timings.
- `WARNING` / `ERROR` lines for backend failures.

At `info` (default) and above, the server does not log auth tokens, request/response bodies, or audio bytes — it logs the model slug, request id, duration, and result size.

**At `debug`, this changes: full request/response content is logged**, including TTS input text + `instructions`, cloned-voice reference transcripts, and ASR transcripts (`src/talkies/server.py` request/response `log.debug(...)` calls, gated behind `log.isEnabledFor(logging.DEBUG)`). This is PII. A one-time WARNING fires at startup when `TALKIES_LOG_LEVEL=debug` is active (`src/talkies/logging.py`). **Never run `debug` level in production against real user data** — use it only for local troubleshooting with synthetic/throwaway input.

## Public Access via Reverse Proxy (optional)

talkies binds `0.0.0.0:8000` inside the container. For public exposure, terminate TLS at a reverse proxy (Caddy / Traefik / nginx) and combine with `TALKIES_AUTH_TOKEN`.

Caddy example:

```caddy
talkies.example.com {
    reverse_proxy localhost:8000
}
```

Set the auth token on the talkies container so even if Caddy is misconfigured, the upstream still requires `Authorization: Bearer`. Don't rely on the proxy alone.

For Cloudflare Tunnel / Tailscale, the same logic applies — the tunnel provides transport security, the bearer token provides app-layer auth.
