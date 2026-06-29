# OpenClaw Voice Bridge

Push-to-talk voice input for OpenClaw, triggered by a hardware button on the Snarling display. Records audio from a USB microphone, transcribes via OpenAI Whisper, and delivers the transcript to your agent — which answers and pushes the result back to the display.

## How It Works

```
┌─────────────┐    POST /transcribe-and-reply    ┌──────────────────────┐
│  Snarling    │ ──────────────────────────────▶ │  Voice Bridge Plugin │
│  X Button    │     { wav_path: "/tmp/..." }    │                      │
│  Display     │ ◀─── { status: "transcribing" } │  1. Resolve API key  │
└─────────────┘                                  │  2. Transcribe WAV   │
       │                                         │  3. subagent.run()   │
       │  arecord (in snarling thread)           └──────────┬───────────┘
       │  20s @ 24kHz mono                                   │
       ▼                                                     ▼
┌─────────────┐                                  ┌──────────────────────┐
│  WAV file    │ ──────────────────────────────▶ │  Isolated Agent Turn │
│  /tmp/voice_ │                                  │                      │
│  recording.* │                                  │  Answers question    │
└─────────────┘                                  │  send_notification   │
                                                 │  to Snarling display │
                                                 └──────────┬───────────┘
                                                            │
                                                            ▼
                                                 ┌──────────────────────┐
                                                 │  Snarling Display    │
                                                 │  Notification shown  │
                                                 │  (no A/B buttons)    │
                                                 └──────────────────────┘
```

### Flow

1. Press **X** on the Snarling display
2. Snarling starts `arecord` immediately in a background thread (82ms latency)
3. After recording completes, Snarling POSTs the WAV path to `/transcribe-and-reply`
4. The plugin transcribes via `gpt-4o-mini-transcribe` (~2s)
5. The plugin calls `api.runtime.subagent.run()` with the transcript
6. The subagent answers the question and sends the result to Snarling via the `send_notification` tool
7. The answer appears on the Snarling display as a notification

### Why subagent.run?

Previous approaches using `enqueueSystemEvent` + heartbeat wake were unreliable. The system event would enqueue and the heartbeat would report `status=ran`, but the event text never surfaced in the agent's context during the heartbeat turn (phantom heartbeat bug #86090). CLI-based injection via `openclaw system event --mode now` either deadlocked the event loop (`execSync`) or completed successfully but still didn't surface the event.

`subagent.run` creates a real agent turn that can execute tools — the subagent uses `send_notification` to deliver the answer directly to the Snarling display, bypassing the broken heartbeat wake path entirely.

## Hardware

| Component | Notes |
|-----------|-------|
| **Computer** | Raspberry Pi 4 or higher (recommended) |
| **Display** | Pimoroni Display HAT Mini (320×240 IPS) |
| **Microphone** | USB PnP Sound Device (`plughw:3,0`) |
| **Audio format** | 24kHz, 16-bit little-endian, mono (WAV) |
| **Trigger** | X button on Snarling display |

The USB mic plugs directly into the Pi. The Pimoroni Display HAT Mini sits on the Pi's GPIO header and runs the Snarling software, which renders the UI and handles button input.

## Button Mapping

| Button | Normal State | Approval State | Notification State |
|--------|-------------|----------------|-------------------|
| **X** | 🎙️ Voice input | — | — |
| **Y** | 💤 Sleep mode | — | — |
| **B** | No-op | ❌ Reject | ✕ Dismiss |
| **A** | — | ✅ Approve | 👁️ Reveal |

The X button only triggers voice input when no approval or notification is active. This prevents accidental recording during A/B interactions.

## Architecture: Snarling Owns Recording

In v3+, Snarling handles the recording directly in its own thread rather than delegating to the plugin. This eliminates front-clipping caused by gateway event loop blocking during agent turns.

**Old flow (v1-v2):** X press → HTTP POST to plugin → plugin starts arecord → transcribe → inject
**New flow (v3+):** X press → arecord in snarling thread → POST wav_path to plugin → plugin transcribes → subagent.run → answer to display

Snarling's `trigger_voice_input()` method records audio and POSTs the file path after recording completes. The plugin handles transcription and delivery only.

## Installation

### 1. Install the plugin

```bash
openclaw plugins install clawhub:openclaw-voice-bridge
```

Or clone from GitHub and link manually:

```bash
git clone -b development https://github.com/snarflakes/OpenClaw-Voice-Bridge.git \
  ~/.openclaw/extensions/openclaw-voice-bridge
```

### 2. Enable the plugin in `openclaw.json`

```json
{
  "openclaw-voice-bridge": {
    "enabled": true,
    "config": {},
    "hooks": {
      "allowConversationAccess": true
    }
  }
}
```

> ⚠️ **`hooks.allowConversationAccess: true` is required** (v2026.5.18+). Without it, the plugin loads lazily and its HTTP routes are invisible to the gateway's HTTP server.

### 3. Environment variables

The plugin needs:

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Transcription API access (resolved via OpenClaw auth runtime) |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth (declared in manifest `envVars`) |

The OpenAI key is resolved at runtime via `api.runtime.modelAuth.resolveApiKeyForProvider` — no need to hardcode it.

### 4. Verify your mic

```bash
arecord -l
```

You should see your USB device listed. The default device is `plughw:3,0` — if yours differs, set it in Snarling's config (snarling handles the recording, not the plugin).

Quick test:

```bash
arecord -D plughw:3,0 -f S16_LE -c 1 -r 24000 -d 5 /tmp/test.wav
```

### 5. Restart the gateway

```bash
systemctl --user restart openclaw-gateway
```

