---
name: wakehook
description: Install, configure, authorize and run wakehook so the user's agent (OpenClaw or Hermes) runs their morning routine when they wake up. wakehook turns Google Health / Fitbit sleep data into a neutral user.awake event and POSTs it to the agent's inbound webhook, which turns it into a wake/agent action. Use when the user wants wake-triggered automations, mentions wakehook, or asks to "do something when I wake up".
homepage: https://github.com/robbeverhelst/wakehook
metadata:
  hermes:
    category: automation
    tags: [wake, sleep, google-health, fitbit, morning, webhook]
---

# wakehook → your agent

`wakehook` is a tiny self-hosted service that watches the user's sleep data
(Google Health / Fitbit), detects the moment they **woke up**, and POSTs the
user's agent a neutral `user.awake` event so the morning routine runs itself — at
most once per morning. The agent maps that event into a wake/agent action (its
native pattern), so wakehook stays vendor-neutral.

This works with **OpenClaw** and **Hermes Agent** — they both ingest a webhook and
template it. Everything below is shared except **Step 1**, where you pick the
agent. Work through the steps in order. **Ask the user** at the decision points
instead of assuming. Do not improvise from the README — these steps are verified.

## Prerequisites (check, don't assume)

1. **Bun ≥ 1.3** — `bun --version`; install with `curl -fsSL https://bun.sh/install | bash`.
   wakehook is Bun-only (`bun:sqlite`); never run it with Node.
2. **Google OAuth credentials** — a Google Cloud project with the **Health API**
   enabled and the `googlehealth.sleep.readonly` scope, plus an **OAuth 2.0
   client** (client id + secret). An API key will NOT work; sleep data needs
   user-consented OAuth. Ask the user for the id + secret (reuse their existing
   Google project if they have one).

## Step 1 — wire wakehook to the agent (pick OpenClaw **or** Hermes)

wakehook POSTs the raw `user.awake` event to the agent's inbound webhook; the
agent templates it into a wake. Do the subsection for the user's agent — it gives
both the **agent-side config** and the matching **wakehook subscriber** (drop the
subscriber into `config.json` in Step 3).

### Option A — OpenClaw (mapped hook)

In the OpenClaw gateway config, enable hooks and add a mapping:

```json5
{
  hooks: {
    enabled: true,
    path: "/hooks",            // must not be "/"
    token: "<HOOKS_TOKEN>",    // any strong random string
    mappings: [
      {
        match: { path: "wakehook" },   // matches POST /hooks/wakehook
        action: "wake",
        wakeMode: "now",
        name: "wakehook",
        // action "wake" builds its text from textTemplate (NOT messageTemplate —
        // that's only for action "agent"; the wrong one returns HTTP 400):
        textTemplate: "You woke at {{wokeAt}} (slept {{session.durationMin}} min).",
      },
    ],
  },
}
```

Gateway address: OpenClaw's docs examples use `127.0.0.1:18789` — confirm the
user's port. `/hooks/*` is gated by the token in a header (`Authorization: Bearer`
or `x-openclaw-token`). wakehook subscriber:

```json
{ "id": "openclaw", "url": "http://<host>:<port>/hooks/wakehook",
  "headers": { "Authorization": "Bearer <HOOKS_TOKEN>" } }
```

### Option B — Hermes Agent (webhook route)

In the Hermes webhook config, add a route with a `prompt` template + secret:

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      routes:
        wakehook:
          secret: "<ROUTE_SECRET>"
          prompt: "The user woke at {wokeAt} (slept {session.durationMin} min). Run the morning routine."
          # deliver: telegram   # optional: send the result to a chat
```

Hermes verifies an HMAC signature; wakehook signs with the route secret under the
header Hermes expects. wakehook subscriber:

```json
{ "id": "hermes", "url": "http://<host>:8644/webhooks/wakehook",
  "secret": "<ROUTE_SECRET>", "signatureHeader": "X-Webhook-Signature", "signatureFormat": "hex" }
```

> On loopback you can skip signing entirely with Hermes's `INSECURE_NO_AUTH` and
> drop `secret`/`signatureHeader`/`signatureFormat`.

## Step 2 — choose how wakehook gets the sleep data (ask the user)

Two modes — confirm which they want; **don't assume**:

- **poll** *(recommended default)* — wakehook pulls from Google on a timer.
  **No public URL / tunnel / open port** (all outbound). By default it only polls
  around the morning window and stops once it has fired today (`pollWindowOnly`),
  so a short `pollIntervalMs` (5 min default) is cheap — wake is detected within
  one interval. This path is verified end-to-end.
- **webhook** — Google pushes the instant data lands → fires immediately, but
  requires a **public HTTPS endpoint** for wakehook plus registering a Google
  Health sleep subscription. ⚠️ This path is **not yet verified** — only choose
  it if the user explicitly wants instant fires and can expose an endpoint.

If the user has no preference, use **poll**.

## Step 3 — configure wakehook

Create **`config.json`** in the working directory. Set `timezone` to the user's
IANA zone and drop in the **subscriber from Step 1** (the OpenClaw or Hermes one):

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
    { "id": "openclaw", "url": "http://<host>:<port>/hooks/wakehook", "headers": { "Authorization": "Bearer <HOOKS_TOKEN>" } }
  ]
}
```

> The `subscribers` array above uses the **OpenClaw** entry; swap it for the
> **Hermes** entry from Step 1 if that's the agent. You can list both to fan out
> to multiple agents.

