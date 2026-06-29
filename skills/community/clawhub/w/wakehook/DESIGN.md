# wakehook — Design

A small, **vendor-neutral "wake detection" webhook bus.** It subscribes to a health
data provider (v1: **Google Health API**, for Fitbit devices), infers when its person
actually **woke up**, and **fans out** a clean, signed `user.awake` event to *every*
subscriber. It is not built for any one consumer — OpenClaw is simply one subscriber
among many (Home Assistant, n8n, a raw URL, your own script…).

> The bus states a **fact** ("this person woke at 07:03") and broadcasts it. Each subscriber
> decides its own **behavior** (OpenClaw runs a morning routine; a lamp turns on; a script
> logs it). The bus knows nothing about any subscriber's purpose.

---

## Why this exists (the gap)

You cannot point Google Health's webhook straight at OpenClaw. Three hard blockers:

1. **Semantics** — Google's webhook fires on `operation: UPSERT` meaning *"sleep data
   changed,"* which also fires for naps, mid-night syncs, and after-the-fact edits. It is
   **not** a "you woke up" event. Something must fetch the session and *infer* the wake.
2. **Payload mismatch** — Google sends `{operation, healthUserId, dataType, intervals}`;
   OpenClaw expects its own `{action, goal}` / `{text, mode}` shapes.
3. **Handshake** — Google requires an endpoint-ownership verification challenge (POST with
   auth → `200`, POST without → `401/403`) and a `204` ack with up-to-7-day retries.
   OpenClaw's endpoint won't perform that.

This service is the translator that closes the gap — and it does so generically, so any
consumer (OpenClaw, Home Assistant, n8n, a raw URL) can subscribe.

---

## Runtime flow

```
  you wake
     │  (Fitbit device → phone → Fitbit/Google cloud sync)
     ▼
  Google Health cloud ──HTTP POST──▶ ADAPTER (/webhook)      "sleep data changed (UPSERT)"
                                        │
                                        │ 1. ack 204 immediately
                                        │ 2. fetch sleep session (Google Health API)
                                        │ 3. apply wake-inference rule
                                        │ 4. dedup against state (bun:sqlite)
                                        ▼
                                     ADAPTER ──fan out signed `user.awake`──▶ ALL SUBSCRIBERS
                                                                   ├─▶ OpenClaw  → runs workflow
                                                                   ├─▶ Home Assistant → lamp on
                                                                   └─▶ any URL → its own behavior
```

Latency floor is **Fitbit's phone→cloud sync** (we add ~0). Opening the Fitbit app forces
an instant sync; background sync is ~15 min. Documented as a setup note, not solvable in code.

---

## Architecture (pluggable, config-driven)

```
[ Source adapter ] ──▶ [ Core: normalize → wake-inference → dedup/state ] ──▶ [ Subscriber fan-out ]
 GoogleHealthSource        provider-agnostic WakeEvent (user.awake)            for each subscriber:
 (v1)                                                                            POST signed event
 + FitbitWebSource (later)                                                       ├─ generic (default)
 + HealthConnectSource (later)                                                   └─ OpenClaw preset
```

- **Source interface** — yields normalized `SleepSession`s via one or both **capabilities**:
  `webhook` (push: handshake + parse notification + fetch) and `poll` (pull: timed `run()`).
  A config-driven **registry** (`src/sources/registry.ts`) selects the active source by name;
  adding a provider is a one-line registration + a file, with no core changes. v1 ships
  `GoogleHealthSource` (webhook). The server mounts `/webhook` only for push sources; a
  scheduler drives poll sources.
