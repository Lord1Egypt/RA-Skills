---
name: wellness
description: A personal Wellness hub for OpenClaw. Use when users want an all-in-one way to connect their health/wellness apps and devices (wearables, workouts, sleep, nutrition, weight, vitals) and get unified daily/weekly summaries, insights, and reminders inside OpenClaw (any chat channel). Guides users to add data sources via official personal OAuth/API keys (Tier 1) or via phone OS health aggregators like Apple Health / Android Health Connect (Tier 2).
---

# Wellness (Health Hub)

Provide an **all-in-one wellness experience** in OpenClaw:

- Add the apps/devices you already use
- Connect them with official personal authorization (Tier 1) or OS aggregators (Tier 2)
- Generate unified digests (daily/weekly) and push them to any channel

This skill is the **hub**. It should:

1) Identify which sources the user has (WHOOP/Oura/Strava/Withings/…)
2) Install the matching source skill(s) from ClawHub
3) Guide the user through authorization
4) Pull + normalize data into a shared schema
5) Render a digest and optionally schedule it via cron

## Quick start

1) Ask the user which sources they use (wearables, workouts, nutrition, scales, etc.).
2) Ask where they are authorizing OAuth:
   - **Phone/remote** (recommended): user opens the auth link on any device and copy/pastes the redirect URL/code back into chat.
   - **Desktop same-machine** (optional): user authorizes in a browser on the same machine that runs OpenClaw and can use loopback redirects (127.0.0.1) for a no-copy/paste fast path.
3) For each source, consult the catalog: `references/catalog.md`.
4) Install the source skill(s) (via `clawhub install <slug>`), then run the source skill’s connect/fetch workflow.
5) Produce a digest using the normalized schema in `references/schema.md`.

## Source selection

- Prefer Tier 1 sources first (official OAuth/API key, user can self-authorize).
- Use Tier 2 (Apple Health / Android Health Connect) to fill gaps and unify multiple devices.

## Catalog + schema

- Source catalog: `references/catalog.md`
- Unified normalized schema: `references/schema.md`
- Digest templates: `references/digest-templates.md`
- Tier 2 bridge (Apple Health / Health Connect): `references/bridge.md`
- iOS exporter (Shortcuts): `references/exporter-ios-shortcuts.md`
- Android exporter (automation): `references/exporter-android-automation.md`
- Ingest protocol: `references/ingest-protocol.md`

## Daily digest + push

To generate a unified digest, use `scripts/wellness_digest.py` to merge normalized source outputs (Tier 1) and optionally include the newest Tier 2 bridge inbox payload.

To prepare a sendable message (and optionally emit a `message` tool template), use `scripts/wellness_push.py`.

## Guardrails

- Do not use unofficial scraping or credential capture.
- Keep tokens local (never paste tokens back to chat). Store in user-controlled paths.
- Keep each source integration in its own skill where possible; the hub orchestrates.
