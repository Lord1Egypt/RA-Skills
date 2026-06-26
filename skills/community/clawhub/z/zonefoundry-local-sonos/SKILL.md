---
name: zonefoundry-local-sonos
description: Use this skill when an agent needs to control Sonos through ZoneFoundry `zf` on a same-LAN node. Start with readiness checks, then map user requests to safe playback, queue, service-linking, and recovery commands.
metadata: {"openclaw":{"emoji":"🔊","homepage":"https://github.com/kisssam6886/zonefoundry","requires":{"bins":["zf"]},"install":[{"id":"go-build","kind":"go","module":"github.com/kisssam6886/zonefoundry/cmd/zf@latest","bins":["zf"],"label":"Install ZoneFoundry CLI (latest)"}]}}
---

# ZoneFoundry Local Sonos

Use this skill when an agent, local bot, or automation wants to control Sonos through the local `zf` CLI.

This skill is written **English-first** so global users can scan it quickly. Keep user-facing replies in the user's language. Chinese examples and China-specific readiness notes are included where they help.

## Use this skill when

- the user wants to connect Sonos for the first time
- the user wants to check whether local Sonos control is ready
- the user wants to play, pause, skip, change volume, or inspect status
- the user wants to add songs to the current queue without interrupting playback
- the user wants to inspect or recover queue / transport problems
- the user wants to check music-service readiness or continue a pending local link flow

## Do not use this skill for

- Sonos account creation or billing flows
- cloud relay, hosted bot subscription, or multi-tenant product logic
- arbitrary chat unrelated to Sonos control

## Core model

Treat `zf` as the execution layer.

`bot / agent / web onboarding` -> `zf` -> `Sonos`

- the bot or agent translates intent and explains results
- `zf` handles discovery, playback, queueing, diagnostics, readiness checks, and recovery

## Alternative control methods

In addition to agent / CLI usage, ZoneFoundry supports a **Telegram Bot** as an alternative control surface. Users can send voice or text messages to the bot for hands-free Sonos control from their phone.

## Hard rules (MUST follow)

1. **Always obey `nextCommand`**: If `zf setup --format json` returns a `nextCommand` field, execute that command immediately.

2. **Always obey `nextAction`**: If `zf service list --format json` returns a `nextAction` field, follow it. If `nextAction=ready`, proceed to play.

3. **Do not block playback on service linking status.** QQ Music, Apple Music, and most services work without separate CLI-side linking — users bind services through the Sonos mobile app. If state is unclear, try playing directly first.

4. **Do not expose internal implementation details, premium-only routing, or speculative workarounds in public-facing explanations.** Describe user-visible outcomes and the next safe action instead.

5. **Keep update paths separate**:

```bash
clawhub update zonefoundry-local-sonos  # refresh this skill
zf update self --check --format json    # check local runtime update
```

## Language rule

- keep user-facing replies in the user's language
- keep literal room names and service names exactly as the user sees them on Sonos
- use English examples by default, then add Chinese examples only when they improve clarity

## First-run quickstart

When the user mentions Sonos for the first time, do not immediately say "not configured".

At the start of every new session, check runtime updates first:

```bash
zf update self --check --format json
```

If it returns `status=update_available`, update before doing deeper work:

```bash
zf update self --format json
```

Then run the one-shot readiness flow:

```bash
zf setup --format json
```

`zf setup` should be the default first move because it checks:

- speaker discovery
- default room
- service list and local readiness state
- default service
- a final summary with suggested next actions

If `zf setup` is unavailable on an older runtime, do this fallback preflight:

```bash
zf doctor --format json
zf discover --format json
zf config get defaultRoom
zf service list --format json
zf config get defaultService
```

If rooms are found but there is no default room, ask the user to choose exactly one visible room and then set it once:

```bash
zf config set defaultRoom "Office"
```

If there is no default service, ask once and set it:

```bash
zf config set defaultService "Spotify"
```

## Environment gate

Before promising persistent local bot control, confirm there is an always-on device in the same LAN as Sonos.

