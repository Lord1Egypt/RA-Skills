---
name: wolverine
description: Supervised self-healing process manager for OpenClaw. Wraps your gateway in a crash recovery loop — catches errors, diagnoses with AI, proposes fixes for review, verifies them, and restarts. Includes runtime code injection detection (33 patterns), automatic backup/rollback, and semantic memory that learns from past fixes.
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
      anyBins:
        - node
      bins:
        - npm
    primaryEnv: ANTHROPIC_API_KEY
    emoji: "\U0001F43A"
    homepage: https://github.com/bobbyswhip/Wolverine
    install:
      - kind: node
        package: wolverine-ai
        bins:
          - wolverine
          - wolverine-claw
---

# Wolverine — Self-Healing Process Manager

> **EXPERIMENTAL**: This skill wraps your OpenClaw gateway in a supervised repair and security layer. Do not use in workspaces with critical production data until you have tested in a staging environment. All file modifications create backups first and can be rolled back.

## What It Does

Wolverine watches your OpenClaw process. When it crashes, Wolverine:

1. Captures the error (crash or caught 500)
2. Diagnoses it with AI (Anthropic or OpenAI)
3. Proposes a code fix
4. Verifies the fix (syntax check + boot probe)
5. Restarts — with rollback if the fix fails

Most errors are resolved in 3–60 seconds for $0.00–$0.10 in AI tokens. All changes are backed up before being applied.

## Quick Start

```bash
npx wolverine-ai@latest --setup-claw
```

One command. Detects your `.openclaw/config.yml`, merges settings, scaffolds `wolverine-claw/`. Zero code changes needed.

## Healing Pipeline

```
Error detected (crash or 500)
  → Empty stderr? → Just restart ($0.00)
  → Operational fix? → npm install / chmod / kill port ($0.00)
  → AI diagnosis → proposes code fix
  → Verify → syntax check + boot probe
  → Pass? → Apply fix, restart
  → Fail? → Rollback to backup, try next approach
  → 3 failures on same error → stop, file bug report for human review
```

**Safety controls:**
- 5 heals max per 5 minutes (prevents runaway costs)
- 3 failures on same error → stops and notifies human
- 5-minute timeout per heal attempt
- All fixes create a backup before applying
- Protected paths: `src/`, `bin/`, `node_modules/`, `.env` files cannot be modified

## Code Guard — Injection Detection

33 static analysis patterns scan code for injection attacks:

- **eval/Function injection** — `eval(req.body.code)` blocked
- **Command injection** — `execSync(req.query.cmd)` blocked
- **Prototype pollution** — `__proto__[key] = value` blocked
- **Dynamic require** — `require(req.query.module)` blocked
- **SSRF** — `fetch(req.query.url)` blocked
- **Reverse shells** — `spawn("/bin/sh")` blocked
- **Obfuscation** — encoded payloads detected and blocked
- **Execution boundary** — code loaded from outside project root blocked

Blocked files are quarantined with forensic logs (code hash, stack trace, timestamp) for review.

## Backup & Rollback

Every fix creates a backup first. Nothing is lost.

```
wolverine --backup "before risky change"
wolverine --rollback-latest
wolverine --undo-rollback
```

Backups stored in `~/.wolverine-safe-backups/` — outside the project directory, survives `git pull` and reinstalls.

Lifecycle: UNSTABLE → VERIFIED → STABLE (30min of no crashes).

## Brain — Semantic Memory

Vector store that learns from every fix. Before calling AI, Wolverine searches past solutions.

- Repeat errors resolved for $0.00 (cached fix)
- Sub-millisecond search even at 10K+ entries

## Security Stack

| Layer | What It Does |
|-------|-------------|
| Code Guard | 33 injection patterns, quarantine, forensic logging |
| Injection Detector | 50+ prompt injection patterns before AI sees error text |
| Secret Redactor | Scrubs API keys from all AI calls, logs, and memory |
| Sandbox | File access restricted to project directory only |
| Rate Limiter | Prevents runaway AI costs |
| Blocked Commands | 18 dangerous shell patterns rejected |

## Configuration

Edit `wolverine-claw/config/settings.json`:

```json
{
  "gateway": { "port": 18789 },
  "agent": { "model": "claude-sonnet-4-6", "maxTurns": 25 },
  "healing": { "enabled": true, "maxHealsPerWindow": 5 },
  "security": { "sandbox": true }
}
```

Secrets in `.env.local` only:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...     # optional, for embeddings
```

## Commands

```bash
wolverine-claw --setup     # guided onboarding
wolverine --claw            # start with healing
wolverine-claw --direct     # start without healing (debug)
wolverine --backup "msg"    # create snapshot
wolverine --rollback-latest # restore last snapshot
wolverine --update          # safe framework upgrade (never touches your code)
```

## Key Constraints

- All file modifications backed up first — rollback always available
- Healing restricted to `server/` and `wolverine-claw/` directories
- Framework code (`src/`, `bin/`) is read-only
- Max 5 heals per 5 minutes, 3 failures = stop
- Token budgets capped: simple=20K, moderate=50K, complex=100K

## Cost

Most fixes: **$0.00–$0.01**. Complex multi-file: **$0.05–$0.10**. Idle: **$0.00**.

## Links

- [GitHub](https://github.com/bobbyswhip/Wolverine)
- [npm](https://www.npmjs.com/package/wolverine-ai)
- [Website](https://wolverine.dev)
