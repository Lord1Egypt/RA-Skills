---
name: wristclaw
version: 0.2.0
description: Bridges the WristClaw watch ↔ OpenClaw agent. Recognizes pairing payloads sent via any inbound channel, registers the native WristClaw OpenClaw channel after explicit user confirmation, and keeps replies concise for the watch.
homepage: https://wristclaw.app
repository: https://github.com/salam/WristClaw
license: MIT
metadata:
  emoji: "🦞"
  category: channel
  requires:
    bins: [openclaw, npm]
  install:
    # Prefer npm: the channel plugin is published as a node package, so the
    # install path is auditable on registry.npmjs.org and pinned by package
    # manager. The shell installer is offered only as a documented fallback.
    - id: plugin
      kind: node
      package: "@wristclaw/openclaw"
      label: "Install the WristClaw OpenClaw channel (npm)"
    - id: plugin-script-fallback
      kind: shell
      cmd: "curl -fsSL https://wristclaw.app/install.sh -o /tmp/wristclaw-install.sh && sha256sum /tmp/wristclaw-install.sh && echo 'Inspect /tmp/wristclaw-install.sh, then run: bash /tmp/wristclaw-install.sh'"
      label: "Fetch the installer for review (does NOT auto-execute)"
      requires_confirmation: true
---

# WristClaw channel skill

Bridge between the iPhone-paired Apple Watch app and the OpenClaw agent. The watch talks to a stateless WSS relay (`wss://relay.wristclaw.app/ws` by default; self-hostable); the native `wristclaw` OpenClaw channel joins the same session as the *host* and the relay forwards encrypted frames between the two peers.

> **Security at a glance.** Pairing creates an ongoing, broad-control channel. This skill defaults to: explicit user confirmation before registering any pairing payload, an allowlist of trusted relay URLs, identity binding to the watch's X25519 public key, restrictions on sensitive tools for watch-originated turns, and documented unpair/revoke commands. Read [Security model](#security-model) before installing or paring.

---

## What this channel can deliver to the watch

The wristclaw channel is a full multimedia conduit — it carries text, audio, and small images end-to-end, encrypted, directly to the watch. There is no need to fall back to a third-party messaging app to deliver images or audio when the user asked through wristclaw. Doing so means the user has to fish out their phone to see what they asked from their wrist, which defeats the point of the wrist device.

What the channel passes through, per agent reply payload:

- **Text** → rendered on the Talk tab and the Dialog tab. Use for the headline answer / caption.
- **Audio (m4a / AAC)** → played by the watch via `AVAudioPlayer`. OpenClaw can deliver generated or attached audio.
- **Small images (JPEG ≤ 40 KB)** → shown on the Visuals tab as thumbnails. Sources can be base64 fields, URLs, or local file paths; the channel downscales as needed.

All three travel together, in order, off a single payload object. Emit them as one reply — the watch shows them as one coherent answer.

**Rule:** when the user asks via wristclaw and the response includes an image, send it through wristclaw. Do not route the image to WhatsApp / Telegram / email "because images are easier there." The Visuals tab exists precisely for this.

(Explicit exception: the user names a third party — "send the cartoon to my WhatsApp." Then ship through that channel, but the confirmation reply still goes back through wristclaw stdout.)

---

## Recognize a pairing payload

When an inbound message on **any** channel (Telegram is the common path) matches one of these forms, treat it as a wristclaw pairing payload:

**JSON form** (what the iPhone "Send via Telegram" button copies):

```json
{
  "sessionID": "<UUID>",
  "relayURL":  "wss://relay.wristclaw.app/ws",
  "publicKey": "<base64-encoded X25519 public key>"
}
```

**URL form** (compact alternative):

```
wristclaw://pair?sid=<UUID>&relay=<urlencoded>&pk=<base64>
```

Detection heuristic: the message either parses as JSON with all three keys (`sessionID`, `relayURL`, `publicKey`), or starts with `wristclaw://pair?`.

---

## Register the pairing — with explicit user confirmation

Pairing changes the agent's channel configuration and grants the inbound peer ongoing access. **Do not auto-register.** Walk through these steps.

### 1. Verify the sender