SIGUSR1 hot-reload only reloads config, not plugin code. A full process restart is required after installation or code changes.

## Configuration

All config lives in `openclaw.json` under the `openclaw-voice-bridge.config` key:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `transcriptionModel` | string | `gpt-4o-mini-transcribe` | OpenAI transcription model |

Recording settings (duration, mic device) are controlled by Snarling, not the plugin, since Snarling owns the recording pipeline.

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/transcribe-and-reply` | POST | gateway token | Receives `{wav_path}`, transcribes, spawns subagent, delivers answer to Snarling |
| `/audio-status` | GET | gateway token | Returns `{version, transcriptionModel, authAvailable}` |
| `/start-listening` | POST | gateway token | Deprecated — returns 410 with migration hint |

### Trigger a transcription manually

```bash
curl -X POST http://localhost:18789/transcribe-and-reply \
  -H "Authorization: Bearer <gateway-token>" \
  -H "Content-Type: application/json" \
  -d '{"wav_path": "/tmp/recording.wav"}'
```

## Notification Delivery

The subagent sends answers to the Snarling display using the `send_notification` tool:

```json
{
  "type": "notification",
  "message": "You said 7 numbers!",
  "priority": "normal",
  "secret": "voice-bridge"
}
```

- `type: "notification"` — displays as a notification (no A/B buttons)
- No `duration` — stays on display until manually dismissed
- The secret authenticates with Snarling (shared between plugin and display)

## Transcription Models

| Model | Latency | Cost/20s | Quality | Best Use |
|-------|---------|----------|---------|----------|
| `gpt-4o-mini-transcribe` | ~2s | ~$0.006 | Very good | Default — best value |
| `gpt-4o-transcribe` | ~3-5s | ~$0.012 | Best | Noisy environments |
| `whisper-1` | ~3-5s | ~$0.012 | Good | Legacy, timestamps |

## Troubleshooting

### Voice input reaches Snarling but no answer appears

Check `/tmp/voice-bridge-debug.log` for the pipeline status:

```bash
tail -20 /tmp/voice-bridge-debug.log
```

Key lines to look for:
- `Transcript: "..."` — transcription succeeded
- `Spawning subagent for voice input` — subagent.run called
- `Subagent spawned: runId=...` — subagent created
- `Subagent wait: status=ok` — subagent completed successfully

If you see `subagent.run not available`, the plugin fell back to the broken heartbeat path — check that the plugin is running on a recent OpenClaw version that exposes `api.runtime.subagent`.

### `/transcribe-and-reply` returns 404

The plugin isn't loading at startup. Add `hooks.allowConversationAccess: true` to its config in `openclaw.json`. Requires gateway restart.

### Voice transcript is empty or cut off

- Check mic volume: `alsamixer -c 3` (card number from `arecord -l`)
- Test directly: `arecord -D plughw:3,0 -f S16_LE -c 1 -r 24000 -d 5 /tmp/test.wav && aplay /tmp/test.wav`
- Snarling records for a fixed duration (default 20s) — if you speak too quickly after pressing X, the beginning may be captured

### Notification shows as approval (A/B buttons) instead of plain text

The `send_notification` tool automatically formats the notification correctly. If `subagent.run` is unavailable, the plugin falls back to `enqueueSystemEvent` (which may not deliver reliably — see phantom heartbeat bug #86090). There is no curl fallback path.

### esbuild rebuild breaks transcription

⚠️ **Do not rebuild `index.mjs` from `index.ts` via esbuild.** The esbuild output differs subtly from the hand-curated version and breaks transcription. Apply patches surgically to `index.mjs` directly.

## Performance

| Stage | Typical latency |
|-------|----------------|
| X press → arecord starts | ~82ms |
| Recording (fixed duration) | 20s |
| Snarling POSTs WAV to plugin | ~50ms |
| API key resolution (cached) | ~1ms |
| OpenAI transcription | ~2s |
| Subagent run + answer + send_notification | ~3-5s |
| **Total round trip** | **~25s** |

First recording after restart may add ~5s for API key cache warming.

## v2026.5.18 Compatibility

OpenClaw v2026.5.18 introduced breaking changes requiring manifest updates:

1. **`contracts.tools` required** — plugins must declare tool names before `api.registerTool()` succeeds. This plugin declares `"contracts": { "tools": [] }` (no tools, only HTTP routes).
2. **`hooks.allowConversationAccess` required** — without this config, the plugin loads lazily and its HTTP routes are invisible to the server.
3. **Schema defaults override code defaults** — if the manifest config schema has `"default": X`, it overrides `const FOO = Y` in the code. Keep both in sync.

## Privacy

⚠️ **Audio is sent to OpenAI for transcription.** When you press X, the recorded audio (WAV file) is transmitted to OpenAI's Whisper API (`api.openai.com/v1/audio/transcriptions`) for speech-to-text conversion. OpenAI may retain transcribed text per their API data retention policy.

- **What's sent:** The raw WAV audio recording (~20 seconds)
- **Where it goes:** OpenAI's servers (US-based)
- **What's retained:** Check [OpenAI's API data usage policy](https://openai.com/policies/api-data-usage/)
- **Local data:** The WAV file is deleted after transcription. Debug logs (if enabled) do not contain audio or full API keys.

To avoid sending audio to OpenAI, you can use a local transcription model by changing the `transcriptionModel` config — but this requires a self-hosted Whisper endpoint.

## License

MIT

## Links

- **GitHub**: https://github.com/snarflakes/OpenClaw-Voice-Bridge
- **ClawHub**: https://clawhub.ai/skills/openclaw-voice-bridge
- **Snarling Display**: https://github.com/snarflakes/snarling