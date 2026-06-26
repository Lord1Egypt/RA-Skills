---
name: retarus-sms4a
description: Send SMS jobs and check SMS delivery status through the Retarus SMS for Applications REST API. Use when Codex or OpenClaw needs to create SMS jobs, inspect per-recipient delivery results for a Retarus job ID, work from the SMS4A OpenAPI schema, or route requests across the `eu`, `de1`, and `de2` datacenters with the required `eu` status fallback to both German datacenters.
---

# Retarus SMS4A

## Overview

Use this skill for operational work with the Retarus SMS for Applications API: prepare or validate SMS job payloads, send jobs, and fetch per-recipient status for a `jobId`.

Prefer the helper script in `scripts/sms4a_api.py` instead of hand-writing HTTP calls. It already handles Basic Auth, simple payload construction, full-payload file input, datacenter selection, and the `eu` status fallback across `de2` and `de1`.

## Quick Start

1. Resolve credentials from the secret store into one of these supported inputs:
   - `RETARUS_SMS4A_USERNAME` and `RETARUS_SMS4A_PASSWORD`
   - `RETARUS_SMS4A_SECRET_FILE` pointing to a JSON or `.env`-style file with `username` and `password`
   - The default local secret file path `~/.openclaw/secrets/retarus-sms4a.env` or `~/.openclaw/secrets/retarus-sms4a.json`
   - Explicit `--username` and `--password` flags only for local testing
2. Send a simple SMS job:

```bash
python3 scripts/sms4a_api.py send \
  --datacenter eu \
  --text "Your access code is 123456" \
  --recipient +4917600000000 \
  --status-requested
```

3. Check recipient status for a job:

```bash
python3 scripts/sms4a_api.py status --job-id J.20221116-102407.583-0lajfsfmoXIZJO93PQ
```

## Datacenter Rules

- Use `eu` as the default send endpoint unless the user explicitly wants `de1` or `de2`.
- Do not rely on the `eu` hostname for status lookups. The `eu` endpoint is DNS-balanced across `de1` and `de2`, so a status lookup must try both datacenters.
- The `status` command defaults to `--datacenter auto`, which tries `de2` first and then `de1`.
- If the user explicitly prefers `de1` or `de2`, still try both datacenters and use the chosen one only as the first lookup target.

## Sending Workflow

- For common one-message jobs, pass `--text` and one or more `--recipient` values.
- For advanced jobs, pass `--payload-file` with a JSON body matching the OpenAPI `JobRequest` schema.
- Use `--dry-run` first if you want to validate payload assembly without sending anything.
- Return the created `jobId` and the datacenter that accepted the job.

## Status Workflow

- Use `status --job-id ...` to query `GET /sms?jobId=...`.
- Return the successful datacenter together with the recipient reports.
- If one datacenter returns `404` or `500`, continue with the next datacenter.
- If both datacenters fail, report both attempts and their response codes.

## Credential Handling

- Never hardcode credentials into the skill files.
- Prefer secret-store backed environment injection.
- Prefer the standard local secret path `~/.openclaw/secrets/retarus-sms4a.env` for operator-managed credentials on an OpenClaw host.
- If a secret file is used, support either:
  - JSON: `{"username":"...","password":"..."}`
  - `.env` style:

```dotenv
RETARUS_SMS4A_USERNAME=...
RETARUS_SMS4A_PASSWORD=...
```

## Reference

- Read `references/api.md` for the server aliases, supported helper-script options, and the subset of the OpenAPI schema this skill uses most often.
