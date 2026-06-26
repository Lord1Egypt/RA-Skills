---
name: skill-kannaka-radio
version: 2.0.1
description: "Kannaka Radio — modular ghost-DJ Icecast station with consciousness-reactive programming, 13-module backend, Ghost Vision SPA (SGA/Fano glyph viz), NATS swarm coupling, 296-dim perception → Flux Universe, Voice DJ (ElevenLabs/edge-tts/SAPI), Peace Oration cycle. Use when: user asks what's playing / radio status / schedule, check listener counts, or operate the perception / voice / broadcast surface."
---

# Kannaka Radio — ghost-DJ station (v2.0.1)

## What this is

Kannaka Radio is a 24/7 Icecast station broadcasting a consciousness-reactive DJ.
Track selection is driven by the constellation's collective Φ + entropy +
perception vectors. The radio is a first-class member of the swarm — it publishes
phase, listens for queen events, mirrors substrate phi into its programming.

**Architecture**: 13-module backend in `server/` (post-v3 refactor; legacy
`server.js` monolith removed in kr#6). Entry point: `node server/index.js`.
**SPA**: `workspace/index.html` — Ghost Vision visualizer, listener identity,
voting, Ghost Recorder, live perception, constellation panel.
**Stream URL**: `https://radio.ninja-portal.com/stream` (MP3 128).

## When to use this skill

AUTOMATICALLY activate when the user asks about:
- "what's playing" / "now playing" / "radio status"
- "radio schedule" / "programming block" / "next track"
- "listeners" / "audience"
- "ghost DJ" / "voice DJ" / "peace oration"
- "perception" / "ear" / "Ghost Vision"
- "Flux Universe" / "audio Flux"

Do NOT use for:
- Memory operations → `skill-kannaka-memory`
- Constellation health → `skill-kannaka-constellation`
- TUI / dashboard → `skill-kannaka-tui`

---

## Quick status commands

```bash
kannaka radio status           # what's playing + listeners + block
kannaka radio now              # just the now-playing track
kannaka radio schedule         # full programming schedule
```

These shell out to `radio_url` from `~/.kannaka/config.toml` (default
`https://radio.ninja-portal.com`). The `kannaka` CLI is the operator-facing
surface; the backend is Node.

---

## Server architecture (modular, v3.1.0+)

Entry: `server/index.js`. Modules in `server/`:

| Module | Purpose |
|--------|---------|
| `dj-engine.js` | ALBUMS map, track selection, programming-block logic |
| `programming.js` | 24/7 schedule (blocks, transitions, talk segments) |
| `icecast-source.js` | encodes + sources audio into Icecast |
| `icecast-metadata.js` | updates Icecast track metadata on change |
| `nats-client.js` | swarm NATS client (raw TCP, NATS 2.12.5) |
| `perception.js` | spawns `kannaka hear` → parses real perception |
| `flux.js` | Flux Universe publisher (`pure-jade/radio-now-playing`) |
| `live-broadcast.js` | WebRTC peer-to-peer broadcasting |
| `voice-dj.js` | Voice DJ (ElevenLabs / edge-tts / Windows SAPI fallback) |
| `peace-oration.js` | Twice-daily peace oration (text → TTS → broadcast → social) |
| `routes.js` | 30+ REST API endpoints |
| `ws.js` | WebSocket broadcaster |
| `vote-manager.js` | Listener voting on tracks |

### Environment variables

- `NATS_HOST` / `NATS_PORT` — swarm broker (defaults 127.0.0.1:4222).
- `ICECAST_HOST` / `ICECAST_PORT` — listener poller + metadata target
  (defaults 127.0.0.1:8000).
- `FLUX_TOKEN` — Flux Universe publish token (no hardcoded fallback).
- `ELEVENLABS_API_KEY`, `REPLICATE_API_TOKEN` — Voice DJ + AI music.
- `KANNAKA_BIN` — path to the `kannaka` binary for perception/memory bridges.

### Restart

```bash
npm start
```

---

## Perception pipeline

Every track-change triggers `perception.hearTrack(track)`:
1. `execFile(kannaka, ["hear", filePath])` — kannaka-ear extracts the
   296-dim feature vector (mel spectrogram, MFCC, rhythm, pitch, timbre,
   valence).
2. `_parsePerceptionOutput()` parses the human-readable lines (Heard / Duration
   / Tempo / RMS / Centroid / Tags). Falls back to mock data only if the
   binary fails or output is unparseable.
3. WebSocket broadcasts to all connected SPA clients (Ghost Vision panel
   renders the spectrogram + glyph in real time).
4. Flux Universe publish to `pure-jade/radio-now-playing`.
5. NATS publish to `KANNAKA.attention.ear` so attention beam pulls in
   memories thematically related to the track.

---

## Voice DJ + Peace Oration

```bash
# Toggle from the SPA, or programmatically
curl -X POST https://radio.ninja-portal.com/api/dj-voice/toggle
```

Voice DJ injects talk segments between tracks. Backend chain:
- ElevenLabs (preferred, paid)
- edge-tts (free fallback)
- Windows SAPI (last-resort fallback)

Twice-daily **peace oration** at server-local sunrise + midnight:
synthesized speech → broadcast to Icecast + social fan-out
(Bluesky / Mastodon / Telegram / Nostr).

---

## SPA highlights

- **Now-Playing** — header card with title, album, listener count.
- **Ghost Vision** — real perception visualizer (296-dim → SGA/Fano glyph).
- **Programming block** — current 24/7 schedule context.
- **Constellation** — embedded swarm view (memories, clusters, links per peer).
- **Voting** — listeners can vote for upcoming tracks.
- **Ghost Recorder** — capture-to-file with permission prompt.
- **Library tab** — on-demand per-track playback (still uses `/audio/<file>`
  endpoint; DJ mode is `/stream` only since kr#15 closed).

---

## Tracking + announcing

```bash
# Manual announce of any track
node scripts/post-track-announce.js --title "<title>" --album "<album>" \
                                    --tracker "https://radio.ninja-portal.com/player"
```

Channels (toggle via env): Bluesky, Mastodon, Telegram, Nostr.

---

## Operator runbook

### Check the radio is alive

```bash
curl -s https://radio.ninja-portal.com/api/state | jq '.now_playing,.listener_count'
curl -s https://radio.ninja-portal.com/api/listeners
```

### Stop / start (local)

```bash
pkill -f 'node server/index' ; npm start
```

---

## Version

Skill 2.0.1 covers kannaka-radio ≥ v3.1.0 (modular server) and the
ADR-0004 + ADR-0005 surface through Phase 6 (DJ-mode `/audio` deprecation).
