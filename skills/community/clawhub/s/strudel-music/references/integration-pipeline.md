# Strudel Integration Pipeline — Offline Rendering to Discord VC

## Architecture

```
Agent                     Node.js Renderer              Audio Pipeline
┌──────────┐  pattern.js  ┌──────────────────┐  WAV    ┌────────────┐
│ Generate  │ ──────────→ │ node-web-audio   │ ─────→ │ ffmpeg     │
│ pattern   │             │ OfflineAudio     │        │ WAV → MP3  │
│ from mood │             │ Context          │        └─────┬──────┘
│ params    │             │                  │              │ MP3/Opus
└──────────┘             │ offline-render   │              ▼
                          │ -v2.mjs          │        ┌────────────┐
                          └──────────────────┘        │ Discord VC │
                                                      │ via        │
                                                      │ vc-play.mjs│
                                                      └────────────┘
```

All rendering is local and offline via `node-web-audio-api` (Rust/C++ Web Audio
implementation for Node.js). No browser, no Puppeteer, no remote code execution.

## Key Components

### 1. Offline Renderer — `src/runtime/offline-render-v2.mjs`

Evaluates a Strudel composition file, schedules haps into an `OfflineAudioContext`,
and writes the result to a WAV file.

```bash
node src/runtime/offline-render-v2.mjs <composition.js> <output.wav> <cycles> [bpm]
```

**Security hardening during pattern evaluation:**
- `process.env` is frozen (only `NODE_ENV=production` visible)
- `child_process` module is blocked
- Environment restored after evaluation completes

⚠️ **Session safety:** The renderer blocks the Node.js event loop. Always run
in a sub-agent or background exec — never inline in the main gateway session.

### 2. Audio Conversion

```bash
# WAV → MP3 (general purpose)
ffmpeg -i output.wav -c:a libmp3lame -q:a 2 output.mp3

# WAV → Opus (Discord native, low latency)
ffmpeg -i output.wav -c:a libopus -b:a 128k -ar 48000 output.opus

# WAV → 48kHz stereo (for VC streaming)
ffmpeg -i output.wav -ar 48000 -ac 2 output-48k.wav
```

### 3. Discord VC Streaming — `scripts/vc-play.mjs`

Streams a rendered WAV file into a Discord voice channel using the platform
gateway's existing authenticated connection. No separate bot token required.

### 4. Command Dispatcher — `scripts/dispatch.sh`

Routes `/strudel` subcommands (render, play, list, samples, concert).
All user inputs are validated before use — composition names restricted to
`[a-zA-Z0-9_-]`, channel IDs and numeric args validated as numeric-only.

## Rendering Modes

| Mode | Approach | Latency | Use Case |
|------|----------|---------|----------|
| Batch | offline-render-v2.mjs → WAV → convert | 5-30s | Pre-rendered compositions, exports |
| Chunked | chunked-render.mjs → WAV (low memory) | 10-60s | Long compositions, memory-constrained hosts |

For agent-driven use cases, **batch rendering** is the standard path.
Chunked rendering handles long pieces without OOM on constrained hardware.

## Sample Management

Default samples: `github:tidalcycles/dirt-samples` (CC-licensed, ~11MB).
Downloaded automatically by `scripts/download-samples.sh`.

Custom samples:
```javascript
samples('local:')  // loads from local ./samples/ directory
```

For domain-specific atmospheres, create sample packs — directories of `.wav`
files organized by name. See `scripts/samples-manage.sh` for pack management.
