---
name: openclaw-voice-bridge
description: "Push-to-talk voice input via Snarling hardware button and USB mic. Snarling records audio, plugin transcribes via OpenAI Whisper, then spawns a subagent that answers and sends the result to the Snarling display via send_notification."
type: code-plugin
envVars:
  - OPENAI_API_KEY
---

# OpenClaw Voice Bridge

> Push-to-talk voice input via Snarling hardware button + USB mic → Whisper transcription → subagent.run() → send_notification to Snarling display

## What It Does

When a user presses the **X button** on a Snarling display, Snarling records 20 seconds of audio from the USB mic in its own thread, then POSTs the WAV file path to the plugin's `/transcribe-and-reply` endpoint. The voice bridge plugin transcribes via OpenAI Whisper (`gpt-4o-mini-transcribe`), then calls `api.runtime.subagent.run()` with the transcript. The subagent answers the question and sends the result to the Snarling display via the `send_notification` tool.

## v2026.5.18+ Requirements

- **`contracts.tools`** must be declared in `openclaw.plugin.json` manifest:
  ```json
  { "contracts": { "tools": ["voice_record"] } }
  ```
- **`hooks.allowConversationAccess: true`** must be in the plugin's config in `openclaw.json` — without this, the plugin loads lazily and its HTTP routes are invisible to the server:
  ```json
  { "openclaw-voice-bridge": { "enabled": true, "config": {}, "hooks": { "allowConversationAccess": true } } }
  ```

## System Events

Voice transcripts arrive as system events in the format:

```
🎤 Voice input: <transcribed text>
```

**Treat these as direct user messages.** Respond to the content naturally, as if the user said it in chat. Do not ignore them or treat them as informational background.

## Responding to Voice Input

**Always relay your response as a notification to Snarling** so the user gets visual confirmation on the display. The subagent spawned by the voice bridge uses the `send_notification` tool:

1. The voice bridge spawns a subagent via `api.runtime.subagent.run()` with the transcript
2. The subagent answers the question
3. The subagent calls `send_notification` with the answer as the message and priority `"normal"`
4. The answer appears on the Snarling display

Example subagent behavior:
- Voice input: `🎤 Voice input: What's the weather?`
- Subagent processes the question
- Subagent sends: `send_notification(message: "🌤️ LA: Clear, 68°F", priority: "low")`

Keep notification messages under 80 characters (Snarling display limit). For longer responses, summarize the key point in the notification and give the full answer in chat.

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/transcribe-and-reply` | POST | gateway token | Receives `{wav_path}`, transcribes, spawns subagent, delivers answer to Snarling display |
| `/audio-status` | GET | gateway token | Returns `{version, transcriptionModel, authAvailable}` |
| `/start-listening` | POST | gateway token | **Deprecated (410)** — use `/transcribe-and-reply` with `wav_path` |

### Trigger a transcription manually

```bash
curl -X POST http://localhost:18789/transcribe-and-reply \
  -H "Authorization: Bearer <gateway-token>" \
  -H "Content-Type: application/json" \
  -d '{"wav_path": "/tmp/recording.wav"}'
```

## Snarling Button Mapping

| Button | Normal State | Approval State | Notification State |
|--------|-------------|----------------|-------------------|
| **X** | Voice input | — | — |
| **Y** | Sleep mode | — | — |
| **B** | No-op | Reject | Dismiss |
| **A** | — | Approve | Reveal |

The X button only triggers voice input when no approval or notification is active.

## Recording Pipeline (v5)

The v5 pipeline uses `subagent.run()` to create an isolated agent turn, which then uses `send_notification` to deliver the answer to the Snarling display:

1. **X press** → Snarling starts `arecord` immediately in a background thread (~82ms latency)
2. **Recording** → Snarling records 20s of audio to a WAV file
3. **POST wav_path** → Snarling POSTs the file path to `/transcribe-and-reply`
4. **Transcription** → Plugin transcribes via `gpt-4o-mini-transcribe` (~2s)
5. **subagent.run()** → Plugin calls `api.runtime.subagent.run()` with the transcript
6. **send_notification** → The subagent answers the question and calls `send_notification` to display the result on Snarling
7. **Sleep** → Snarling state set back to sleeping

### Why subagent.run?

Previous approaches using `enqueueSystemEvent` + heartbeat wake were unreliable. The system event would enqueue and the heartbeat would report `status=ran`, but the event text never surfaced in the agent's context during the heartbeat turn (phantom heartbeat bug #86090). The subagent approach creates a real agent turn that can execute tools — specifically `send_notification` — to deliver answers directly to the display.

## Privacy

⚠️ **Audio is sent to OpenAI for transcription.** When you press X, the recorded audio (WAV file) is transmitted to OpenAI's Whisper API (`api.openai.com/v1/audio/transcriptions`) for speech-to-text conversion. OpenAI may retain transcribed text per their API data retention policy.

- **What's sent:** The raw WAV audio recording (~20 seconds)
- **Where it goes:** OpenAI's servers (US-based)
- **What's retained:** Check [OpenAI's API data usage policy](https://openai.com/policies/api-data-usage/)
- **Local data:** The WAV file is deleted after transcription. Debug logs (if enabled) do not contain audio or full API keys.

To avoid sending audio to OpenAI, you can use a local transcription model by changing the `transcriptionModel` config — but this requires a self-hosted Whisper endpoint.

## Known Limitations

- USB mic picks up audio within ~1-2 feet
- Empty transcripts are silently skipped (not enqueued)
- Whisper may truncate trailing words with "..."
- Background noise can cause false activations
- OpenAI API key is cached after first resolution; first call after restart takes ~5-6s (mitigated by v4 parallel start)

## Plugin Location

- Source: `~/.openclaw/extensions/openclaw-voice-bridge/index.mjs` (hand-curated, NOT esbuild output)
- Config: `openclaw.plugin.json` with `micDevice`, `recordingDurationSec` (default: 20), `transcriptionModel`
- GitHub: https://github.com/snarflakes/OpenClaw-Voice-Bridge (development branch)

## Debugging

Debug logging is **opt-in** and disabled by default. To enable:

```bash
export VOICE_BRIDGE_DEBUG=1
# Optional: override the log file path
export VOICE_BRIDGE_DEBUG_LOG=/tmp/voice-bridge-debug.log
```

When enabled, debug logs are written to `VOICE_BRIDGE_DEBUG_LOG` (default: `/tmp/voice-bridge-debug.log`). All potentially sensitive values (API keys, tokens, bearer strings) are automatically redacted.

WAV files are created at `/tmp/voice_recording.wav.<timestamp>.wav` during recording and deleted after transcription.

After code changes to the plugin, a **full process restart** is required (`systemctl --user restart openclaw-gateway`). SIGUSR1 hot-reload only reloads config, not plugin code.

⚠️ **Do NOT esbuild rebuild `index.mjs` from `index.ts`** — the esbuild output differs subtly from the hand-curated git version and breaks transcription. Apply patches surgically to `index.mjs` directly.