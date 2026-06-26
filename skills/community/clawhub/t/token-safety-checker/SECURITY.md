# Security Policy

## Purpose

`token-safety-checker` is a **defensive security tool**. It exists to *remove* plaintext secrets from OpenClaw configuration, not to extract or exfiltrate them.

## What this skill does

- **Reads** `openclaw.json` to detect plaintext credential fields (tokens, API keys)
- **Writes** environment variable exports to the user's local shell profile (`~/.zshrc` etc.)
- **Replaces** plaintext values in `openclaw.json` with SecretRef pointers (`{ "source": "env", ... }`)
- The actual secret values are **never logged, printed, or transmitted** — only field paths and lengths are reported

## What this skill does NOT do

- Does not send any data to external servers
- Does not log or store secret values
- Does not make network requests
- All operations are local to the user's machine

## Reporting a vulnerability

If you find a security issue in this skill, please open a GitHub issue or contact the maintainer directly.
