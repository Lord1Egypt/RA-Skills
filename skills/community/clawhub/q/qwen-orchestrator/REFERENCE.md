# Qwen Orchestrator Reference

## Purpose
Operational reference for `qwen-orchestrator`.
Use this file when debugging runtime failures, daemon issues, auth problems, or selector drift.

## Architecture
- `ask-qwen.sh` — shell wrapper for normal use
- `ask-puppeteer.js` — main runtime
- `qwen-daemon.js` — persistent browser daemon for fast startup
- `auth-check.js` — Qwen-specific auth detection
- `.qwen.json` — runtime config overrides (including `preferredModel`)

## Expected Files
- `.daemon-ws-endpoint` — daemon websocket endpoint
- `.sessions/*.json` — saved chat/session metadata
- `.logs/qwen.log` — optional runtime log
- `.diagnostics/` — screenshots, traces, summaries on failures

## Daemon Commands
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
bash scripts/setup-daemon.sh
pm2 status qwen-daemon
pm2 restart qwen-daemon
pm2 stop qwen-daemon
```

## Auth Repair
If Qwen opens login/auth screens or dry-run says auth is missing:
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
pm2 stop qwen-daemon
rm -f .daemon-ws-endpoint
bash ask-qwen.sh --visible --wait --dry-run
pm2 start qwen-daemon
bash ask-qwen.sh --dry-run --daemon
```

## Lock Repair
If Chromium profile lock errors appear:
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
rm -f .profile/Singleton*
pm2 restart qwen-daemon
bash ask-qwen.sh --dry-run
```

## Manual Smoke Tests
```bash
# CLI help
bash ask-qwen.sh --help

# Auth + composer only
bash ask-qwen.sh --dry-run

# Daemon path
bash ask-qwen.sh --dry-run --daemon

# Real prompt
bash ask-qwen.sh "Say OK"

# Session path
bash ask-qwen.sh --session test "Say OK"
bash ask-qwen.sh --session test "Repeat OK"
bash ask-qwen.sh --session test --new-chat "Fresh OK"
bash ask-qwen.sh --session test --end-session

# Broader matrix
bash scripts/test-mode-matrix.sh
```

## Known Risks
- Qwen DOM/selectors may drift.
- Daemon mode depends on a valid `.daemon-ws-endpoint`.
- Search toggle may need selector updates if chat.qwen.ai UI changes.
- Model selector may need selector updates if Qwen changes the model-picker UI or renames `Qwen3.6-Max-Preview`.
- Browser auth state is profile-backed; profile corruption can require re-login.
- Local mode and daemon mode currently share one Chromium profile. Do not run local mode while `qwen-daemon` is active; use `--daemon` or stop the daemon first.
- Restored follow-up chats can briefly show a valid URL and composer before prior messages hydrate; this shell-only state is unsafe for follow-up submit and must be waited out or treated as recovery-needed.
- Current runtime hardening for this case: follow-up preflight now requires both the expected chat URL and visible hydrated history before submit, with hard rebind fallback before the prompt is allowed to send. Sidebar title activation is intentionally disabled in the continuity path because duplicate chat titles can misbind to the wrong chat.
- Drift debugging signal: successful follow-up preflight logs a detection path including visible history node count and visible new-chat-root count, so shell-only false positives are easier to spot after Qwen UI changes.
