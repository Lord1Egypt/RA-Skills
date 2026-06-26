---
name: telegram-miniapp-security-auditor
description: Audit Telegram Mini App projects for launch safety before connecting bot tokens or public channels. Use when Codex needs to review a Telegram WebApp/Mini App, TMA frontend, FastAPI/Node backend, BotFather launch runbook, Colab/ngrok deployment, or OpenClaw/Codex skill that handles Telegram initData, bot tokens, admin endpoints, CORS, PII, request forms, or public channel launch readiness.
version: 1.0.3
homepage: https://github.com/zack-dev-cm/telegram-miniapp-security-auditor
license: MIT-0
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/telegram-miniapp-security-auditor","skillKey":"telegram-miniapp-security-auditor","requires":{"anyBins":["python3","python"]}}}
---

# Telegram Mini App Security Auditor

Audit Telegram Mini Apps with a static, evidence-first workflow. Prefer the bundled script for repeatability, then inspect the flagged files before giving launch advice.

## Quick Start

Run the static auditor from the skill folder:

```bash
python3 {baseDir}/scripts/audit_tma.py \
  /path/to/project \
  --out-dir /tmp/tma-audit
```

Expected outputs:
- `tma_security_audit.json`
- `tma_security_audit.md`

Decision meanings:
- `PASS`: no blocking or review-triggering evidence found by this static pass.
- `REVIEW`: launch only after a human verifies the listed risks.
- `BLOCK`: do not launch or connect production bot tokens until fixed.

## Workflow

1. Run `scripts/audit_tma.py` against the project root or Mini App subdirectory.
2. Read the Markdown report and inspect every `BLOCK` and `REVIEW` file reference.
3. If the app is not detected as a Telegram Mini App, confirm whether the user passed the correct path.
4. For production launch, require all of these:
   - server-side Telegram `initData` validation,
   - no committed bot tokens or token-like literals,
   - admin endpoints protected by server-side authorization,
   - no broad CORS in production,
   - request forms reject or avoid contact details, handles, secrets, and payment terms when governance requires it,
   - local/browser QA evidence before BotFather or channel changes.
5. If packaging as a ClawHub/Codex skill, run TrustClaw after this audit:

```bash
trustclaw scan /path/to/skill --format markdown
```

## Finding Triage

Treat script output as static evidence, not a final safety determination.

- `hardcoded-telegram-token`: always `BLOCK`; rotate the token if it was committed.
- `initdata-no-server-validation`: `BLOCK`; Mini App users must not be trusted from client-side data alone.
- `insecure-initdata-bypass`: usually `REVIEW`; acceptable only for clearly documented local dev commands and disabled-by-default server behavior.
- `cors-wildcard`: `REVIEW`, or `BLOCK` if credentials are also enabled.
- `admin-endpoint-without-guard`: `BLOCK`.
- `unsafe-innerhtml`: `REVIEW`; verify escaping or sanitization.

For detailed rules and manual checks, read `references/tma-security-checklist.md` only when needed.

## Output Contract

When answering a user, lead with:

1. decision,
2. highest-severity findings with file paths,
3. launch recommendation,
4. artifacts produced,
5. any limitations of the audit.

Keep live Telegram/BotFather/channel changes out of scope unless the user explicitly asks to launch and the project has passed audit and QA.