- **Core** — stateless inference + stateful dedup. Provider-agnostic.
- **Subscribers** — a configured list of consumer endpoints. The core **fans the `WakeEvent`
  out to all of them**, each independently signed and retried. A subscriber is `{ url, secret,
  preset }` where `preset` defaults to `generic` (raw signed event) or `openclaw` (thin
  translation to OpenClaw's `/hooks/wake`). OpenClaw is just one entry. Nothing about
  host/provider/consumer is hardcoded; the bus has no knowledge of any subscriber's purpose.
  (A dynamic `/subscriptions` register/unregister API is a clean later addition; v1 is
  config-defined.)

### Stack
- **Bun** + **Hono** (HTTP routes: `/webhook`, `/healthz`, `/test/replay`)
- **`bun:sqlite`** for dedup state + OAuth tokens
- Shipped as a **Docker** image; 12-factor config (env + optional file). No ingress baked in —
  operator fronts it with Cloudflare Tunnel / reverse proxy / VPS / serverless as they like.

---

## Wake-inference rule

On each `UPSERT` webhook: ack `204`, fetch the affected sleep session, then:

```
fire user.awake  IF
    session.isMainSleep                       # ignore naps
    AND session.end.date == today (local tz)  # ignore edits to prior days
    AND window.start <= session.end.time <= window.end   # configurable, e.g. 04:00–11:00
    AND session.durationMin >= minDurationMin            # weak guard, e.g. 180
    AND ( not firedToday
          OR session.end > lastFiredEnd + supersedeGapMin )   # heals split-night, re-fires once
THEN
    emit immediately
    record { firedToday=true, lastFiredEnd=session.end }
```

**Design intent (locked priorities): never miss a wakeup; fire as fast as possible.**
- **No upper freshness gate** → a late-syncing webhook still fires (slightly late) instead of
  being rejected → never miss.
- **Fire on first qualifying arrival** → fastest the data can physically be acted on.
- **Morning-window lower bound** is the primary guard against a too-early/false fire from a
  Fitbit "first-part" split-sleep log (Fitbit splits a sleep log if you're awake >1h mid-night
  and the device syncs during the gap; logs <1h apart are stitched). A first-part log ending at
  e.g. 04:00 falls below the window and won't fire.
- **Supersede re-fire** self-heals the rare split-night where a later main-sleep ends well
  after one we already fired on.

All thresholds (`window`, `minDurationMin`, `supersedeGapMin`, timezone) are config.

---

## Event contract (the "standard" part)

Neutral, signed, consumer-agnostic. Delivered to every sink.

```json
{
  "event": "user.awake",
  "wokeAt": "2026-06-14T07:03:00+02:00",
  "user": "<healthUserId>",
  "source": "google-health",
  "session": { "start": "2026-06-13T23:52:00+02:00", "end": "2026-06-14T07:03:00+02:00", "durationMin": 431 }
}
```

The **same event is broadcast to every subscriber**. Each subscriber receives it independently.

- **Signing:** `X-Wake-Signature: sha256=<hmac>` over the raw body using that subscriber's
  shared secret, so each consumer can verify authenticity.
- **`generic` preset (default):** posts the raw signed event above to the subscriber's URL.
  This is the vendor-neutral contract anything can consume.
- **`openclaw` preset:** translates the event into a factual nudge that lets OpenClaw decide,
  e.g. `POST /hooks/wake { "text": "You woke at 07:03 (slept 7h11m).", "mode": "now" }`.
  Opt-in alt mapping: `create_flow { goal: "<operator-configured>" }`. Behavior lives in the
  subscriber, never in the bus.

---

## State (bun:sqlite)

- `oauth_tokens(user, access_token, refresh_token, expires_at)` — refreshed automatically.
- `wake_state(user, fired_date, last_fired_end)` — once-per-day dedup + supersede tracking.
- `delivery(subscriber, event_id, status, attempts)` — per-subscriber fan-out delivery +
  retry tracking (one slow/failing subscriber must not block the others).
- Keyed by `healthUserId` → single-user today, multi-user-ready without schema change.

---

## OAuth / onboarding (one-time)

1. Create a Google Cloud project, enable the Health API, configure the OAuth consent screen.
2. **Publish the app to "In Production"** (still unverified, 100-user cap — fine for personal
   use). This is required so refresh tokens don't expire after 7 days (the "Testing" default).
3. Run a one-time local authorization flow to mint the refresh token (stored in sqlite).
4. Create the Google Health **sleep webhook subscription** pointing at the adapter's public
   `/webhook` URL; the adapter answers the verification challenge automatically.

Scope: `googlehealth.sleep.readonly`.

---

## Out of scope for v1 (clean extension points exist)

- Additional sources: Fitbit Web API (turns down ~Sept 2026), Health Connect on-device bridge.
- Additional sinks: Home Assistant, n8n, generic fan-out to multiple URLs.
- Multi-tenant onboarding / dashboard / hosted SaaS.
- `user.asleep` / other lifecycle events.

---

## Decisions log

| Decision | Resolution |
|---|---|
| Scope | Open-source, self-hostable, vendor-neutral (you are first user) |
| v1 breadth | Minimal Google Health→OpenClaw path with clean pluggable interfaces |
| Data source | Google Health API (solo access confirmed; publish OAuth to Production for long-lived tokens) |
| Wake rule | `isMainSleep` + `end.date==today` + morning window + min-duration + once/day |
| Reliability | No upper freshness gate (never miss); fire on first arrival (fastest); supersede re-fire heals split-nights |
| Hosting | Deployment-agnostic portable service (Docker); no ingress baked in |
| Stack | Bun + Hono + `bun:sqlite` |
| Output | Fan-out: same neutral signed `user.awake` event broadcast to **all** subscribers; OpenClaw is one preset among many; each subscriber decides its own behavior |
