---
name: "RedactKit - AI Privacy Scrubber"
description: "Scan your data before sending it to AI. Detect and redact PII, secrets, and sensitive info. Reversible, local, zero network calls."
author: "@TheShadowRose"
version: "1.0.1"
tags: ["privacy", "redaction", "pii", "security", "data-protection", "scrubber"]
license: "MIT"
---

# RedactKit - AI Privacy Scrubber

Use this skill to scan text for sensitive data before sending it to any AI API. Detects and redacts PII, API keys, passwords, phone numbers, emails, and custom patterns. Fully reversible — original values can be restored after the AI responds.

## When to Use This Skill

Invoke this skill when:
- A user wants to send documents to an AI without exposing personal data
- You need to redact API keys, tokens, or credentials from text before logging or sharing
- Preprocessing text for AI analysis that must remain GDPR/HIPAA compliant
- You want to restore redacted values after receiving an AI response

## Quick Start

```python
from redact_kit import RedactionEngine
from redact_restore import RestorationEngine

engine = RedactionEngine(sensitivity_level='medium')

text = "Email john@example.com or call 555-123-4567. API key: sk-abc123xyz"
result = engine.redact(text)

print(result.redacted_text)
# "Email [EMAIL-1] or call [PHONE-1]. API key: [API-KEY-1]"

# Save mapping so you can restore later
engine.save_mapping(result.mapping_id, 'mapping.json')

# Send result.redacted_text to AI safely
# Then restore originals from the AI response
restore_engine = RestorationEngine()
restore_engine.load_mapping('mapping.json')
restored = restore_engine.restore(ai_response, result.mapping_id)
```

## What RedactKit Detects

| Category | Examples |
|----------|---------|
| Email addresses | `user@domain.com` |
| Phone numbers | `555-123-4567`, `+1 (555) 123-4567` |
| API keys & tokens | `sk-...`, `Bearer ...`, `ghp_...` |
| Credit card numbers | `4111 1111 1111 1111` |
| Social Security Numbers | `123-45-6789` |
| IP addresses | `192.168.1.1` |
| Passwords in text | `password: mysecret` |
| Custom patterns | Define your own regex patterns |

## Custom Patterns

```python
from redact_patterns import CustomPatternManager

manager = CustomPatternManager()
manager.add_pattern(
    name="employee_id",
    pattern=r"EMP-\d{6}",
    placeholder="[EMPLOYEE_ID]",
    category="internal",
    sensitivity="high"
)
```

## Restoration

```python
from redact_restore import RestorationEngine

restorer = RestorationEngine()
restorer.load_mapping('mapping.json')  # must load before restoring

# After AI processes the redacted text, restore originals
original_response = restorer.restore(
    redacted_text="Contact [EMAIL-1] for details",
    mapping_id=result.mapping_id
)
# "Contact john@example.com for details"
```

## Sensitivity Levels

Patterns are tagged by sensitivity:
- `critical` — API keys, passwords, SSNs → always redact
- `high` — emails, phone numbers → redact by default
- `medium` — IP addresses, internal IDs → configurable
- `low` — general identifiers → opt-in

Control which levels to redact at engine construction:
```python
# Redact only critical + high patterns (skip medium/low)
engine = RedactionEngine(sensitivity_level='high')
result = engine.redact(text)
```

## Zero Network Calls

All redaction and restoration happens locally. No data leaves your machine. No external dependencies beyond Python standard library.

See README.md for full pattern reference and batch processing documentation.
