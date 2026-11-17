---
name: qname-cli
description: Use QName AI from the terminal for WHOIS, traffic, or Google Ads keyword research through the approved QName AI API, staying within the key's approved API types and quotas.
metadata:
  homepage: https://qname.ai
---

# QName AI CLI

Use `qname-cli` when you need WHOIS/domain availability, traffic evidence, or
Google Ads keyword research from QName AI in a terminal workflow.

## Scope

Allowed:

- WHOIS lookup with `qname-cli whois <domain...>`, capped by the approved
  per-request domain quota and daily request quota for the configured API key.
- Traffic lookup with `qname-cli traffic <domain>`, capped by the approved
  `domain.traffic.lookup` API type and daily request quota.
- Google keyword ideas with `qname-cli keywords "<seed>"` or
  `qname-cli keywords --website <domain>`, capped by the approved
  `keyword.research` API type and daily request quota.
- JSON output for Agent parsing.
- Local config through `qname-cli init` or environment variables.

Not allowed through this API/CLI:

- Realtime stream checks.
- Domain rating or backlink analysis data.
- Registrar purchase actions.

## Setup

If the CLI is not configured, ask the user for an approved QName AI API key or ask
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

Multiple domains are supported when the approved per-request quota allows them:

```bash
qname-cli whois qname.ai example.com --pretty
```

If you only need a quick human-readable status:

```bash
qname-cli whois qname.ai --format text
```

## Traffic

Use JSON output by default:

```bash
qname-cli traffic qname.ai --pretty
```

If you only need a quick human-readable summary:

```bash
qname-cli traffic qname.ai --format text
```

## Google Keyword Research

Query one or more seed phrases. Quote phrases containing spaces:

```bash
qname-cli keywords "ai video generator" "text to video" --pretty
```

Discover keywords from a public website:

```bash
qname-cli keywords --website canva.com --pretty
```

Google Ads target IDs default to the United States (`2840`) and English
(`1000`). Override them when needed:

```bash
qname-cli keywords "ai image generator" \
  --country 2826 --language 1001 --network partners --format text
```

## Agent Guidelines

- Keep each command within the approved per-request domain quota.
- Keep automation loops within the approved daily request quota.
- Use `traffic` only when the configured key is approved for
  `domain.traffic.lookup`.
- Use `keywords` only when the configured key is approved for
  `keyword.research`.
- Do not try to use this CLI for realtime streams, domain rating data, backlink
  analysis data, or purchase actions.
- Treat the API key as a secret; do not print it unless the user explicitly
  asks to inspect local config with `--show-secrets`.
- Prefer `qname-cli doctor` before debugging credentials.
- Use direct HTTP calls only when validating the API contract or debugging the
  CLI itself.
