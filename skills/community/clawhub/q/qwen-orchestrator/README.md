# Qwen Orchestrator

Puppeteer-based access to Qwen Chat (`chat.qwen.ai`) for OpenClaw skills and agents.

## What it does
- Fast daemon mode with a persistent browser
- Session continuity across multiple prompts
- Follow-up preflight waits for hydrated restored chat state, not just URL + composer shell
- Follow-up readiness now requires visible history hydration and will hard-rebind the saved chat before submit if the restored page is still shell-only
- Readiness diagnostics now log the detection path (`historyNodes`, `newChatRoots`, `hasMessageText`, `activeTitle`, `shellOnly`) for UI drift debugging
- Preferred model enforcement before prompt send (`Qwen3.6-Max-Preview` by default)
- Thinking-mode preference before prompt send
- Optional Qwen web search toggle
- Auth checks and practical recovery commands
- Soft client-side `rateLimitMs` between prompt sends

## Quick start
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
bash ask-qwen.sh --dry-run --daemon
bash ask-qwen.sh "What is HTTP?" --daemon
bash ask-qwen.sh --session work "Explain OAuth2" --daemon
```

## Main files
- `SKILL.md` — usage contract and operational instructions
- `REFERENCE.md` — troubleshooting and repair guide
- `ask-qwen.sh` — normal CLI entrypoint
- `ask-puppeteer.js` — runtime implementation
- `qwen-daemon.js` — persistent browser daemon

## Notes
- Prefer `--daemon` for normal use.
- Do not run local mode concurrently with a live daemon against the same Chromium profile.
- Runtime state (`.profile/`, `.sessions/`, `.diagnostics/`, logs) is local-only and not intended for publish.