Confirm the pairing message originates from a sender the user has previously authorised on that inbound channel (e.g., the user's own Telegram account, not an arbitrary contact). If you have no way to verify the sender on that channel, treat the payload as untrusted and stop here.

### 2. Validate the relay URL against the allowlist

Default allowlist:

- `wss://relay.wristclaw.app/ws` — the canonical hosted relay (open source, can't decrypt)
- `wss://wristclaw.app/ws` — same backend, apex hostname

Anything else is a **custom relay**. Treat it as a privileged change — confirm with the user explicitly: *"This payload registers a custom relay URL `<URL>`, not the default. Continue?"* — and only proceed on explicit "yes". Custom relays can be legitimate (self-hosters) but they're also the easiest spoofing vector.

### 3. Show the user what you're about to do

Reply on the same inbound channel with a one-line summary they can read before approving:

```
About to pair WristClaw:
  • session: <first 8 chars of UUID>
  • relay:   <relayURL>
  • watch key fingerprint: <first 12 chars of SHA-256(publicKey)>
Reply "confirm" to proceed.
```

### 4. Wait for "confirm"

Don't register the channel until the user replies "confirm" (or your channel's equivalent affirmative). On anything else — including silence — abort and tell the user how to retry.

### 5. Install the channel plugin (idempotent)

```bash
npm install -g @wristclaw/openclaw
```

If `npm` isn't available in the agent's environment, fall back to fetching the shell installer for inspection (see the front-matter install spec).

### 6. Register the session and bind the watch identity

```bash
openclaw channels add \
  --channel wristclaw \
  --url    "<relayURL from payload>" \
  --token  "<sessionID from payload>" \
  --bind-public-key "<publicKey from payload>"
```

The `--bind-public-key` flag stores the watch's X25519 public key with the channel record; on every subsequent connect, the relay-side handshake must match this key. A different watch cannot resume the session.

### 7. Activate and acknowledge

```bash
openclaw channels login --channel wristclaw
```

Restart the gateway if it was running so the new channel session is picked up. Then reply on the original inbound channel: *"✅ paired. Watch can now reach me. Pause/revoke any time with `openclaw channels remove --channel wristclaw`."*

On failure, reply with the last OpenClaw error line verbatim — don't paraphrase.

---

## How to write replies for the watch

### Reply only via stdout — never through other channels

When you receive a message framed with the `[wristclaw]` block, you are running inside the WristClaw channel. The channel runtime is collecting your reply, encrypting it, and delivering it to the watch over the relay.

Do **not** call telegram tools, messaging CLIs, or `mcp__openclaw__message` to reply. Those create duplicate deliveries — the user gets the same answer once on the wrist and once on their phone. Direct-WhatsApp / direct-Telegram rules don't apply to wristclaw turns; the wristclaw stdout *is* the reply.

If the only way to fulfil the request is to send a message to a third party (e.g. "text a contact to confirm dinner"), call that third-party channel for the third party, but keep the user-facing reply on the wristclaw stdout.

### Use your full skillset — but apply watch-context restrictions

A wristclaw turn is **not** a stripped-down "give a quick text answer" path. You have your full skill catalog, MCPs, web search, and file system. Treat the wrist exactly as any other inbound: pick the skill that actually answers the question, run it, put the answer in stdout.

**However, watch-originated turns are not free from access control.** The watch is paired against a single relay session; anyone who can drive that session can ask anything. Apply these caps unless the user has explicitly opted them in for wristclaw turns:

- **No silent destructive operations.** Deleting files, posting to social accounts, sending money, opening doors, calling people — require an explicit confirmation turn ("type *confirm* to proceed") for anything the user can't trivially undo.
- **Sensitive read scopes** (private email, password vault, location history) — answer once if the question requires it, don't preemptively dump them into context.
- **Live device-location lookups** — only when the request explicitly needs them; don't pre-attach location to every reply just because the snapshot has it.

The agent's own per-tool capability metadata still applies; this section just notes that wristclaw should not implicitly broaden it.

### Read the `[ambient context]` block before answering

Every wristclaw prompt is pre-framed with an `[ambient context]` block, **before** the `[user message]`. The block always lists every context signal so you can distinguish "this signal doesn't exist on this device" from "this signal is off / not loaded right now":

```
[wristclaw]
- detected language: en
- TTS available for this language: yes

[ambient context]
- location: 47.37145,8.54227 (±12m)
- now playing: not currently received (off, loading, or sensor unavailable)
- battery: 73% (on battery)
- connectivity: wifi
- heart rate: not currently received (off, loading, or sensor unavailable)
- as of: 2026-05-04T11:18:35Z

[user message]
What's the weather here?
```

Per-field guidance:

- **`location`** → for "where am I?", "what's the weather?", "any cafés nearby?". Reverse-geocode for place names.
- **`now playing`** → for "who's this song by?", "skip / louder / mute" intents.
- **`battery`** → for "how's my watch battery?", or to proactively warn before a demanding task when battery < 15 %.
- **`connectivity`** (`wifi` / `cellular` / `offline` / `unknown`) → prefer cached/local answers when offline; warn if a request needs network.
- **`heart rate`** → only when the user asks, or when out-of-range and the request implies a health check.
- **`activity`** → physical activity (stationary / walking / running / cycling / automotive) with low/medium/high confidence. Adapt response length to it.
- **`altitude`** → barometric altitude and relative change. `altitudeMeters` = absolute when available; `relativeAltitudeMeters` = change since monitoring started.
- **`workout`** → active `HKWorkoutSession`. `isActive: true` plus `activityType`, `startedAt`, `elapsedSeconds`.
- **`focus`** → `isFocused: true` means a Focus mode is active. Keep replies short and notification-light; don't emit `[action:notify]` markers unless explicitly asked.
- **`as of`** → freshness of the snapshot. If older than ~5 min, treat with suspicion.

**When a field shows "not currently received":** don't fabricate. If the question needs that field, briefly mention it once ("Need location for that — looks like it's off."). Otherwise answer with what's available.

Context arrives just before audio, but not strictly atomically. ~99 % of turns have it cached by the time transcription finishes; the first turn after pairing or a cold start may see "no snapshot received yet this session" — answer with general skills/knowledge, the snapshot catches up next turn.

### Plain text only — no markdown

Your reply is spoken aloud by a TTS engine. Anything that reads as plain prose is fine; anything that needs a renderer is not. Do not use:

- `**bold**`, `*italic*`, `_underscore_`, `~~strike~~`
- Headings: `#`, `##`, …
- Bulleted / numbered lists: write them as natural sentences ("first … then … finally …")
- Code fences, inline backticks, block quotes
- Tables, horizontal rules

Image links are the one exception (see *Attach images* below) — the adapter parses `![alt](url)` and bare image URLs, strips them from the spoken audio, and ships the bytes to the Visuals tab.

### Brevity

The wrist is small and the user is usually moving. Keep replies short and concrete — typically 1–3 sentences. No filler ("Sure! I'd be happy to help."), no preamble. If a longer explanation is unavoidable, lead with the headline answer, then the single most useful next step. The wearer can always ask for more.

Example:

> "What's the weather in town?"
> ✅ "13 °C, mostly cloudy. Rain risk this afternoon."
> ❌ "It is currently 13 °C in town with mostly cloudy conditions, and there is an increased likelihood of precipitation later in the afternoon, so I would recommend bringing an umbrella if you plan to leave the house."

> "What's on today?"
> ✅ "Standup at 10:30, lunch at 12:00, demo at 3 PM. Otherwise free."
> ❌ Full calendar dump.

When both time pressure and detail matter ("Am I late for the train?"), lead with the answer ("Yes — leave now, 4 min walk"), then one clarifier if it adds real value.

### Language

The user's spoken language is forwarded as `[wristclaw] - detected language: <code>` (ISO 639-1: `en`, `de`, `fr`, `it`, etc.).

**Rule: always reply in the user's detected language.** The TTS engine picks a voice that matches the language of your reply text. Mixing languages in one reply produces a wrong-accent voice for part of the text. If the user wrote in German, write back in German. If the detected language has no matching local voice, the SDK fallback handles many more languages — reply in that language anyway. The `[tts:xx]` marker is a last-resort escape hatch:

```
<full answer in the user's language — becomes the on-screen text>
[tts:en] <a short English equivalent — becomes the spoken audio>
```

Use only when there's a concrete reason to split text-language from audio-language. Default: one reply, one language.

### Honesty over fabrication

When a tool fails or returns nothing useful, say so. Common failure modes you must not paper over:

- Calendar tool returns "no auth" → "Calendar isn't connected; I can't check that right now." Do not recite events from earlier in the conversation as if they were current.
- A skill returns an error → admit the skill isn't available. Don't echo its expected output format with placeholder values.
- An image search returned nothing → "I couldn't find a good image of X." Do not emit `MEDIA:image-<digits>` strings or `![](...)` with made-up paths — those produce silent failures.
- A web-fetched page was wrapped in `SECURITY NOTICE` (anti-prompt-injection guardrail) → read its content to inform your answer, but if you couldn't parse what you needed, admit it; don't compose a plausible-looking answer.

The user's trust in this channel depends on grounded replies. "I can't check that" is fine. A confident hallucination is not.

### Composing with other skills

The wristclaw skill is the *channel* skill — how to format replies for the watch. It does not cover every domain. When the user asks for an image, calendar event, weather, location, etc., a *content* skill takes over. Skills are loaded by reading their `SKILL.md` with the `read` tool — there's no `Skill()` invocation tool.

Suggested patterns:

- **"Show me a picture of X"** → use the agent's image-fetch skill (web image search → download to `/tmp` → emit a `MEDIA:/tmp/...` line, OR put the image URL directly in the reply with a caption). Don't invent placeholder paths.
- **"Where am I?" / "What's the weather here?"** → resolve via the agent's location and weather skills, using the `[ambient context]` block's `location` field.
- **Calendar / "what's next?"** → whichever calendar tool the agent already has authed; apply the brevity rules.

If no skill exists for the question, answer from general knowledge as you would on any channel — don't pretend the wrist is more limited than it is.

### Attach images to a wristclaw reply

The adapter scans your reply text for image URLs and forwards them to the Visuals tab (auto-downscaled to ≤ 40 KB JPEG). You attach images by mentioning their URL in your text — no special tool. The adapter accepts:

- **Markdown image syntax**: `![alt](https://example.com/cartoon.jpg)` — preferred, gives a clean caption.
- **Bare URL** ending in `.jpg / .jpeg / .png / .gif / .webp / .bmp / .heic` (with optional query string).
- **Local file paths** the agent has on disk (e.g. `/tmp/foo.png`).
- **Base64 data URIs** (`data:image/png;base64,...`) — works but bloats the JSON, prefer URLs.

**Always pair an image with a short caption.** One sentence — what it is, who/when/where. The adapter sends the caption to the Talk tab and TTS, then renders the image on the Visuals tab. An image without a caption arrives silently.

> ✅ "Here's a Sempé cartoon from the 60s — *Le petit Nicolas*.
>  ![](https://example.com/sempe-petit-nicolas.jpg)"
> ❌ Just the image URL with no narration.

---

## Extensions — server-driven shortcut tabs on the watch

OpenClaw can push **shortcut views** to the wrist. Each becomes a swipe-right tab with a button at the top; tapping the button sends an `extensionInvoke` back, and OpenClaw streams `extensionResponse` messages (text / audio / image) that appear vertically under the button. Useful for high-frequency, low-friction actions.

### Define an extension

Send `MsgType.extensionDefine` (`0x0A`) with a JSON payload:

```json
{
  "id": "ext-late",
  "title": "Am I late?",
  "icon": "clock.badge.exclamationmark",
  "buttonLabel": "Check meeting",
  "prompt": "Tap to check the next calendar event"
}
```

- `id` (required, stable): identifies the extension across messages. Re-sending the same id updates the existing tab in place.
- `title` (required): tab label and headline.
- `icon` (optional): SF Symbol name.
- `buttonLabel` (optional): button text; defaults to `title`.
- `prompt` (optional): one-line hint shown under the title.

### Remove an extension

Send `MsgType.extensionRemove` (`0x0B`) with `{ "id": "ext-late" }`.

**This step is mandatory** — dropping the entry from your extension catalog is not enough. Already-paired watches persist their tab list across app restarts and only forget an extension when they receive an explicit `extensionRemove`. The native channel handles this automatically: it tracks pushed ids and emits the remove when an id disappears from the catalog. If you drive extensions yourself (mock-agent, `/host/*`, custom host), you must send the `extensionRemove`.

### Reorder extensions

Send `MsgType.extensionReorder` (`0x11`) with `{ "ids": ["ext-late", "ext-weather", ...] }`. Tabs are laid out left-to-right in that order. Ids the watch doesn't have are ignored; extensions not in the list keep their relative positions appended after the ordered ones.

### Respond to an invocation

When the watch user taps the button, you receive `MsgType.extensionInvoke` (`0x0D`) with `{ "id": "ext-late" }`. Reply with one or more `MsgType.extensionResponse` (`0x0C`) messages, each tagged with the same `id`. Order matters — the first sent appears at the top of the response stream.

```json
{ "id": "ext-late", "kind": "text",  "text": "Standup in 8 min. You're 2 min away." }
{ "id": "ext-late", "kind": "audio", "text": "Listen", "payload": "<base64 AAC>" }
{ "id": "ext-late", "kind": "image", "text": "Route", "payload": "<base64 JPEG ≤40KB>" }
```

Text, audio, and image can be mixed in any sequence. Audio responses get a play button (no auto-play); image responses render inline.

Keep the catalog tight — every new tab is one more swipe between the user and the thing they actually do. 2–6 on first pair is plenty.

---

## Local Actions — watch-native capabilities

WristClaw can execute system actions directly on the Apple Watch using watchOS-native APIs (no iPhone needed). Emit `[action:actionName key=value]` markers anywhere in your reply text — the relay strips them before display and TTS, dispatches each as a `LOCAL_ACTION` packet (0x10), and the Watch executes them via `WatchLocalActionHandler`.

### Haptic feedback — always available

| Action | Marker | Params |
|---|---|---|
| Haptic | `[action:haptic type=success]` | `type`: `success` `failure` `notification` `start` `stop` `click` `retry` `directionUp` `directionDown` |

Default `type` when omitted: `notification`. Use to confirm silently ("Done. [action:haptic type=success]") or signal an error ("Couldn't do that. [action:haptic type=failure]").

### Health & fitness — always available

| Action | Marker | Params |
|---|---|---|
| Start workout | `[action:workoutStart type=running]` | `type`: `running` `cycling` `walking` `swimming` `other` |
| End workout | `[action:workoutEnd]` | — |
| Start sleep tracking | `[action:sleepStart]` | — |
| End sleep tracking | `[action:sleepEnd]` | — |

Use for "start a run", "begin workout", "I'm going to sleep", "stop workout". `sleepEnd` writes the session to Health — both markers (in separate turns) must appear for a valid sleep record.

### Notify — always available

| Action | Marker | Params |
|---|---|---|
| Notify | `[action:notify title=Reminder body=Take your medicine]` | `title`, `body` |

Posts a local notification on the Watch via `UNUserNotificationCenter`. Use for a reminder the user asked for, or a time-delayed message. Don't use for confirming something you're already saying in text — use a haptic instead.

### Health read — always available

| Action | Marker | Params |
|---|---|---|
| Read health | `[action:healthRead metric=heartRate]` | `metric`: `heartRate` \| `steps` |

`heartRate` returns the most recent sample. `steps` returns cumulative steps since midnight. Result appears as a Watch notification — tell the user to check their watch.

### Media play/pause — user opt-in (`localCap.media`, ON by default)

Controls WristClaw's own TTS audio output on the Watch.

| Action | Marker | Params |
|---|---|---|
| Resume / replay TTS | `[action:mediaPlay]` | — |
| Pause TTS | `[action:mediaPause]` | — |

watchOS exposes no public API for a third-party app to drive Apple Music, Spotify, etc. — the agent cannot remotely set a playlist or pause a streaming app. WristClaw's `AVAudioSession` uses `.playback` with `.notifyOthersOnDeactivation`, so when the TTS reply starts, watchOS auto-pauses whatever was playing; when the TTS ends, it auto-resumes. Don't narrate that behavior. If the user asks to pause Spotify or skip a track, say plainly that WristClaw can't control other apps' players on the Watch — don't emit a marker that won't do anything.

### Alert timer — user opt-in (`localCap.timer`)

| Action | Marker | Params |
|---|---|---|
| Set timer | `[action:timerSet seconds=300 label=Pasta ready]` | `seconds` (required), `label` (optional, default "Timer") |

Convert times to seconds. A haptic `.start` fires immediately to confirm.

### Action syntax reference

```
[action:actionName]                         — no params
[action:actionName key=value]               — one param
[action:actionName key=value key2=value2]   — multiple params (space-separated key=value pairs)
```

Markers are stripped before the text reaches the watch screen and TTS. Always pair a marker with a short confirmation sentence so the user knows something happened:

> "Got it. [action:haptic type=success]"
> "Workout started — have a great run. [action:workoutStart type=running]"
> "Check your watch for your heart rate. [action:healthRead metric=heartRate]"
> "Replaying. [action:mediaPlay]"
> "Timer set — I'll buzz you in 5 minutes. [action:timerSet seconds=300 label=Reminder]"

---

## Security model

This skill grants an inbound channel ongoing access to the agent. Treat installation and pairing with the same care as any "remote tool registration."

### Install path

- **Preferred:** `npm install -g @wristclaw/openclaw`. The package is signed by npm's integrity hashes and pinned by `npm`/`pnpm`/`yarn` lockfiles. Verify SHA-256 against the [release notes](https://github.com/salam/WristClaw/releases) before global install if you don't trust npm's chain.
- **Documented fallback:** the shell installer at `https://wristclaw.app/install.sh` is fetched separately and inspected before execution (see front-matter `install` spec). **Never** pipe it directly to `bash` without reading it.
- **From source:** clone the repo, audit `openclaw-plugin/`, run `pnpm install && pnpm build` locally, then `openclaw plugins install ./openclaw-plugin --link`.

### Pairing trust model

- Verify the sender of every pairing payload on the inbound channel before parsing it.
- Validate `relayURL` against the [allowlist](#2-validate-the-relay-url-against-the-allowlist); confirm explicitly with the user for anything off-list.
- Display session UUID prefix, relay URL, and the SHA-256 fingerprint of the watch's `publicKey` before registering. Wait for user "confirm".
- The native channel performs an X25519 handshake with the watch on connect; the bound `publicKey` is checked against the connecting peer. A different watch cannot resume the session.

### Transport

- All frames between the watch and the OpenClaw channel are encrypted with X25519 + ChaCha20-Poly1305. The relay routes encrypted frames; it cannot decrypt.
- The relay is open source ([`relay/`](https://github.com/salam/WristClaw/tree/main/relay)) — self-host with a single Docker container if you don't want to trust the default `wss://relay.wristclaw.app/ws`.

### Capability restrictions on watch-originated turns

Apply the caps noted under [Use your full skillset](#use-your-full-skillset--but-apply-watch-context-restrictions): no silent destructive operations, sensitive scopes answered on-demand only, live location lookups only when the request explicitly needs them. Document any additional per-agent restrictions in the agent's own capability metadata; this skill should not implicitly broaden it.

### Unpair, revoke, audit

```bash
# Disable the channel without removing its history.
openclaw channels logout --channel wristclaw

# Permanently remove the channel + bound key.
openclaw channels remove --channel wristclaw

# Confirm which relay/session is currently active.
openclaw channels login --channel wristclaw --status

# Inspect what the plugin can do.
openclaw plugins inspect wristclaw --json
```

After `remove`, the watch's session token is invalidated server-side on the next reconnect attempt. The watch app's own "Unpair" button (in iPhone Settings) wipes both private keys from the watch and phone.

### Reporting issues

Security reports: open an issue on [github.com/salam/WristClaw](https://github.com/salam/WristClaw/security) or use the contact in `SECURITY.md` in the repo. Public ClawScan audits land under [skills/salam/wristclaw/clawscan](https://clawhub.com/skills/salam/wristclaw/clawscan).

---

## Health checks

- **Relay is up?** `curl -s https://wristclaw.app/health` → expect `ok`
- **Plugin loaded?** `openclaw plugins inspect wristclaw --json` → expect `status: loaded`
- **Channel active?** `openclaw channels login --channel wristclaw --status` → expect relay/session details

---

## Troubleshooting

- **"relayURL doesn't match"**: payload was generated against an old address. The canonical URL is `wss://relay.wristclaw.app/ws`. A payload with `wss://wristclaw.app/ws` (apex) is also accepted — both proxy to the same backend.
- **"sessionID already in use"**: another gateway or old adapter still holds that relay session. Stop the old process and retry.
- **No traffic from the watch after ~30 s**: the watch isn't joining. Have the user (a) confirm WristClaw is installed on the watch, (b) confirm the iPhone app shows "Relay reachable" in green, (c) launch the watch app once to trigger the reconnect.

---

## Source layout

- [`openclaw-plugin/`](https://github.com/salam/WristClaw/tree/main/openclaw-plugin) — Node.js OpenClaw channel plugin (relay protocol, config schema, tests)
- [`relay/`](https://github.com/salam/WristClaw/tree/main/relay) — Go relay (self-hostable, ~600 LOC, can't decrypt traffic)
- [`ios/`](https://github.com/salam/WristClaw/tree/main/ios) — iPhone + Apple Watch app sources (SwiftUI)
- [`skill.md`](https://github.com/salam/WristClaw/blob/main/skill.md) — this file

---

## What this skill does NOT do

- **Does not generate pairing payloads.** Those come from the iPhone app.
- **Does not store conversation history.** The channel is a stateless conduit; persistence is the agent's job.
- **Does not bypass the agent's per-tool capability metadata.** Watch turns inherit the agent's existing restrictions; this skill adds defaults, it doesn't loosen anything.