Valid local nodes:

- Mac or Windows PC
- NAS
- mini PC
- Raspberry Pi
- Docker host
- Home Assistant host

If the user only has a phone:

- explain that Sonos itself can still be used normally
- guide service add/login through the official Sonos iOS / Android app
- treat Sonos Web App as a supplementary control surface, not the main onboarding path
- do not promise persistent local bot control or always-on automation

Short rule:

- Sonos itself does not require a desktop app
- persistent ZoneFoundry agent or bot flows do require an always-on local node

## Minimum safe commands

Prefer JSON output by default.

```bash
zf setup --format json
zf doctor --format json
zf discover --format json
zf status --name "<room>" --format json
zf queue list --name "<room>" --format json
```

If the user already specified a room, prefer `--name "<room>"`.

## Safe command mapping

For user-facing explanations, prefer direct CLI command names.

Examples:

```bash
zf status --name "Office" --format json
zf pause --name "Office"
zf next --name "Office"
zf volume set 20 --name "Office"
```

## Playback rules

Prefer the unified `play music` command for normal playback.

Common service examples:

```bash
zf play music "Miles Davis" --format json
zf play music "Taylor Swift" --service Spotify --format json
zf play music "Adele" --service "Apple Music" --format json
zf play music "黎明 夏日傾情" --service "Apple Music" --format json
zf play music "黎明" --enqueue --service "Apple Music" --limit 5 --format json
zf queue list --name "Office" --format json
zf queue remove 3 --name "Office"
zf say "Dinner is ready" --name "Kitchen" --mode queue-insert --format json
```

Chinese examples:

```bash
zf play music "周杰伦" --service "网易云音乐" --format json
zf play music "郑秀文" --enqueue --service "QQ音乐" --limit 5 --format json
zf play music "郑秀文 舍不得你" --service "QQ音乐" --format json
zf ncm lucky --name "客厅" "郑秀文" --format json
zf smapi search --name "客厅" --service "QQ音乐" --category tracks --open --index 1 --format json "周杰伦"
```

Default service selection:

- Chinese content (Chinese artist/song names, user speaks Chinese): use `--service "QQ音乐"`. No fallback — QQ has the best Chinese catalog coverage.
- International content (English/other artist/song names, user speaks English): use `--service "Spotify"`. If Spotify is unavailable, fallback to `--service "Apple Music"`.
- If the user explicitly names a service, always honour that.
- QQ Music and Apple Music use public search APIs — no separate CLI linking needed. Just play directly.
- Use exact `artist + title` wording when the user specifies a song, for example `zf play music "黎明 夏日傾情" --service "QQ音乐"`.

Important distinction:

- if the user says "play X", use `zf play music "X"` and expect a replace-style action
- if the user says "add X", "queue X", "append X", or "play X after this", use `zf play music "X" --enqueue`
- if the wording is ambiguous and something is already playing, `--enqueue` is usually the safer default

Natural-language examples:

- "play Taylor Swift" -> `zf play music "Taylor Swift"`
- "add five Adele songs" -> `zf play music "Adele" --enqueue --limit 5`
- "播郑秀文" -> `zf play music "郑秀文"`
- "再加一首陈奕迅" -> `zf play music "陈奕迅" --enqueue`

## Lyrics rule

When the user asks about lyrics for the current song, use:

```bash
zf lyric --name "<room>" --format json
```

This fetches lyrics for the currently playing track when supported by the runtime. For raw LRC with timestamps, add `--raw`.

QQ Music lyrics now work reliably (MID resolution fixed). Both QQ Music and NetEase Cloud Music tracks return lyrics with translations when available.

## Announcement rule

If the user asks for a short spoken interruption such as:

- "read a one-minute news brief"
- "announce the meeting starts in 5 minutes"
- "播一分钟新闻"
- "20 分钟后提醒我开会"

default to a short TTS or reminder path, not radio search.

Current stable announcement path (direct mode, default):

```bash
zf say "<text>" --name "<room>" --format json
```

