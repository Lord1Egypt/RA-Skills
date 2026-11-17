---
name: secret-drop
description: "Password/API key in Telegram/Discord/Slack or OpenClaw-masked: request pwpush/snappwd link, ingest it, or share stored secrets as one-time link."
---

# secret-drop

Move secrets into and out of OpenClaw chat without exposing plaintext in transcripts, model context, tool arguments, or logs.

## Route the request

| Trigger | Action |
|---|---|
| User says they want to send a password or API key | Reply: "Don't paste it here. Put it into https://pwpush.com with 1 view, 1 day, and the retrieval step enabled, then send me the exact generated `/r` link." |
| User already pasted plaintext or OpenClaw shows `***` / a shortened mask | Do not guess or request another plaintext paste. Send the same Password Pusher instruction. |
| User sends a Password Pusher `/r` or SnapPwd link | Run the inbound procedure. |
| User asks for a locally stored password or API key | Run the outbound procedure and return only the generated one-time URL. |

## Inbound: user to agent

Run after the user supplies the link, destination, and variable name:

```bash
python3 <skill-directory>/scripts/secret-drop ingest "<URL>" \
  --to openclaw-env \
  --name "VARIABLE_NAME" \
  --json
```

Use `--to dotenv --path <path>`, `--to file --path <path>`, or `--to openclaw-store` when requested. Add `--restart-gateway` only when the task authorizes the restart.

For Password Pusher, require the exact generated retrieval-step URL ending in `/r`. Never remove `/r` or rebuild a bare `/p/<token>` URL because messenger link previews can consume the push.

Verify `ok: true`; report destination, name, and byte count. Never print the plaintext.

## Outbound: agent to user

Use only the local source authorized by the request:

```bash
# ~/.openclaw/.env
python3 <skill-directory>/scripts/secret-drop share \
  --from openclaw-env \
  --name "VARIABLE_NAME" \
  --json

# Project dotenv
python3 <skill-directory>/scripts/secret-drop share \
  --from dotenv \
  --path "/path/to/.env" \
  --name "VARIABLE_NAME" \
  --json

# Text file
python3 <skill-directory>/scripts/secret-drop share \
  --from file \
  --path "/path/to/secret" \
  --json
```

Verify `ok: true`, `expire_views: 1`, `expire_days: 1`, `retrieval_step: true`, and that `url` ends in `/r`. Deliver only that URL to the authorized requester; use a private conversation instead of a group when available.

## Rules

1. Never use `cat`, `echo`, `grep`, shell expansion, or command arguments to extract plaintext.
2. Never repeat plaintext from chat or local storage.
3. Never reconstruct Password Pusher links from `url_token`; preserve the API-returned `html_url`.
4. Do not add rotation lectures. Route the user directly to the one-time-link flow.
