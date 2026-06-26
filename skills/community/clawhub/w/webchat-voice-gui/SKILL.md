---
name: webchat-voice-gui
description: >
  Voice input and microphone button for OpenClaw WebChat Control UI. Adds a mic
  button to chat, records audio via browser MediaRecorder, transcribes locally
  via faster-whisper, and injects text into the conversation. Includes gateway
  hook for update safety. Real-time VU meter shows voice activity.
  Push-to-Talk (hold to speak) and Toggle mode (click start/stop), switchable
  via double-click. Keyboard shortcuts: Ctrl+Space PTT, Ctrl+Shift+M continuous
  recording, Ctrl+Shift+B live transcription [beta]. Localized UI (English,
  German, Chinese built-in, extensible). Fully local speech-to-text, no API costs.
  Keywords: voice input, microphone, WebChat, Control UI, speech to text, STT,
  local transcription, MediaRecorder, voice button, mic button, push-to-talk,
  PTT, keyboard shortcut, i18n, localization.
requires:
  skills:
    - webchat-https-proxy (HTTPS/WSS reverse proxy — must be deployed first)
    - faster-whisper-local-service (local STT backend on port 18790)
  modified_paths:
    - <npm-global>/openclaw/dist/control-ui/index.html (injects script tag)
    - <npm-global>/openclaw/dist/control-ui/assets/voice-input.js (copies asset)
    - ~/.openclaw/hooks/voice-input-inject/ (creates startup hook)
    - ~/.openclaw/workspace/voice-input/voice-input.js (copies runtime file)
    - ~/.openclaw/workspace/voice-input/i18n.json (copies runtime file)
  env:
    - VOICE_LANG (optional, default: auto — prompts interactively if not set)
  persistence:
    - "Gateway startup hook: voice-input-inject (re-injects JS after updates)"
  privileges: user-level only, no root/sudo required
  dependencies:
    - faster-whisper transcription service on port 18790
---

# WebChat Voice GUI

Voice input GUI for OpenClaw WebChat Control UI:
- Mic button with idle/recording/processing states
- Real-time VU meter: button shadow/scale reacts to voice level
- **Push-to-Talk**: hold mic button to record, release to send (default mode)
- **Toggle mode**: click to start, click to stop (switch via double-click on mic button)
- **Keyboard shortcuts**: `Ctrl+Space` Push-to-Talk, `Ctrl+Shift+M` start/stop continuous recording, `Ctrl+Shift+B` live transcription [beta]
- **Localized UI**: auto-detects browser language (English, German, Chinese built-in), customizable
- Gateway startup hook re-injects script after `openclaw update`

## Prerequisites

1. **`webchat-https-proxy`** — HTTPS/WSS reverse proxy must be deployed and running.
2. **`faster-whisper-local-service`** — Local STT backend on port 18790.

Verify:
```bash
systemctl --user is-active openclaw-voice-https.service
systemctl --user is-active openclaw-transcribe.service
```

## Deploy

```bash
bash scripts/deploy.sh
```

With language override:
```bash
VOICE_LANG=de bash scripts/deploy.sh
```

When run interactively without `VOICE_LANG`, the script will ask you to choose a UI language.

This script is idempotent.

## Quick verify

```bash
bash scripts/status.sh
```

## Security Notes

### Client-side JS (`voice-input.js`)
- **No dynamic code execution**: No `eval()`, `new Function()`, or `innerHTML` with user data.
- **HTTPS-first**: Transcription requests use same-origin `/transcribe` when served over HTTPS. Only falls back to `http://127.0.0.1:18790` in local dev.
- **No external servers**: Audio is never sent outside the local machine.
- **No token scraping**: Client JS does not read gateway auth from browser storage. `/transcribe` is accepted via same-origin browser requests; Bearer auth remains optional fallback at the proxy.
- Uses `textContent` for all toast messages (no XSS vector).
- **Bounded memory**: Continuous recording mode enforces a 120-chunk limit (~2 minutes), preventing unbounded memory growth.

### Deployment scripts
- **Language input validated**: `VOICE_LANG` must match `^([a-zA-Z]{2,5}(-[a-zA-Z]{2,5})?|auto)$` — prevents injection via sed.
- **Robust path detection**: All scripts validate Control UI directory exists before modifying files.
- **Gateway hook**: Uses `execFileSync` with array args — no shell interpolation. Script path derived from `__dirname`, not user input.
- **Idempotent**: All scripts safe to run repeatedly.

### No data exfiltration
- No outbound network calls from JS or scripts.
- No telemetry, analytics, or tracking.

## What this skill modifies

| What | Path | Action |
|---|---|---|
| Control UI HTML | `<npm-global>/openclaw/dist/control-ui/index.html` | Adds `<script>` tag for voice-input.js |
| Control UI asset | `<npm-global>/openclaw/dist/control-ui/assets/voice-input.js` | Copies mic button JS |
| Gateway hook | `~/.openclaw/hooks/voice-input-inject/` | Installs startup hook that re-injects JS after updates |
| Workspace files | `~/.openclaw/workspace/voice-input/` | Copies voice-input.js, i18n.json |

## Mic Button Controls

| Action | Effect |
|---|---|
| **Hold** (PTT mode) | Record while held, transcribe on release |
| **Click** (Toggle mode) | Start recording / stop and transcribe |
| **Double-click** | Switch between PTT and Toggle mode |
| **Right-click** | Toggle beep sound on/off |
| **Ctrl+Space** (hold) | Push-to-Talk via keyboard |
| **Ctrl+Shift+M** | Start/stop recording |
| **Ctrl+Shift+B** | Start/stop live transcription [beta] |

## Language / i18n

Auto-detects browser language. Built-in: English (`en`), German (`de`), Chinese (`zh`).

Override in browser console:
```js
localStorage.setItem('oc-voice-lang', 'de');  // force German
localStorage.removeItem('oc-voice-lang');      // back to auto-detect
```

See `assets/i18n.json` for all translation keys.

## Uninstall

```bash
bash scripts/uninstall.sh
```

This removes the UI injection, hook, and workspace files. Does **not** touch the HTTPS proxy or faster-whisper backend — uninstall those separately.