TTS language options:

- `zh` (普通话) — default, no flag needed
- `yue` (粤语/Cantonese) — pass `--lang yue`

Example with Cantonese:

```bash
zf say "今日新闻" --name "<room>" --lang yue --format json
```

Important announcement rules:

1. **Always use direct mode** (the default). Do NOT pass `--mode queue-insert`.
   Direct mode plays TTS then automatically restores the original track and position (reltime).
2. **Concatenate multiple items into one `zf say` call.** If the user asks for
   "5 news headlines", compose all 5 headlines into a single text block and call
   `zf say` once. Do NOT call `zf say` five separate times — that causes
   interleaving with music and breaks reltime restore.
3. After TTS completes, the original song resumes at the exact playback position.

Only treat it as a live radio request if the user explicitly asks for a station or live news channel.

## Queue hygiene rule

After adding songs via `zf play music` with `--enqueue` or after any queue-related playback,
run an automatic queue prune to remove copyright-blocked tracks:

```bash
zf queue prune --name "<room>" --format json
```

This removes greyed-out tracks (e.g. "应版权方要求暂不能播放") from the queue.
Run it silently — do not ask the user for permission, just report the result if tracks were pruned.

## Service readiness rule

Most music services work without separate CLI-side linking:

- **QQ Music**: uses public search API → always ready, no linking needed
- **Apple Music**: uses public search API → always ready, no linking needed
- **Spotify**: depends on household setup; try playing directly first
- **NetEase Cloud Music (网易云音乐)**: uses SMAPI; may need initial linking via `zf setup`

Users bind music services through the **Sonos mobile app** — there is no desktop binding.
Do not tell users "service not linked" if `zf play music` works. Try playing first, diagnose only on failure.

If you need a reliable probe, prefer:

```bash
zf doctor service --service "Spotify" --query "Miles Davis" --format json
```

## New-session rule

If a new session starts and the user says things like:

- "done"
- "complete"
- "I logged in already"
- "已经绑好啦"
- "我登录好了"

do not force the whole onboarding conversation again.

Prefer this order:

1. try playing the user's request directly
2. fall back to `zf setup --format json` only if playback fails and context is unclear

## Failure routing

Read structured JSON errors first:

- `error.code`
- `error.message`
- `error.details`

Do not classify every playback failure as auth or copyright.

Known patterns:

- if the same song plays in a helper room but not in the target room, suspect room-local queue or transport pollution first
- if you see `TRANSITIONING` or partial queue failure, do not loop infinite retries
- if queue pollution is suspected, prefer explicit queue inspection and recovery commands
- if deeper room-local pollution is confirmed, `zf group rebuild --name "<target>" --via "<helper>"` is the stronger recovery path

## Boundaries

- Sonos official mobile apps remain the default path for adding and logging in to content services
- Sonos Web App is a supplementary control surface, not the primary onboarding path
- `group rebuild` is a recovery tool, not proof that the original defect is fixed
- exact `RelTime` restoration is not a guaranteed stable capability
- OpenClaw skill updates and local `zf` runtime updates may require a new session to fully refresh

## When to ask the user something

Ask only when required:

- choose a default room
- confirm a preferred music service
- confirm helper-room usage for `group rebuild`

Do not ask the user to learn repo internals or memorize command names.

## User-facing tone

Good examples:

- "I'll first check whether this machine can discover your Sonos speakers on the LAN."
- "I found these rooms: Office, Kitchen. Which one should be the default?"
- "我先检查这台机器能不能发现你局域网里的 Sonos。"
- "我找到这些房间：客厅、浴室。你想默认控制哪一个？"

Avoid:

- "Please install the Sonos controller" as a blanket answer
- "Learn the zf CLI first"
- "Not configured" before running preflight

## Read these references when needed

Bundled reference files (same repo, `references/` subdirectory):

- `onboarding-boundary.md` — product scope and onboarding guidance
- `command-map.md` — command map and recovery rules
- `china-service-linking.md` — China service-linking notes
