---
name: qwen-orchestrator
description: >
  Qwen Chat (chat.qwen.ai) access via Puppeteer browser automation with CDP interceptor.
  Persistent daemon (~35ms startup), health checks, graceful shutdown, PM2 management.
  Configurable via `.qwen.json`. Use when: (1) need Qwen responses without API key,
  (2) code analysis, review, or generation, (3) text analysis, summarization, translation,
  (4) web search via Qwen's built-in search, (5) "consult Qwen" or ask-qwen.sh.
---

# Qwen Orchestrator v1.5.8

**What this is:** Browser automation that talks to Qwen Chat via Puppeteer.
**Default runtime policy:** before sending a prompt, qwen-orchestrator must switch the Qwen model selector to `Qwen3.6-Max-Preview` and then switch the Qwen mode selector to thinking mode when those selectors are available.
**What this is NOT:** A general AI router or multi-model orchestrator. It's one browser → one LLM.

## Execution

**Working directory rule:** Unless a command here uses an absolute path, run qwen-orchestrator commands from the skill root: `~/.openclaw/workspace/skills/qwen-orchestrator`.
If you are not already there, run:

```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator
```

## Quick Start
```bash
# Simple question
ask-qwen.sh "What is HTTP?"

# Session (keeps context between questions)
ask-qwen.sh "Explain OAuth2" --session work
ask-qwen.sh "What about OpenID Connect?" --session work
ask-qwen.sh --session work --end-session

# With daemon (fast startup ~35ms vs ~15s cold)
ask-qwen.sh "Question" --daemon

# With web search
ask-qwen.sh "Latest news about AI" --search

# Pipe content
cat code.py | ask-qwen.sh "Find bugs"
ask-qwen.sh --stdin < code.py
ask-qwen.sh <<'EOF'
Long multi-line prompt here
EOF
```

## Before you start
- Fastest normal path: prefer `--daemon`
- Safe readiness check: run `ask-qwen.sh --dry-run --daemon`
- Need context across calls: add `--session NAME`
- Need browser automation / scraping / clicking / forms: use `agent-browser`, not qwen-orchestrator

## When to use qwen-orchestrator

| Task | qwen-orchestrator | Direct API | Manual browser |
|------|-------------------|------------|----------------|
| Code analysis / review | ✅ Fast, no API key | Needs API | ❌ Slow |
| Text analysis / summary | ✅ (with --daemon) | Needs API | ❌ Tedious |
| Web search via Qwen | ✅ (with --search) | Needs API | ❌ |
| Brainstorming | ❌ (Dual Thinking) | Needs API | ❌ |
| Web scraping | ❌ Wrong tool | ❌ | ✅ |

**Rule:** Need LLM reasoning without API key → qwen-orchestrator.
Need browser tasks (scrape, click, fill forms) → use `agent-browser` skill instead.

**Session continuity:** in daemon mode, follow-up requests using `--session NAME` must restore the exact saved Qwen `chatUrl` for that session unless `--new-chat` was explicitly requested. Reusing an arbitrary open Qwen tab is incorrect because it breaks multi-round review continuity.

**Follow-up continuity invariant:** after restoring an existing session chat, the next prompt send must remain bound to that same chat unless `--new-chat` was explicitly requested. Before follow-up submit, qwen-orchestrator should prefer the cheapest safe continuity check first: navigate to the saved `chatUrl` only if the current tab is not already bound to that chat, wait for the composer on that exact chat, and require hydrated follow-up chat state rather than a shell-only page before submitting. Hydration readiness now means visible prior history, not just URL + composer presence. If the restored page is still shell-only, qwen-orchestrator must use exact-URL hard rebind rather than sidebar title activation, because duplicate chat titles can bind to the wrong conversation. Submit should stay bound to the composer/send control for that chat, not a page-global Enter fallback unless no safer path exists. If submit still jumps to `/c/new-chat` or a different chat id, treat it as a continuity failure; do not silently accept or persist the new chat as the session state.

