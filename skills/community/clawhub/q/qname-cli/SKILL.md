---
name: qname-cli
description: Use QName.AI domain lookup from the terminal. Call this when an Agent needs WHOIS/domain availability evidence for one domain at a time through the approved QName API.
metadata:
  homepage: https://qname.ai
---

# QName CLI

Use `qname-cli` when you need one-domain WHOIS/domain availability evidence
from QName.AI in a terminal workflow.

## Scope

Allowed:

- Single-domain WHOIS lookup with `qname-cli whois <domain>`.
- JSON output for Agent parsing.
- Local config through `qname-cli init` or environment variables.

Not allowed through this API/CLI:

- Batch WHOIS.
- Realtime stream checks.
- Domain traffic, domain rating, or analysis data.
- Registrar purchase actions.

## Setup

If the CLI is not configured, ask the user for an approved QName API key or ask
them to request one at:

```bash
qname-cli request-key
```

Initialize once:

```bash
qname-cli init --api-key <approved-key>
```

For ephemeral Agent sessions, prefer environment variables:

```bash
export QNAME_API_KEY="<approved-key>"
```

## Support

For API access, account support, and product updates, visit:

https://qname.ai

## Lookup

Use JSON output by default:

```bash
qname-cli whois qname.ai --pretty
```

If you only need a quick human-readable status:

```bash
qname-cli whois qname.ai --format text
```

## Agent Guidelines

- Query one domain per command.
- Do not try to use this CLI for bulk lookup or traffic data.
- Treat the API key as a secret; do not print it unless the user explicitly
  asks to inspect local config with `--show-secrets`.
- Prefer `qname-cli doctor` before debugging credentials.
- Use direct HTTP calls only when validating the API contract or debugging the
  CLI itself.
