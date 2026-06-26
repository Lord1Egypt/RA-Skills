---
name: senticlaw
description: >
  Runtime AI security for OpenClaw agents. Protects against prompt injection,
  identity spoofing, PII leakage, and runtime abuse. Drop-in 6-layer security
  middleware with SQLite audit logging, outbound content gating, and instant
  threat alerts. Use when: hardening your OpenClaw agent against external input
  attacks, protecting sensitive data in responses, or monitoring agent activity.
  NOT for: network/firewall security (this is AI-layer only).
metadata:
  openclaw:
    emoji: "🛡️"
    version: "1.0.0"
    author: "PHRAIMWORK LLC"
    url: "https://phraimwork.com"
    requires:
      python: ">=3.10"
---

# SentiClaw — Runtime AI Security for OpenClaw

SentiClaw is a 6-layer security middleware that protects your OpenClaw agent
from prompt injection, identity spoofing, data exfiltration, and runtime abuse.

## Install

```bash
npx clawhub@latest install senticlaw
pip install ./skills/senticlaw
```

## Quick Start

Add to your OpenClaw workspace (`HEARTBEAT.md` or any tool):

```python
from senticlaw import SentiClaw

sc = SentiClaw(config={
    "owner_ids": {"discord": ["YOUR_DISCORD_USER_ID"]},
    "trusted_senders": {"discord": ["YOUR_DISCORD_USER_ID"]},
})

# Check inbound message
result = sc.check_inbound(text, sender_id=sender_id, channel="discord", session_id=session_id)
if not result.allowed:
    return result.block_message

# Run your agent logic here...
response = agent.respond(result.text)

# Check outbound response
safe = sc.check_outbound(response, session_id=session_id)
return safe.response
```

## The 6 Layers

| # | Layer | Protects Against |
|---|-------|-----------------|
| 0 | **Identity** | Spoofing, unauthorized access, name-claim attacks |
| 1 | **Sanitizer** | Prompt injection, jailbreaks, zero-width char attacks |
| 2 | **Outbound Gate** | API key leaks, internal IP exposure, system prompt leakage |
| 3 | **Redactor** | PII in responses (email, phone, SSN, credit cards) |
| 4 | **Governance** | Rate limiting, loop detection, spend caps |
| 5 | **Access Control** | Unsafe file paths, private URL access, tool abuse |

## Audit Log

All events are logged to SQLite (`senticlaw_audit.db`):
- `ALLOWED` — clean message passed through
- `BLOCKED` — message blocked by policy
- `INJECTION_ATTEMPT` — prompt injection detected
- `SPOOFING_ATTEMPT` — identity spoofing detected
- `OUTBOUND_BLOCKED` — sensitive data in response blocked
- `RATE_LIMITED` — sender exceeded volume limits
- `LOOP_DETECTED` — repeated identical messages

## Alert Integration

Wire up instant alerts to any channel OpenClaw supports:

```python
sc = SentiClaw(config={
    "owner_ids": {"discord": ["YOUR_ID"]},
    "alert_channel":    "discord",    # discord | telegram | slack | whatsapp
    "alert_channel_id": "YOUR_CHANNEL_OR_CHAT_ID",
})
```

Any injection or spoofing attempt fires an immediate alert to your channel.

## Configuration

```python
from senticlaw import SentiClaw, SentiClawConfig

config = SentiClawConfig(
    owner_ids={"discord": ["YOUR_ID"]},
    trusted_senders={"discord": ["YOUR_ID"]},
    block_unknown_senders=False,
    redact_pii=True,
    redact_secrets=True,
    redaction_mode="mask",          # mask | remove | tokenize
    spend_cap_daily_usd=10.0,
    max_messages_per_hour=100,
    loop_threshold=3,
    outbound_block_api_keys=True,
    outbound_block_file_paths=True,
    alert_channel_id="",            # Discord channel ID for alerts
    audit_db_path="senticlaw_audit.db",
)
```

## Running Tests

```bash
cd skills/senticlaw
python tests/run_tests.py
```

---

Built by [PHRAIMWORK LLC](https://phraimwork.com) · MIT License
