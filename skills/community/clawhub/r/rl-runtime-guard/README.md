# rl-runtime-guard 🛡️

> **Pre-tool-call runtime guardrails for AI agents.**
> Catches **82.5% of common agent errors** at runtime via soft prompt augmentation — no blocking, no tool output mutation, zero external dependencies.

[![ClawHub](https://img.shields.io/badge/ClawHub-huanmeng9527%2Frl--runtime--guard-blue)](https://clawhub.ai/huanmeng9527/skills/rl-runtime-guard)
[![License: MIT](https://img.shields.io/badge/License-MIT-0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.7-green)]()
[![Node](https://img.shields.io/badge/node-%3E%3D18-green)]()

Adapted from **OpenClaw-RL Phase 2.4** — deployed in production 2026-08-22 with **73% → 50% error rate reduction over 1 week**.

---

## Why runtime guards?

LLM agents fail in **predictable, repeated ways**. A 279-error Phase 2.3 attribution study found:

| Failure category | Share | Agent fault? | Covered by guard? |
|------------------|-------|--------------|-------------------|
| complex_task_fail | 43.4% | Yes | ✅ `complex_task_guard` |
| retry_loop | 26.9% | Yes | ✅ `retry_loop_guard` |
| insufficient_context | 8.4% | No | — |
| tool_arg_complex | 6.8% | Yes | ✅ `tool_guard` |
| debug_session_pollution | 4.8% | No | — |
| ambiguous_brief | 4.8% | No | — |
| path_mismatch | 4.4% | No | ✅ `tool_guard` |
| **Total covered** | **82.5%** | — | — |

Three guards, **zero modifications** to agent behavior — just context-aware reminders injected into the prompt at the right moment.

---

## What this skill does

Three runtime guards inject soft prompt augmentation before each `command:new` event:

| Guard | Catches | Trigger condition |
|-------|---------|-------------------|
| **`complex_task_guard`** | complex_task_fail | User message ≥ 400 chars, or multi-step keywords ("step by step", "and then", "finally") |
| **`retry_loop_guard`** | retry_loop | Last 3 user messages have Jaccard similarity ≥ 0.4 |
| **`tool_guard`** | tool_arg_complex + path_mismatch | Long exec commands or platform-incompatible paths (e.g. Windows path on Linux) |

Each guard is **soft** — it adds system messages, **never blocks requests** and **never modifies tool outputs**. This is the first line of defense, not the enforcement layer.

---

## Install

```bash
# From ClawHub
openclaw skills install rl-runtime-guard

# Or from source
openclaw skills install huanmeng9527/rl-runtime-guard
```

After install, the guard runs automatically on every `command:new` event. **No code changes required.**

---

## Quick start

Once installed, the guard is active. To verify it is running:

```bash
# Check that the hook is registered
openclaw hooks list | grep rl-runtime-guard

# Tail the audit log to see decisions
tail -f ~/.openclaw/logs/audit/rl-guard-decisions.jsonl
```

Each decision emits a JSONL line (only if `auditLogPath` is set):

```json
{
  "timestamp": "2026-08-30T18:30:00Z",
  "sessionKey": "agent-main-abc123",
  "decisions": ["retry_loop"],
  "guardPromptLength": 215,
  "userContentLength": 48
}
```

By default, **no log is written**. To capture decisions for telemetry or debugging, set `auditLogPath` explicitly.

---

## Configuration

Edit `~/.openclaw/hooks/rl-runtime-guard/config.json`:

```json
{
  "complexTaskThreshold": 400,
  "retryLoopThreshold": 0.4,
  "maxExecLength": 2000,
  "auditLogPath": "",
  "enabled": true
}
```

> **Privacy by default**: audit logging is **OFF** in v1.0.5+. Set `auditLogPath` to enable. The log captures only metadata (decisions, prompt length, message length) — never raw user content. See `references/audit-log.md`.

### Threshold tuning

| Parameter | Default | What it controls |
|-----------|---------|------------------|
| `complexTaskThreshold` | 400 | Min chars to consider a task "complex" |
| `retryLoopThreshold` | 0.4 | Min Jaccard similarity to consider a retry loop |
| `maxExecLength` | 2000 | Max exec command length before `tool_guard` warns |
| `enabled` | `true` | Global enable/disable switch |

See `references/thresholds.md` for detailed tuning guidance.

---

## Disable

Three ways, in order of granularity:

```bash
# 1. Per-session (env var, takes effect immediately)
RL_GUARD_DISABLED=1 openclaw ...

# 2. Per-session (config, restart required)
echo '{"enabled": false}' > ~/.openclaw/hooks/rl-runtime-guard/config.json

# 3. Globally
mv ~/.openclaw/hooks/rl-runtime-guard/config.json{,.disabled}
```

See `references/disabling.md` for full details.

---

## Files

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill manifest and instructions for the agent |
| `handler.mjs` | Standalone ESM implementation (zero dependencies, Node ≥ 18) |
| `references/thresholds.md` | Detailed threshold tuning guide |
| `references/disabling.md` | All the ways to turn this off (3 levels) |
| `references/audit-log.md` | Audit log format and example queries |
| `examples/config-minimal.json` | Minimal configuration (defaults) |
| `examples/config-strict.json` | Strict configuration for production |
| `templates/handler.mjs` | Drop-in adapter for OpenClaw hook systems |
| `skill-card.md` | ClawHub-rendered skill card |

---

## Security & limitations

- ✅ **No network access** — purely local computation
- ✅ **No data exfiltration** — only writes to your own audit log
- ✅ **No external dependencies** — pure Node.js stdlib
- ⚠️ **Soft guardrails only** — never blocks requests, never modifies tool output. For enforcement, use OpenClaw ClawGuard's intent-verifier
- ⚠️ **Threshold tuning required** — defaults are calibrated for OpenClaw workstation usage; cloud / sandbox deployments may need different values

---

## Companion skill

For a complete **evaluation + interception** loop, also install [`claw-rl-prm-judge`](https://github.com/huanmeng9527/claw-rl-prm-judge). The PRM judge scores turns off-line so you can measure whether the guards are actually working:

```
guard catches bad pattern at runtime
        ↓
PRM judge scores the turn off-line
        ↓
regression detected? → adjust thresholds
        ↓
loop continues
```

---

## Provenance

Adapted from `OpenClaw-RL` Phase 2.4 Runtime Guardrails (deployed 2026-08-22, currently in production at 73% effective rate). Three runtime guards evolved from a 279-error Phase 2.3 attribution study.

---

## License

MIT-0 (MIT with no attribution required) — see [LICENSE](LICENSE).

---

## Links

- 🛡️ **ClawHub**: https://clawhub.ai/huanmeng9527/skills/rl-runtime-guard
- 🐙 **GitHub**: https://github.com/huanmeng9527/rl-runtime-guard
- 📊 **Companion skill**: https://github.com/huanmeng9527/claw-rl-prm-judge
- 📚 **OpenClaw docs**: https://docs.openclaw.ai
