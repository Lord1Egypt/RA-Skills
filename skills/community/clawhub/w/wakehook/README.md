<div align="center">

# ⏰ wakehook

**A webhook that fires when you wake up.**

Plug in your sleep data, get a clean `user.awake` event — then make your morning *do something*.

<img src="docs/architecture.svg" alt="wakehook — health APIs flow into wakehook, which infers the wake moment and fans a signed user.awake event out to OpenClaw, Home Assistant, or any URL" width="100%">

<br>

[![npm](https://img.shields.io/npm/v/wakehook?logo=npm&color=cb3837)](https://www.npmjs.com/package/wakehook)
[![ghcr](https://img.shields.io/badge/ghcr.io-wakehook-2496ED?logo=docker&logoColor=white)](https://github.com/robbeverhelst/wakehook/pkgs/container/wakehook)
![runtime](https://img.shields.io/badge/built%20with-Bun-000000?logo=bun)
![lang](https://img.shields.io/badge/TypeScript-3178c6?logo=typescript&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-43b581)
![providers](https://img.shields.io/badge/source-Google%20Health-4dd0e1)

</div>

---

## 🌅 The idea

You wake up. Your Fitbit knows. So why does *nothing happen?*

**wakehook** is the missing piece: a tiny, self-hosted service that watches your sleep data,
figures out the moment you actually **woke up**, and **broadcasts a signed `user.awake` event**
to anything you want — your AI agent, your smart home, a script, a webhook URL.

It's deliberately **not built for any one tool.** [OpenClaw](https://docs.openclaw.ai) is just
*one* subscriber, sitting next to Home Assistant, n8n, a smart lamp, or your own code.

> 🧠 wakehook states a **fact** — *"this person woke at 07:03"* — and broadcasts it.
> Every subscriber decides its own **behavior**. The bus knows nothing about their purpose.

📐 Full rationale & decision log in [`DESIGN.md`](./DESIGN.md).

## ☕ A morning, scripted

```
06:58  you stir, your Fitbit logs the end of sleep
07:00  your phone syncs → Google Health → wakehook            "sleep data changed"
07:00  wakehook: main sleep? ✓  ends this morning? ✓  not fired yet today? ✓  → FIRE
07:00  ┌─ OpenClaw       → "morning! here's your day, weather's clear, 2 overnight msgs"
       ├─ Home Assistant → bedroom lights fade up, coffee machine on
       └─ your script    → logs wake time to a spreadsheet
```

You didn't touch your phone. It just *happened.*

## 🤔 Why it has to exist

You can't point Google Health's webhook straight at OpenClaw (or anything else):

| Blocker | What goes wrong |
|---|---|
| **Semantics** | Google's webhook means *"sleep data changed"* — it also fires for naps, mid-night syncs, and edits. It is **not** "you woke up." Something must fetch the session and *infer* the wake. |
| **Payload** | Google speaks `{operation, healthUserId, intervals}`; your consumer speaks something else entirely. |
| **Handshake** | Google demands an ownership-verification challenge and a `204` ack with 7-day retries. Your agent's endpoint won't play along. |

wakehook is the translator that closes that gap — **generically**, so *anything* can subscribe.

## ⚙️ How it works

```
you wake → (phone syncs) → Google Health cloud ──POST──▶ /webhook
   └─ ack 204 → fetch session → infer wake → dedup ──▶ fan out signed user.awake
                                                         ├─▶ OpenClaw       → runs a workflow
                                                         ├─▶ Home Assistant → lamp on
                                                         └─▶ any URL        → its own behavior
```

The wake rule (every threshold configurable): fire when a session is the **main** sleep,
**ends today** inside a **morning window**, is **long enough**, and we **haven't already fired
today** — with a **supersede** re-fire to heal Fitbit's rare split-night logs.

Tuned to two priorities:

- 🛟 **Never miss a wakeup** — no freshness gate, so a late-syncing webhook still fires.
- ⚡ **Fire as fast as the data arrives** — we act on the first qualifying signal, zero batching.

> Latency floor is your phone syncing to the cloud (open the Fitbit app to force it instantly);
> wakehook itself adds ~zero delay.

## 📦 The event subscribers receive

```http
POST <subscriber-url>
X-Wake-Signature: sha256=<hmac of body with the subscriber's secret>   # only if "secret" is set
X-Wake-Event-Id: <user>:<wokeAt>

{ "event": "user.awake", "wokeAt": "2026-06-14T07:03:00+02:00",
  "user": "<healthUserId>", "source": "google-health",
  "session": { "start": "...", "end": "...", "durationMin": 431 } }
```

Every subscriber gets exactly this — one **vendor-neutral** event. The bus does
not format per-consumer; the consumer decides what it means. Per-subscriber knobs:

- **`secret`** *(optional)* — when set, the body is HMAC-SHA256 signed so the
  receiver can verify authenticity.
- **`signatureHeader`** *(optional, default `X-Wake-Signature`)* — header the
  signature rides in; **`signatureFormat`** is `prefixed` (`sha256=<hex>`, default)
  or `hex` (bare). Set these to match a receiver's expected header.
- **`headers`** *(optional)* — extra request headers to satisfy the receiver's
  own auth, e.g. `{ "Authorization": "Bearer <token>" }`.

**OpenClaw:** point `url` at a [mapped hook](https://docs.openclaw.ai/gateway/configuration-reference)
(`/hooks/<name>`), pass the gateway's hook token via `headers`, and let OpenClaw
turn the event into a wake/agent action with `hooks.mappings`. The
[`SKILL.md`](./SKILL.md) walks an agent through it.

**[Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks):**
point `url` at a Hermes webhook route (`:8644/webhooks/<route>`), set `secret` to
the route secret with `signatureHeader: "X-Webhook-Signature"`, `signatureFormat:
"hex"`, and write the route's `prompt` template (`{wokeAt}`, `{session.durationMin}`).
On loopback you can skip signing with Hermes's `INSECURE_NO_AUTH`.

### 🤖 Install the skill into your agent

[`SKILL.md`](./SKILL.md) (one skill, both agents) walks the agent through the
whole setup — install, configure, authorize, run, and wire the hook. Add it with:

```bash
# OpenClaw
openclaw skills install git:robbeverhelst/wakehook   # or: openclaw skills install wakehook (ClawHub)
# Hermes Agent — zero-infra tap (reads the root SKILL.md)
hermes skills tap add robbeverhelst/wakehook
```

## 🚀 Quick start

**Prerequisites:** [Bun](https://bun.sh) ≥ 1.3 (it's a Bun service — the npm package is
**Bun-only**, it imports `bun:sqlite`), and a Google Cloud project with the **Health API**
enabled, an **OAuth 2.0 client** (id + secret), and the `googlehealth.sleep.readonly` scope —
see [Google setup notes](#-google-setup-notes).

The simplest path is **poll mode**: wakehook pulls sleep from the API on a timer, so all traffic
is **outbound — no public URL or tunnel needed.** (Want *instant* fires? See
[Webhook mode](#-webhook-mode-advanced).)

**1 · Install**

```bash
bunx wakehook                 # run without installing — or: bun add wakehook
# or Docker:
docker run -v wakehook-data:/data --env-file .env ghcr.io/robbeverhelst/wakehook
```

**2 · Configure** — create `config.json` in your working directory:

```json
{
  "dbPath": "./wake.sqlite",
  "source": "google-health",
  "inference": {
    "timezone": "Europe/Brussels",
    "windowStart": "04:00",
    "windowEnd": "11:00",
    "minDurationMin": 180,
    "supersedeGapMin": 45
  },
  "google": { "mode": "poll", "pollIntervalMs": 300000, "pollLookbackMin": 720, "pollWindowOnly": true, "pollWindowMarginMin": 30 },
  "subscribers": [
    { "id": "openclaw", "url": "http://localhost:18789/hooks/wakehook", "headers": { "Authorization": "Bearer <openclaw-hooks-token>" } }
  ]
}
```

…and a `.env` with your OAuth credentials (keep these out of `config.json`):

```bash
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8080/oauth/callback
```

**3 · Authorize once** — opens a Google consent URL, then stores a refresh token in the sqlite
DB (it auto-refreshes forever after):

```bash
bunx wakehook-auth            # from source: bun run auth
```

**4 · Run it** — it now polls Google every 15 min and fans a signed `user.awake` out to your
subscribers, at most once per morning:

```bash
bunx wakehook                 # from source: bun run start  (bun run dev to watch)
```

No inbound URL anywhere. By default (`pollWindowOnly`) it only polls around the
morning window (`windowStart..windowEnd` ± `pollWindowMarginMin`) and stops once
it has fired for the day — so a short `pollIntervalMs` (e.g. 2–5 min) gives a fast
wake without hammering the API all day. Set `pollWindowOnly: false` to poll 24/7.

### 🧪 Test it without waiting for morning

```bash
curl -X POST http://localhost:8080/test/replay \
  -H "Authorization: Bearer $GOOGLE_WEBHOOK_AUTH_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{}'    # fires a synthetic wake "now"; pass {"end":"...","durationMin":420} to control it
```

### 📡 Webhook mode (advanced)

For *instant* fires, Google Health can **push** to wakehook instead of being polled: set
`"mode": "webhook"`, set `webhookAuthToken` (env `GOOGLE_WEBHOOK_AUTH_TOKEN` — the token Google
must present), expose `/webhook` over public HTTPS (Cloudflare Tunnel / reverse proxy / VPS —
wakehook makes **no ingress assumptions**), and register a Google Health **sleep** webhook
subscription pointing at it.

> ⚠️ **Status:** the **poll** path is verified end-to-end against the live API. The webhook
> *notification parsing* and the *subscription-creation* step are **not yet verified/implemented** —
> stick with poll unless you're ready to wire and test the push contract yourself. `"both"` runs
> poll with the webhook as an experimental safety net.

## 🔑 Google setup notes

- Create a Google Cloud project, enable the Health API, configure the OAuth consent screen,
  add yourself as a test user. Scope: `googlehealth.sleep.readonly`.
- **Publish the app to "In Production"** (still unverified, 100-user cap — fine for personal
  use) so the refresh token doesn't expire after 7 days (the "Testing" default).

## 🧩 Add your own provider

Google Health is just the first `Source`. The core (inference, dedup, fan-out) is
provider-agnostic, so a new provider touches **no core code**:

1. Implement the `Source` interface (`src/types.ts`) under `src/sources/<name>/`. A source
   declares one or both **capabilities**:
   - **`webhook`** (push) — the provider POSTs to `/webhook`
     *(Google Health, Fitbit Web, WHOOP, Withings, Oura, Sleep as Android…)*.
   - **`poll`** (pull) — wakehook polls it on a timer
     *(on-device Health Connect bridge, Open Wearables, plain REST APIs…)*.
2. Register it with **one line** in `src/sources/registry.ts`.
3. Select it via `"source": "<name>"` in config.

The server mounts `/webhook` only for push sources; the scheduler drives poll sources. Google
Health implements **both** (selectable via `google.mode`) — proof the interface carries either
kind with no core changes.

➕ **Receiver needs its own auth?** Set `headers` on the subscriber (e.g. a bearer token) — no code change.

## 🛠️ Stack

**Bun** · **Hono** · **`bun:sqlite`** — single portable service, shipped as a Docker image,
12-factor config. Core logic is unit tested (`bun test`).

## 📍 Status

v1: Google Health source + wake inference + signed fan-out of one neutral
`user.awake` event (per-subscriber `secret`/`headers`), with a generic push/poll
`Source` interface ready for more providers. The Google
sleep-response field mapping (`mapSession`) is isolated in one place so it can be confirmed
against the live API.

## 📄 License

MIT
