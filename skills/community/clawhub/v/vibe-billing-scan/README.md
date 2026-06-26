# vibe-billing-scan — OpenClaw Skill

> Find which run blew up your API bill. One command. No signup.

## Install

```bash
npx clawhub@latest install vibe-billing-scan
```

## What it does

Scans your OpenClaw API call logs and tells you exactly where your money went:
- Which session cost the most
- Retry storms — 429 errors that triggered expensive retry chains
- Context accumulation — sessions where the context window ballooned
- Looped tool calls — tool calls that repeated on unexpected outputs

## Usage

Just ask your OpenClaw agent: "scan my api spend" or "why is my bill so high"

Or run directly: `npx vibe-billing scan`

## Proof

- $7,691 saved, 947M tokens intercepted, 161 loops blocked

https://api.jockeyvc.com
