---
name: codex-account-switcher
description: Query OpenAI Codex OAuth account quotas in OpenClaw, switch the preferred account by email/profile id, and optionally auto-switch when 5h quota drops below a threshold. Use for OpenClaw model account management and quota-aware failover.
metadata:
  openclaw:
    emoji: 🔁
    requires:
      bins: [python3, openclaw]
    optionalEnv:
      - OPENCLAW_HOME
      - OPENCLAW_AGENT_ID
      - OPENCLAW_AUTH_STATE
      - OPENCLAW_AUTH_PROFILES
      - OPENCLAW_CODEX_SWITCH_THRESHOLD
      - OPENCLAW_CODEX_SWITCH_SUFFICIENT_THRESHOLD
      - OPENCLAW_CODEX_SWITCH_NOTIFY_GROUP
---

# Codex Account Switcher

Use the bundled scripts to manage `openai-codex` OAuth profiles without exposing tokens.

## Commands

From this skill directory:

```bash
python3 scripts/openclaw-accounts-query.py
python3 scripts/openclaw-account-switch.py user@example.com --dry-run
python3 scripts/openclaw-account-switch.py user@example.com
python3 scripts/codex-cli-sync.py --dry-run
python3 scripts/codex-cli-sync.py
python3 scripts/openai-codex-auto-switch.py --dry-run
python3 scripts/openai-codex-quota-query.py --json
```

## Behavior

- Reads OpenClaw auth profile metadata from the selected agent directory.
- Queries quota directly from ChatGPT WHAM usage using each profile's OAuth access token.
- Never prints access tokens, refresh tokens, API keys, or credential file contents.
- Account switching only rewrites `auth-state.json` provider order for `openai-codex`.
- `codex-cli-sync.py` is advanced/explicit: it imports the current Codex CLI `~/.codex/auth.json` login into OpenClaw and writes backups first.
- Auto-switch defaults to switching only when the active account's 5h remaining quota is below `20%`.

## Useful environment variables

```bash
export OPENCLAW_HOME="$HOME/.openclaw"
export OPENCLAW_AGENT_ID="main"
export OPENCLAW_CODEX_SWITCH_THRESHOLD=20
export OPENCLAW_CODEX_SWITCH_SUFFICIENT_THRESHOLD=20
```

For cron, use an absolute path to `scripts/openai-codex-auto-switch.py` and redirect output to logs.

## Safety

Do not paste script output containing local paths into public places without review. Do not commit `auth-state.json`, `auth-profiles.json`, `.env`, logs, or screenshots containing account emails unless you intend to share them.
