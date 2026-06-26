# 🛡️ SentiClaw

**6-Layer Runtime AI Security for OpenClaw Agents**

Protect your OpenClaw agent from prompt injection, identity spoofing, PII leakage, and runtime abuse — with zero configuration required to get started.

Built by [PHRAIMWORK LLC](https://phraimwork.com)

---

## Install

```bash
npx clawhub@latest install senticlaw
pip install ./skills/senticlaw
```

---

## Quick Start

```python
from senticlaw import SentiClaw

sc = SentiClaw(config={
    "owner_ids":        {"discord": ["YOUR_DISCORD_USER_ID"]},
    "trusted_senders":  {"discord": ["YOUR_DISCORD_USER_ID"]},
    "alert_channel_id": "YOUR_SECURITY_CHANNEL_ID",
})

# Check every inbound message
result = sc.check_inbound(text, sender_id=sender_id,
                          channel="discord", session_id=session_id)
if not result.allowed:
    return result.block_message   # blocked — send this back

# Pass result.text (sanitized) to your agent
response = agent.respond(result.text)

# Check every outbound response
safe = sc.check_outbound(response, session_id=session_id)
return safe.response              # guaranteed clean
```

---

## The 6 Layers

| # | Layer | Blocks |
|---|-------|--------|
| 0 | **Identity** | Spoofing, unauthorized access, name-claim attacks |
| 1 | **Sanitizer** | Prompt injection, jailbreaks, zero-width char attacks |
| 2 | **Outbound Gate** | API key leaks, file path exposure, system prompt leakage |
| 3 | **Redactor** | PII in responses (email, phone, SSN, credit cards) |
| 4 | **Governance** | Rate limiting, spend caps, loop detection |
| 5 | **Access Control** | Unsafe file paths, private URL access, tool abuse |

---

## Configuration

```python
from senticlaw import SentiClaw, SentiClawConfig

sc = SentiClaw(config=SentiClawConfig(
    # Identity
    owner_ids={"discord": ["YOUR_ID"]},
    trusted_senders={"discord": ["YOUR_ID"]},
    block_unknown_senders=False,      # True = strict mode

    # Redaction
    redact_pii=True,
    redact_secrets=True,
    redaction_mode="mask",            # mask | remove | tokenize

    # Governance
    spend_cap_daily_usd=10.0,
    max_messages_per_hour=100,
    max_messages_per_minute=20,
    loop_threshold=3,

    # Outbound
    outbound_block_api_keys=True,
    outbound_block_file_paths=True,

    # Alerts — discord | telegram | slack | whatsapp
    alert_channel="discord",
    alert_channel_id="YOUR_CHANNEL_ID",

    # Audit
    audit_db_path="senticlaw_audit.db",
))
```

---

## Instant Threat Alerts

When a threat is detected, SentiClaw fires an immediate alert to your preferred channel:

```
🚨 SentiClaw Alert [09:34:17]
INJECTION ATTEMPT
Channel: DISCORD | Session: discord_999 | Sender: 999999
```

Supports any channel OpenClaw has configured:

```python
# Discord
sc = SentiClaw(config={
    "alert_channel":    "discord",
    "alert_channel_id": "YOUR_CHANNEL_ID",
})

# Telegram
sc = SentiClaw(config={
    "alert_channel":    "telegram",
    "alert_channel_id": "YOUR_CHAT_ID",
})

# Slack
sc = SentiClaw(config={
    "alert_channel":    "slack",
    "alert_channel_id": "YOUR_CHANNEL_ID",
})

# WhatsApp
sc = SentiClaw(config={
    "alert_channel":    "whatsapp",
    "alert_channel_id": "+12035551234",
})
```

---

## Audit Log

All events are logged to SQLite. Query anytime:

```python
# Recent threats
threats = sc.recent_threats(hours=24)

# Full stats
stats = sc.stats()
# {'allowed': 142, 'injection_attempt': 3, 'spoofing_attempt': 1, ...}
```

---

## Running Tests

```bash
python tests/run_tests.py
```

Expected output: all ✅ passing.

---

## License

MIT © 2026 [PHRAIMWORK LLC](https://phraimwork.com)
