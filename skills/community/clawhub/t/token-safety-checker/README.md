# tightlip 🤐 — secret & token leak guard for agent memory

Find and fix leaked API keys, tokens and passwords in your AI agent's memory, session transcripts and
config — for **Claude Code** and **OpenClaw**. Secret values are never printed: you only see file paths,
line numbers, detector names and `sha256:` fingerprints.

## Install

```
/plugin install tightlip --marketplace maoisdamao/token-safety-checker
```

Requires `python3` (3.10+). Python standard library only, no network calls.

## Use

Ask Claude:

- "Did I leak any API keys into your memory?"
- "Scan my CLAUDE.md and chat history for secrets"
- "Stop secrets from being saved to memory"

What it does:

- **Scans memory** — `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules`, auto memory, prompt history and session
  transcripts (plus OpenClaw memory, transcripts and logs). Read-only.
- **Flags live secrets** — leaked values that match a token in use right now, with rotation steps.
- **Guards new writes** (opt-in, `install-guard --platform claude`) — a `PreToolUse` hook that denies writing a detected secret
  into memory / instruction files. Remove with `uninstall-guard`.
- **Migrates OpenClaw config secrets** to environment variables (`openclaw.json` → SecretRef).

Full workflow: [SKILL.md](SKILL.md). Source, issues and changelog:
https://github.com/maoisdamao/token-safety-checker

## Privacy

Everything runs locally on your machine. Nothing is collected or sent anywhere.

## License

MIT
