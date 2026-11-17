---
name: sluice
description: An outbound egress guard for agents — scan any message (email, social draft, Telegram reply, a write to a public site) for leaked secrets and private identifiers before it goes out, and either refuse it or redact them in place. Pure standard library, precision-tuned to not cry wolf.
version: 0.1.0
homepage: https://workloft.ai/labs
metadata:
  openclaw:
    emoji: "🚰"
    requires:
      bins:
        - python3
---

# sluice

Agents touch live credentials all day: API keys in `.env`, bot tokens in systemd
units, JWTs from Supabase. One careless paste into outbound copy and a key is on
the public internet forever. `sluice` is the gate between the machine's insides
and the outside world: every outbound message passes through it first. Pure
Python standard library — no network, no model call, no dependencies.

The executable is `{baseDir}/bin/sluice`.

## When to use this

Put `sluice` in front of anything an agent sends or publishes — an email, a
social post, a Telegram reply, a commit to a public site. Use `scan` as a
pre-send gate (blocks on a breach) or `redact` to scrub in a pipe.

## How to use it

```
# gate a draft — only proceeds if clean (scan exits non-zero on a breach)
{baseDir}/bin/sluice scan draft.md && ./send-it draft.md

# scrub a file and keep going
{baseDir}/bin/sluice redact draft.md > safe.md

# sits in a pipe
generate-post | {baseDir}/bin/sluice redact | queue-to-typefully

# machine-readable, control the block threshold
{baseDir}/bin/sluice scan --json --fail-on high draft.md
```

`scan` prints findings to **stderr** and exits non-zero at or above `--fail-on`
(default `high`). `redact` writes cleaned text to **stdout**. Previews never echo
the full secret — `glpa…z9 (26 chars)`, never the value.

## What it catches

- **High** (live credentials, block by default): Anthropic / OpenAI / OpenRouter
  keys, GitLab & GitHub PATs, AWS access keys, Slack tokens, Stripe live keys,
  Telegram bot tokens, JWTs / Supabase keys, PEM private-key blocks.
- **Medium:** `key = <high-entropy value>` assignments (entropy-gated so prose
  doesn't trip it), private infrastructure paths.
- **Low:** RFC1918 private IPs (topology leak).

## Notes for the agent

- Reference the tool as `{baseDir}/bin/sluice` — never hardcode a path.
- High-severity detectors are tuned for precision (a guard that cries wolf gets
  switched off); the generic `key=value` rule carries a Shannon-entropy gate.
- Extend by adding a `Detector` to `sluice/detectors.py`.
- Built by Workloft (https://workloft.ai/labs).