## All Flags
| Flag | Purpose |
|------|---------|
| `--session NAME` | Persistent context across requests |
| `--daemon` | Use running Chrome daemon (~35ms startup) |
| `--search` | Enable Qwen web search |
| `--new-chat` | Start new chat within existing session |
| `--end-session` | Close and clean up session |
| `--visible` | Open visible browser (for auth/CAPTCHA fixes) |
| `--wait` | Wait for manual auth completion (with --visible) |
| `--close` | Force close browser after request |
| `--dry-run` | Test auth + composer without sending prompt |
| `--stdin` | Explicitly read prompt body from stdin |
| `--debug` | Verbose debug output |
| `--verbose` | More detailed logs |
| `-h, --help` | Show help |

## Health check
```bash
# 1. Daemon running?
pm2 status | grep -q "qwen-daemon.*online" || echo "Daemon down"

# 2. Dry-run path works?
ask-qwen.sh --dry-run --daemon || echo "Qwen dry-run failed"

# 3. Real response path works?
ask-qwen.sh "OK" --daemon | grep -q "OK" || echo "Qwen not responding"
```

## Failure Recovery (mandatory routing)

### Symptom → exact command
| If you see this symptom | Run this exact command | Then verify with |
|---|---|---|
| `Connection refused`, daemon not online | `pm2 restart qwen-daemon && sleep 8 && ask-qwen.sh --dry-run --daemon` | `ask-qwen.sh "Say OK" --daemon` |
| `auth expired`, `CAPTCHA`, login page | `cd ~/.openclaw/workspace/skills/qwen-orchestrator && pm2 stop qwen-daemon && rm -f .daemon-ws-endpoint && bash ask-qwen.sh --visible --wait --dry-run && pm2 start qwen-daemon` | `bash ask-qwen.sh --dry-run --daemon` |
| response cuts off | `ask-qwen.sh "Part 1" --session temp && ask-qwen.sh "Continue" --session temp` | `ask-qwen.sh --session temp --end-session` |
| `lock`, `Singleton`, profile already in use | `cd ~/.openclaw/workspace/skills/qwen-orchestrator && rm -f .profile/Singleton* && pm2 restart qwen-daemon` | `bash ask-qwen.sh --dry-run` |
| selector not found | `ask-qwen.sh --dry-run --visible` | only after manual inspection consider selector edits |

### Failure Recovery (English quick table)
| Symptom | Exact command | Verify |
|---|---|---|
| daemon offline / connection refused | `pm2 restart qwen-daemon && sleep 8 && ask-qwen.sh --dry-run --daemon` | `ask-qwen.sh "Say OK" --daemon` |
| auth expired / login page / CAPTCHA | `cd ~/.openclaw/workspace/skills/qwen-orchestrator && pm2 stop qwen-daemon && rm -f .daemon-ws-endpoint && bash ask-qwen.sh --visible --wait --dry-run && pm2 start qwen-daemon` | `bash ask-qwen.sh --dry-run --daemon` |
| profile lock / Singleton files | `cd ~/.openclaw/workspace/skills/qwen-orchestrator && rm -f .profile/Singleton* && pm2 restart qwen-daemon` | `bash ask-qwen.sh --dry-run` |
| follow-up continuity looks wrong | `ask-qwen.sh --session NAME "Repeat the last answer in one sentence" --daemon` | confirm the saved session stays on the same chat URL and does not submit from a shell-only restored page |

## Daemon Setup
```bash
cd ~/.openclaw/workspace/skills/qwen-orchestrator && bash scripts/setup-daemon.sh
```

## Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success — response received |
| 1 | Config/arg error or generic runtime failure |
| 2 | Qwen/daemon unavailable |
| 3 | Follow-up continuity failure |

## Minimal Contract & Known Limitations

### What you can rely on
- **Exit codes**:
  - `0` → success, response printed to stdout
  - `1` → fatal config/arg error or generic unrecoverable runtime failure
  - `2` → Qwen/daemon unavailable; restart or repair daemon connectivity before retrying
  - `3` → follow-up continuity failure; the stored chat binding was not preserved safely
- **Session continuity**: with `--session NAME` + `--daemon`, qwen-orchestrator keeps the saved `chatUrl` unless `--new-chat` was explicitly requested.
- **Daemon behavior**: warm daemon calls are the normal fast path; local mode must not race against the same Chromium profile while `qwen-daemon` is active.

