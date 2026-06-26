---
name: openclaw-guard-skill
description: Local VAIBot Guard skill for OpenClaw. Use to run the guard service, enforce tool decisions via the OpenClaw circuit-breaker plugin, manage approvals, and validate guard receipts/audit logs. Also use when installing/operating the guard systemd user service or running guard unit tests.
---

# OpenClaw Guard Skill (VAIBot v2.1)

Provide a **local policy decision service** plus a CLI to gate OpenClaw tool calls and write **tamper-evident audit logs** in `.vaibot-guard/`.

## Sensitive credentials
- `VAIBOT_GUARD_TOKEN` — bearer token for Guard endpoints (recommended)
- `VAIBOT_API_KEY` — optional: anchor receipts to VAIBot `/prove`

Treat these as secrets.

## HTTP API (guard service)
- `GET /health`
- `POST /v1/decide/exec` + `POST /v1/finalize` (shell exec flows)
- `POST /v1/decide/tool` + `POST /v1/finalize/tool` (OpenClaw tool gating)
- `POST /v1/approvals/list` + `POST /v1/approvals/resolve` (approve/deny)
- `POST /v1/flush` (checkpoint flush)
- `POST /api/proof` (Merkle inclusion proofs)

Auth:
- If `VAIBOT_GUARD_TOKEN` is set, require `Authorization: Bearer <token>` on protected endpoints.

## Manual quick start (no persistence)

Run the service in the foreground:

```bash
export VAIBOT_GUARD_HOST=127.0.0.1
export VAIBOT_GUARD_PORT=39111
export VAIBOT_POLICY_PATH=references/policy.default.json
export VAIBOT_WORKSPACE="$(pwd)"
export VAIBOT_GUARD_LOG_DIR="$VAIBOT_WORKSPACE/.vaibot-guard"
export VAIBOT_GUARD_TOKEN="<random-token>"

node scripts/vaibot-guard-service.mjs
```

Smoke test:

```bash
curl -s http://127.0.0.1:39111/health
```

## OpenClaw enforcement (recommended)

Use the **OpenClaw circuit-breaker plugin** so tool calls are intercepted at the gateway (not just “model follows instructions”).

Reference:
- `references/openclaw-bridge.md`

## Optional: systemd user service

Install a user service + env file via the CLI helper:

```bash
node scripts/vaibot-guard.mjs install-local
```

This writes:
- `~/.config/systemd/user/vaibot-guard.service`
- `~/.config/vaibot-guard/vaibot-guard.env`

Templates live under `references/systemd/` for reference.

## Policy + schemas

See:
- `references/policy.md`
- `references/policy.default.json`
- `references/receipt-schema.md`
- `references/checkpoint-schema.md`
- `references/inclusion-proofs.md`
- `references/required-mode.md`

## Tests

Run guard service tests (no external deps):

```bash
node --test tests/guard-service.test.mjs
```
