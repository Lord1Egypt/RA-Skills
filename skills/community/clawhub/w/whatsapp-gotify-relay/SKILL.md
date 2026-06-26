---
name: "openclaw"
description: "Use when operating or extending this WhatsApp Gotify relay as the bridge to OpenClaw. Prefer Unix tools for Docker, logs, Gotify queue checks, webhook validation, and relay smoke tests."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - rg
        - sed
        - curl
        - docker
        - npm
        - git
    skillKey: "openclaw"
    homepage: "https://github.com/jr551/gotify-whatsapp-queue"
---

# OpenClaw

Use this skill when working on this repository as the WhatsApp bridge for OpenClaw.

## Purpose

This project sits between WhatsApp and OpenClaw.

It does two directions of communication:

1. OpenClaw sends outbound WhatsApp jobs through Gotify.
2. The relay sends inbound WhatsApp events and connection status back to OpenClaw through webhooks.

## Bridge model

### Outbound path

OpenClaw posts JSON into the Gotify outbox application:

```json
{
  "type": "send",
  "to": "+12025550101",
  "text": "hello from openclaw"
}
```

The relay polls that outbox, sends to WhatsApp, deletes the queue item on success, and emits a `send_result`.

### Inbound path

OpenClaw receives webhook JSON from the relay.

Webhook event types:

- `conversation`
- `send_result`
- `status`

Only meaningful WhatsApp activity should produce `conversation` events. History sync, protocol chatter, and other Baileys internals should stay filtered out.

## Payload shape

The relay should keep payloads flat and readable.

### Conversation

```json
{
  "type": "conversation",
  "relay": "whatsapp-gotify-relay",
  "direction": "inbound",
  "jid": "12025550101@s.whatsapp.net",
  "senderJid": "12025550101@s.whatsapp.net",
  "pushName": "John",
  "timestamp": 1776948451,
  "messageId": "ABC123",
  "text": "hello",
  "contentType": "text"
}
```

### Send result

```json
{
  "type": "send_result",
  "relay": "whatsapp-gotify-relay",
  "status": "sent",
  "requestId": 5544,
  "to": "12025550101@s.whatsapp.net",
  "messageId": "3EB0...",
  "error": null,
  "timestamp": "2026-04-23T12:48:56.415Z"
}
```

### Status

```json
{
  "type": "status",
  "relay": "whatsapp-gotify-relay",
  "connection": "open",
  "phase": "connected",
  "qr": null,
  "statusCode": null,
  "details": null,
  "timestamp": "2026-04-23T12:48:56.415Z"
}
```

If WhatsApp remains disconnected, the relay sends a `status` reminder every 3 hours by default.

## Public relay env vars

The relay runtime env surface is:

- `PORT`
- `APP_LOG_LEVEL`
- `WHATSAPP_AUTH_DIR`
- `WHATSAPP_PAIRING_NUMBER`
- `WHATSAPP_SYNC_FULL_HISTORY`
- `GOTIFY_BASE_URL`
- `GOTIFY_EVENTS_APP_TOKEN`
- `GOTIFY_OUTBOX_TOKEN`
- `GOTIFY_OUTBOX_APPLICATION_ID`
- `GOTIFY_POLL_INTERVAL_MS`
- `GOTIFY_EVENTS_PRIORITY`
- `GOTIFY_RESULTS_PRIORITY`
- `WEBHOOK_URL`
- `WEBHOOK_BEARER_TOKEN`
- `WEBHOOK_TIMEOUT_MS`
- `WEBHOOK_DISCONNECTED_INTERVAL_MS`
- `RELAY_NAME`

## OpenClaw-side env concepts

On the OpenClaw side, the important configuration concepts are:

- Gotify base URL
- Gotify outbox application id
- Gotify outbox write token
- webhook shared secret or bearer token expected from the relay
- relay name if multiple relays exist

Keep the names OpenClaw already uses if they exist. Do not rename OpenClaw env vars just to match the relay.

## Preferred tools

Prefer Unix tools and simple shell commands:

- `rg`
- `sed -n`
- `npm test`
- `docker compose ps`
- `docker compose logs --tail=... connector`
- `docker compose up -d --build connector`
- `curl`
- `git status --short`

## Common operations

### Run tests

```bash
npm test
```

### Rebuild the relay

```bash
docker compose up -d --build connector
```

### Follow relay logs

```bash
docker compose logs -f connector
```

### Inspect the outbox queue

```bash
curl -sS "${GOTIFY_BASE_URL}/application/${GOTIFY_OUTBOX_APPLICATION_ID}/message?token=${GOTIFY_OUTBOX_TOKEN}&limit=10"
```

### Post a manual outbox send

```bash
curl -sS \
  -H 'Content-Type: application/json' \
  -d '{"title":"smoke-test","message":"{\"type\":\"send\",\"to\":\"447550002572\",\"text\":\"smoke test\"}","priority":5}' \
  "${GOTIFY_BASE_URL}/message?token=${GOTIFY_OUTBOX_APP_TOKEN}"
```

`GOTIFY_OUTBOX_APP_TOKEN` is an operator-side token for manually writing to the outbox app. It is not required by the relay runtime.

## Guardrails

- Keep Gotify and webhook payloads lean.
- Do not dump raw Baileys payloads into Gotify.
- Keep webhook and Gotify contracts aligned.
- Update `.env.example`, `README.md`, and tests together when the contract changes.
