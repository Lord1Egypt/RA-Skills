---
name: testtau
version: 1.0.0
homepage: https://testtau.com/
description: Use TestTau when an AI agent needs disposable email inboxes, private API-key protected test inboxes, webhook capture, request inspection, replay, or JSON Schema assertions for QA, CI, signup, checkout, and integration testing.
---

# TestTau

TestTau gives agents disposable mail and webhook endpoints for tests:

- Public mail: send to `<inbox>@mail.testtau.com`, inspect at `https://mail.testtau.com/i/<inbox>`.
- Public hooks: send to `https://hook.testtau.com/<hookId>`, inspect at `https://hook.testtau.com/_/<hookId>`.
- Private mail and hooks: use the user's TestTau Account page to create an API key, then send reads/config requests with `Authorization: Bearer <key>`.

Use a unique name per task, for example `agent-<purpose>-<short-random>`. Valid names start with a lowercase letter or number and may contain lowercase letters, numbers, `.`, `_`, `+`, or `-`.

## Public Disposable Mail

Use public mail when the inbox can be readable by anyone who knows the name.

1. Choose an inbox name, such as `agent-login-7k3p`.
2. Tell the system under test to email `agent-login-7k3p@mail.testtau.com`.
3. Wait for the message:

```bash
curl -fsS "https://mail.testtau.com/i/agent-login-7k3p/api/wait?timeout=15000&subject=Verify"
```

4. Read parsed JSON:

```bash
curl -fsS "https://mail.testtau.com/i/agent-login-7k3p/api/message/<messageId>/json"
```

Important fields include `fromAddr`, `toAddr`, `subject`, `textBody`, `htmlBody`, `preview`, `attachments`, and `links.raw`.

## Private Mail

Use private mail when the test email must not be visible in a public inbox.

1. Ask the user for their TestTau private inbox name and API key, or direct them to `https://testtau.com/account`.
2. Send mail to `<privateInbox>@mail.testtau.com`.
3. Read with a bearer token:

```bash
curl -fsS \
  -H "Authorization: Bearer $TESTTAU_MAIL_KEY" \
  "https://mail.testtau.com/private/i/<privateInbox>/api/wait?timeout=15000&subject=Verify"
```

Never put private keys in URLs. Use `Authorization: Bearer`.

## Public Webhook Capture

Use public hooks when captured requests can be visible to anyone with the hook id.

```bash
HOOK_ID="agent-webhook-7k3p"
curl -fsS -X POST "https://hook.testtau.com/$HOOK_ID" \
  -H "content-type: application/json" \
  -d '{"event":"agent.test","ok":true}'

curl -fsS "https://hook.testtau.com/_/$HOOK_ID/api/list"
```

Open `https://hook.testtau.com/_/<hookId>` for the live inspector.

## Private Hooks

Use private hooks when inspection, replay, config, wipe, and assertions must require an API key.

```bash
curl -fsS -X POST "https://hook.testtau.com/private/<hookId>" \
  -H "content-type: application/json" \
  -d '{"event":"agent.private"}'

curl -fsS \
  -H "Authorization: Bearer $TESTTAU_HOOK_KEY" \
  "https://hook.testtau.com/private/_/<hookId>/api/list"
```

## Schema Assertions

For webhook contract tests, configure a JSON Schema and use the assert endpoint as a CI gate.

```bash
START="$(date +%s%3N)"

curl -fsS -X PUT "https://hook.testtau.com/_/<hookId>/api/config" \
  -H "content-type: application/json" \
  -d '{"schema":"{\"type\":\"object\",\"required\":[\"event\"]}","schemaFailMode":"capture"}'

# Trigger the system under test here.

curl -fsS "https://hook.testtau.com/_/<hookId>/api/assert?since=$START&min_count=1"
```

For private hooks, add `-H "Authorization: Bearer $TESTTAU_HOOK_KEY"` to config, list, request, replay, wipe, and assert calls.

## Limits And Safety

- Public captures are disposable and should not receive production secrets, PII, or credentials.
- Public mail and hooks are name-based; anyone with the name can inspect them.
- Signed-in private tools require bearer tokens for reads and management.
- Current free private limits: 100 private mail messages per account period and 1,000 private hook captures per account period.
- Mail retention is 48 hours, public inbox storage is 100 messages, mail attachments are capped at 5 MB, and hook request bodies are capped at 1 MiB.

## When Done

Return the exact inbox or hook id used, the inspect URL, and the message/request id if one was captured. If a wait timed out, report that explicitly and include the URL the user can open manually.
