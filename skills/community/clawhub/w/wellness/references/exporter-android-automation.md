# Android exporter (Automation) — Health Connect → Wellness Bridge

Goal: push daily aggregates from Android Health Connect to the Wellness Bridge without publishing an app.

Reality check:
- Android automation tools (Tasker/Automate) can POST JSON easily.
- Reading Health Connect data directly may require a compatible exporter/plug-in or using an existing app that can export metrics.
- Start with what you can reliably access (steps/sleep) and expand.

## What users will do

1) Start the bridge + tunnel and copy Sync URL + Token.

2) Choose an automation tool:
- Tasker (popular)
- Automate (flow-based)

3) Configure a daily job that POSTs JSON to:
- `https://<tunnel-host>/ingest`

Headers:
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

Body: JSON matching `references/ingest-protocol.md` with:
- `source`: `health_connect`

## Practical MVP

If direct Health Connect reads are hard:
- Use any app that can export a daily summary (CSV/JSON) and have the automation upload a reduced JSON.
- Or manually enter a small set of numbers (steps/sleep/weight) once per day.

## Troubleshooting

- 401 Unauthorized: token mismatch
- 404: wrong endpoint (must be `/ingest`)
- Tunnel URL changes: update automation target
