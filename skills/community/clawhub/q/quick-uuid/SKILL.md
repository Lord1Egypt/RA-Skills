---
name: quick-uuid
description: Generate UUIDs (v4) and short random IDs from the command line. Use when you need a unique identifier for files, records, test fixtures, or correlation IDs and want a zero-dependency one-liner.
---

# quick-uuid

A tiny helper for generating unique identifiers without extra dependencies.

## Generate a UUID v4

```bash
# Linux (kernel-provided)
cat /proc/sys/kernel/random/uuid

# Portable (Python, always available with OpenClaw runtimes)
python3 -c "import uuid; print(uuid.uuid4())"
```

## Generate a short random ID (8 chars, url-safe)

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(6))"
```

## Generate several at once

```bash
python3 -c "import uuid;[print(uuid.uuid4()) for _ in range(5)]"
```

## Notes

- UUID v4 is random; collision probability is negligible for practical use.
- Prefer `secrets` over `random` for anything security-adjacent.
- Short IDs are convenient for logs/correlation but are NOT collision-proof at scale.