### Non-fatal warnings
These warnings may still return exit code `0` if a response was produced:
- thinking-mode selector could not be opened or confirmed
- web-search toggle could not be confirmed even though the request continued

If the task depends on deep reasoning or web search specifically, treat these warnings as a signal to retry with `--visible` or manually verify mode state.

### Known limitations
- **Selector drift**: Qwen UI changes can break the thinking/search selectors before the rest of the flow fails.
- **Long answers**: use `--session` and continuation prompts for large outputs.
- **Oversized prompts**: Qwen web UI can silently refuse an oversized single-shot submit before any API request is emitted. qwen-orchestrator now validates whether submit really left the page, retries with adaptive shortening when needed, and fails explicitly with `QWEN_SUBMIT_BLOCKED_OVERSIZE_PROMPT` if delivery never succeeds.
- **Continuity failures**: if exit code `3` occurs, end the affected session and start it fresh instead of silently trusting the new chat.
- **Hydration lag**: restored follow-up chats may briefly present the composer before prior messages hydrate; qwen-orchestrator now waits for hydrated chat state before follow-up submit, but severe upstream UI changes can still require visible inspection.

### Recovery shortcuts
```bash
# Exit 2: Qwen/daemon unavailable
pm2 restart qwen-daemon && sleep 8
bash ask-qwen.sh --dry-run --daemon

# Exit 3: continuity failure
bash ask-qwen.sh --session NAME --end-session
bash ask-qwen.sh "your prompt" --session NAME --daemon
```

### Session file trust boundary
Session state in `.sessions/<name>.json` is trusted internal state.
- Do **not** manually edit or swap session files.
- Continuity guarantees apply only while session files are managed exclusively by `ask-qwen.sh`.
- If a session file looks stale or suspicious, end that session and start a fresh one instead of trying to repair the JSON by hand.

## Configuration (.qwen.json)
```json
{
  "browserLaunchTimeout": 30000,
  "answerTimeout": 600000,
  "composerTimeout": 10000,
  "navigationTimeout": 30000,
  "idleTimeout": 15000,
  "heartbeatInterval": 15000,
  "domErrorIdleMs": 25000,
  "rateLimitMs": 5000,
  "maxContinueRounds": 30,
  "preferredModel": "Qwen3.6-Max-Preview",
  "logToFile": true,
  "logPath": ".logs/qwen.log"
}
```

- `rateLimitMs`: client-side delay between prompt sends. Helps avoid accidental rapid-fire requests against Qwen. Set to `0` to disable.
- `preferredModel`: model name that qwen-orchestrator should force before each prompt. Default: `Qwen3.6-Max-Preview`.

## Minimal Decision Rules

- If you need the fastest normal run → `--daemon`
- If you need context across prompts → `--session NAME`
- If you need a fresh Qwen thread inside an existing session namespace → `--new-chat`
- If you need to close stored context → `--end-session`
- Before sending a prompt → force the Qwen model selector to `Qwen3.6-Max-Preview` (or `.qwen.json.preferredModel`) if the selector exists; warn if it cannot be confirmed
- Before sending a prompt → force the Qwen mode selector to thinking mode if the selector exists; warn if it cannot be confirmed
- If you enable search → verify the Web Search toggle really became active; warn if it cannot be confirmed
- Auth repair → stop daemon → `--visible --wait --dry-run`
- Health check → `--dry-run`
- Long answers → `--session` + chunk
- If `qwen-daemon` is running, prefer `--daemon`; local mode currently must not run concurrently against the same Chromium profile
- Browser automation / scraping / form filling → use `agent-browser`, not qwen-orchestrator
- If a follow-up session behaves oddly, prefer reusing the same `--session NAME`; do not silently switch to a different open Qwen tab
- Warning-only mode/search selector issues may still return success if the response was produced; treat the warning text as diagnostic signal, not as a guaranteed hard failure
- Need deeper runtime details or repair commands → read `REFERENCE.md`. Purpose: debug failures.