> No `preset` needed — `generic` (the raw event) is the default and is what both
> agents' mappings/routes expect. The subscriber's auth (the OpenClaw bearer or the
> Hermes secret/signature) must match the agent config from Step 1.
>
> If the user chose **webhook** mode instead: set `"google"` to
> `{ "mode": "webhook", "webhookAuthToken": "<random>" }`, also put
> `GOOGLE_WEBHOOK_AUTH_TOKEN` in `.env`, expose wakehook's `/webhook` over public
> HTTPS, and register a Google Health sleep subscription pointing at it. (Unverified.)

Create **`.env`** (keep secrets out of `config.json`):

```bash
GOOGLE_CLIENT_ID=<client-id>
GOOGLE_CLIENT_SECRET=<client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8080/oauth/callback
```

Ensure `http://localhost:8080/oauth/callback` is an authorized redirect URI on the OAuth client.

## Step 4 — authorize once

```bash
bunx wakehook-auth
```

Prints a Google consent URL — give it to the user to open and approve. It stores
a refresh token in `./wake.sqlite` and auto-refreshes forever (one-time step).
If Google returns HTTP 400, the OAuth client is missing the
`localhost:8080/oauth/callback` redirect URI — add it and retry.

## Step 5 — run it

```bash
bunx wakehook
```

(Docker alt: `docker run -v wakehook-data:/data --env-file .env ghcr.io/robbeverhelst/wakehook`.)
Keep it running (long-lived process / service). In poll mode it polls Google
every `pollIntervalMs` **around the morning window only** (set `pollWindowOnly:
false` to poll all day) and, on the morning wake, POSTs the agent once.

## Step 6 — decide what happens on wake (optional)

By default the Step-1 hook just nudges the agent. To make waking up *do*
something, shape the behavior on the **agent side** (the OpenClaw mapping or the
Hermes route `prompt`) — not in wakehook. wakehook only supplies the trigger; the
actual abilities (calendar, weather, messages, …) come from the **agent's own
skills/tools** — install/enable those separately.

For OpenClaw the lever is the mapping; for Hermes it's the route `prompt` (and
`deliver:`). OpenClaw mapping examples:

**A — simple nudge, routine in the prompt** (`action: "wake"`): make
`textTemplate` the instruction the main session executes.

```json5
{
  match: { path: "wakehook" },
  action: "wake",
  wakeMode: "now",
  textTemplate: "Good morning — the user just woke ({{wokeAt}}). Run the morning routine: review today's calendar, summarize overnight messages, and give the weather.",
}
```

**B — full routine run on a dedicated agent** (`action: "agent"`): route to an
agent that has the relevant skills, and deliver the result to a chat surface.

```json5
{
  match: { path: "wakehook" },
  action: "agent",
  agentId: "morning",          // an agent you've set up with calendar/weather/etc. skills
  wakeMode: "now",
  messageTemplate: "User woke at {{wokeAt}} (slept {{session.durationMin}} min). Produce the morning briefing.",
  deliver: true,               // send the result back to a chat surface…
  channel: "last",             // …e.g. Telegram/Discord (defaults to last used)
}
```

Note: you generally **don't** trigger a cron from this — wakehook *is* the real
wake signal, so it replaces guessing a fixed time. Just run the task on the event.
The capabilities themselves are separate agent skills; this step only wires *when*
and *what to ask for*.

## What the agent receives

wakehook POSTs the raw, neutral event; the agent's mapping/route templates it:

```
POST http://<host>:<port>/<your-agent-route>
Content-Type: application/json
<auth header per Step 1: Authorization: Bearer …  (OpenClaw)  or  X-Webhook-Signature: …  (Hermes)>

{ "event": "user.awake", "wokeAt": "2026-06-13T08:04:00Z", "user": "self",
  "source": "google-health",
  "session": { "start": "...", "end": "2026-06-13T08:04:00Z", "durationMin": 464 } }
```

The agent turns this into a `now` wake with the templated text — handle that as
the trigger to run the morning routine. wakehook also sends `X-Wake-Event-Id` for
idempotency. Fires at most once per morning.

## Verify without waiting for morning

```bash
curl -X POST http://localhost:8080/test/replay \
  -H 'Content-Type: application/json' -d '{}'
```

Injects a synthetic wake "now" and delivers it exactly like a real one — confirm
the agent maps it and runs the routine.

## Gotchas

- **Bun-only** — never run with Node.
- **Auth must match the agent (else 401):** OpenClaw — the `Authorization` bearer
  must equal the gateway `hooks.token`, hooks **enabled**, and the **mapping**
  exists. Hermes — `secret` must equal the route secret and `signatureHeader` /
  `signatureFormat` must match (`X-Webhook-Signature` / `hex`), with the route
  defined; or use `INSECURE_NO_AUTH` on loopback.
- **poll** needs the OAuth creds but **no inbound URL**; **webhook** is instant
  but unverified — prefer poll unless the user asks otherwise.
- A Google **API key is not enough** — it needs the OAuth client + `wakehook-auth`.
- **OpenClaw HTTP 400 `hook mapping requires text`** → an `action: "wake"` mapping
  must use **`textTemplate`** (only `action: "agent"` uses `messageTemplate`).
- If the hook returns 200 but nothing happens, check the OpenClaw version (a known
  issue affected some 2026.3.x builds) and that the mapping `action: "wake"` is set.

Source + full docs: https://github.com/robbeverhelst/wakehook
