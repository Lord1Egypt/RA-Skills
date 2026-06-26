# Sonoff Access and Authentication

Use this guide to keep auth handling and control mode coherent.

## Credentials

- Cloud mode uses `EWELINK_API_TOKEN` from environment.
- LAN and DIY local mode may not require cloud token but still require device eligibility and reachability checks.
- iHost local API uses short-lived local access token flow.

## Auth Rules

1. Load secrets from environment, never from chat.
2. Avoid persisting raw token values in `~/sonoff/` files.
3. Use least-privilege account scope and rotate tokens when possible.
4. Re-authenticate after repeated unauthorized responses; do not blind-retry writes.

## iHost Token Pattern

Typical local sequence:
- request bridge access token from local iHost endpoint
- execute REST calls with that token
- subscribe to SSE stream for event confirmation when needed

## Practical Safeguards

- Verify target device identity before every write.
- Keep cloud id, LAN id, and iHost id mapping in one table.
- Stop rollout on repeated auth or permission drift.
