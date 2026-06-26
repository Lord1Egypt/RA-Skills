# Error Recovery 🩹

> AI agents fail silently. This skill makes sure they fail loudly, recover smartly, and learn from every mistake.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-green.svg)]()
[![Skill](https://img.shields.io/badge/type-agent--skill-blue.svg)]()

## The Problem

AI agents are notoriously bad at handling errors:

| Anti-pattern | What happens | Consequence |
|-------------|-------------|-------------|
| 🤫 **Silent failure** | Error occurs, agent says "Done!" | Broken state, user doesn't know |
| 🔄 **Blind retry** | Same call, same params, same error | Wasted tokens, rate limits hit |
| 🔥 **Error escalation** | Wrong fix makes it worse | Data loss, cascading failures |
| 📉 **Fake success** | "Should work" without verification | Delivery of broken results |

**Sound familiar?** You ask an AI agent to fix a file, it says "Done!" — but nothing changed.

## The Solution: 4R Framework

```
R1: RECOGNIZE  → Did something go wrong? (Stop ignoring errors)
R2: RESCUE     → Can I fix it? (Smart recovery, max 3 attempts)
R3: REPORT     → Does the human need to know? (Structured error reports)
R4: REMEMBER   → What did I learn? (Error journal, pattern detection)
```

### Before vs After

**Without Error Recovery:**
```
User: "Push to GitHub"
Agent: ✅ Pushed successfully!
Reality: fatal: could not read Username, nothing was pushed
```

**With Error Recovery:**
```
User: "Push to GitHub"

⚠️ Error: Git push failed after 2 recovery attempts

What happened: Pushing to origin/main
Error: fatal: could not read Username for 'https://github.com'
Attempted: 
  1. Retried push → same auth error
  2. Tried SSH → not configured
State: Commit saved locally, not on remote
Need: Git credentials or token auth setup
```

## Quick Start

### As Agent Skill
```bash
# Claude Code
cp SKILL.md .claude/skills/error-recovery/

# OpenClaw
cp SKILL.md ~/.openclaw/workspace/skills/error-recovery/

# Cursor
cp SKILL.md .cursor/rules/error-recovery.mdc
```

### As CLI Tool (included)
```bash
# Diagnose any error instantly
node scripts/error-diagnose.mjs --error "ENOENT"
node scripts/error-diagnose.mjs --error "429" --context "GitHub API"
node scripts/error-diagnose.mjs --error "timeout" --context "npm install"
```

Supports: ENOENT, EACCES, EISDIR, 401, 403, 404, 429, 500, timeout, SIGKILL, SIGTERM, and any custom error.

## Key Features

### 🔍 Smart Error Recognition
Never silently continue after a failure. The skill checks:
- Command exit codes
- Exception messages
- Empty or unexpected output
- Timeout detection
- Behavioral anomalies

### 🛠️ Intelligent Recovery
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Attempt 1  │────▶│  Attempt 2  │────▶│  Attempt 3  │
│  Immediate  │     │  Wait 5s    │     │  Wait 15s   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                    All failed? → 📢 REPORT     │
```

**What gets retrried:** Network timeouts, rate limits, transient API errors
**What gets reported immediately:** Auth failures, permission errors, data corruption

### 📋 Structured Error Reports
Every error gets reported with:
1. What happened (context)
2. The full error (details)
3. What was tried (recovery log)
4. Current state (what works, what's broken)
5. What's needed (human action required?)

### 🧠 Error Memory
Errors are logged to `memory/errors/` with:
- Root cause analysis
- Fix documentation
- Prevention measures
- Pattern detection across sessions

## Recovery Strategy Map

| Error Type | Strategy | Max Retries |
|-----------|----------|-------------|
| Network timeout | Exponential backoff | 3 |
| Rate limit (429) | Wait + respect Retry-After | 3 |
| File not found (ENOENT) | Create / suggest correct path | 1 |
| Permission denied (EACCES) | Suggest fix | 0 (report) |
| Auth failure (401) | Re-auth | 1 |
| Server error (500) | Retry after delay | 3 |
| Process killed (SIGKILL) | Reduce load, retry | 2 |
| Data validation | Request correct input | 0 (report) |

## Works With

- [OpenClaw](https://openclaw.ai)
- Claude Code
- Cursor
- Windsurf
- Codex
- Any agent framework

## Related Skills

| Skill | Purpose |
|-------|---------|
| [Cognitive Debt Guard](https://github.com/aptratcn/cognitive-debt-guard) | Prevent AI code quality issues |
| [Prompt Guard](https://github.com/aptratcn/prompt-guard) | Block prompt injection attacks |
| [EVR Framework](https://github.com/aptratcn/evr-framework) | Verify completions are real |
| [Systematic Debugging](https://github.com/aptratcn/systematic-debugging) | Root cause analysis |

## License

MIT — Use freely, fail safely.
