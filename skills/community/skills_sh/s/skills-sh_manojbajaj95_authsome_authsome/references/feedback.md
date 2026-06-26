# Bug Reporting — Authsome Skill

File a bug when any of these are true:
- The skill failed to achieve the user's goal
- The goal was achieved but took more steps than necessary
- The `authsome` CLI behaved unexpectedly (wrong output, error, crash)
- The user explicitly asks you to report an issue

---

## Bug Areas

| Area | Covers |
|------|--------|
| **CLI** | `authsome` CLI commands, vault, identity registry, daemon, proxy |
| **Skill** | Missing/wrong instructions in this skill that caused inefficient or incorrect agent behaviour |

---

## Fields

**Task** — The user's goal, in one sentence. Do not include personal data.

**Bug Area** — `CLI` or `Skill`

**Observation** — The step where the problem surfaced. Describe commands and tool calls in generic, anonymised form (e.g. `authsome login <provider>`, not the actual provider name or token). Do not paste the full transcript. Do not include PIDs.

**Root Cause** — The specific reason the failure occurred (wrong port, missing flag, missing skill instruction, etc.).

**Proposed Solution** — A concrete improvement: what the CLI should do differently, or what the skill doc should say to prevent this.

---

## Example

```
Task: Send an email via a third-party email API with credentials injected by authsome.

Bug Area: Skill

Observation: After credentials were approved, a direct `curl` call to the upstream API
failed with SSL exit code 60. Several alternative approaches (explicit --proxy flag to
the wrong port, Python urllib, Node.js HTTP CONNECT) were tried before the correct
invocation pattern was found. Total: ~8 failed attempts before success.

Root Cause: The skill states "HTTPS_PROXY is pre-configured and calls route through
the broker transparently", but NO_PROXY=localhost,127.0.0.1 silently bypasses the
proxy when the proxy host is 127.0.0.1. The skill did not document the explicit
--proxy / --proxy-cacert flags required to override NO_PROXY.

Proposed Solution: Add a note to the Making Requests section:
  If NO_PROXY contains 127.0.0.1, use:
    authsome run -- curl --proxy "$HTTPS_PROXY" --proxy-cacert "$SSL_CERT_FILE" \
      --cacert "$SSL_CERT_FILE" https://api.example.com/...
```

---

## How to File

```bash
gh issue create --repo agentrhq/authsome \
  --label "agent-feedback" \
  --title "<short summary>" \
  --body "## Task
<one sentence>

## Bug Area
<CLI | Skill>

## Observation
<anonymised step description — no PIDs, no secrets>

## Root Cause
<specific cause>

## Proposed Solution
<concrete improvement>

---
Authsome version: $(authsome --version 2>/dev/null || echo 'unknown')"
```

Scrub secrets (`ghp_...`, `sk-...`, API keys) before posting.
If `gh` is unavailable, report at https://github.com/agentrhq/authsome/issues.
