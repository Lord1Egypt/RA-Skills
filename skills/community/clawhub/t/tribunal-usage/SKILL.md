---
name: tribunal-usage
description: Use Tribunal commands for TDD enforcement, quality gates, secret scanning, Agent Teams hooks, CI integration, and plugin packs. Use when running quality checks, configuring enforcement modes, checking audit logs, using tribunal ci in pipelines, managing plugin packs, or working with multi-agent Claude Code workflows that need quality gates between agents.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏛",
        "requires": { "bins": ["tribunal"] },
        "install": [],
        "keywords": ["tdd", "quality-gates", "claude-code", "enforcement", "hooks", "ci-cd", "agent-teams", "secret-scanning", "mcp", "spec", "tribunal", "testing", "coverage"],
        "homepage": "https://tribunal.dev",
        "repository": "https://github.com/thebotclub/tribunal"
      }
  }
---

# Tribunal — Usage Guide

Tribunal is a Claude Code quality enforcement plugin. Once installed (`pip install tribunal && tribunal init`), it hooks into every file write, test run, and agent interaction.

## Core Commands

### `tribunal status`
Show current config, hook health, and audit summary.
```bash
tribunal status
tribunal status --json
```

### `tribunal doctor`
Pre-flight health check — all hooks, deps, `.claude/` wiring.
```bash
tribunal doctor        # interactive
tribunal doctor --json # for CI
```
Exit code 1 = something broken. Follow the ✗ suggestions to fix.

### `tribunal ci` — Standalone quality gate
Run all checks without Claude Code. Use in CI pipelines.
```bash
tribunal ci                           # check git-diff'd files
tribunal ci src/payments.py           # specific files
tribunal ci --json                    # machine-readable report
tribunal ci --coverage-threshold 80   # fail if coverage < 80%
```

Exit codes: `0` = all pass · `1` = failures · `2` = warnings only

### `tribunal init` — Project setup
```bash
tribunal init                        # interactive wizard
tribunal init --non-interactive      # CI/agent use, sensible defaults
tribunal init --project-dir /path    # target specific directory
```

## Quality Modes

Control enforcement level per session via `CLAUDE_CODE_MODE` env var:

| Mode | Enforcement | TDD | Coverage |
|------|-------------|-----|----------|
| `code` (default) | Strict — blocks on failure | Block | 80% |
| `code--chill` | Advisory — warns only | Warn | 60% |
| Custom | Configure in `tribunal/modes/<name>.json` | Configurable | Configurable |

Add a `"tribunal"` block to any mode JSON:
```json
{
  "tribunal": {
    "tddEnforcement": "advisory",
    "secretScanning": true,
    "coverageThreshold": 70,
    "blockOnFail": false
  }
}
```

## Hook Events

Tribunal intercepts these Claude Code lifecycle events:

| Event | Hook | What it does |
|-------|------|-------------|
| `PreToolUse` (Write/Edit) | `file_checker` | Secrets, language quality, path traversal |
| `PostToolUse` (Bash) | `tdd_enforcer` | Tests pass/fail, coverage threshold |
| `Stop` | `context_monitor` | Warns when context window filling up |
| `TeammateIdle` | `teammate_idle` | Blocks orchestrator if sub-agent left broken code |
| `TaskCompleted` | `task_completed` | Audits sub-agent session before marking done |
| `SessionEnd` | `session_end` | Writes session summary to audit log |

## Plugin Packs

```bash
tribunal list-packs                    # browse registry
tribunal install python-strict         # 90% coverage, type hints, docstrings
tribunal install go-tdd                # go test -cover, go vet, -race flag
tribunal install nextjs-quality        # TypeScript strict, component tests, a11y
tribunal install https://github.com/org/custom-pack   # direct URL
tribunal install ./local-pack/         # local directory
```

## MCP Integration

Tribunal exposes MCP tools queryable by any Claude Code session:

```
tribunal_status       — current hook config, mode, version
tribunal_audit        — recent audit entries (filterable by outcome/agent)
tribunal_check_file   — run file_checker on any path
tribunal_agent_summary — quality summary for a specific agent_id
```

Use via Claude Code's MCP connector pointing to the Tribunal MCP server.

## Agent Teams Quality Gates

In multi-agent workflows, Tribunal gates quality between agents:

```
Orchestrator → spawns Sub-agent A
Sub-agent A writes files
TeammateIdle fires → tribunal checks A's files
  ✅ pass → orchestrator continues
  ❌ fail → orchestrator blocked until A fixes issues
```

Configure in `tribunal/rules/multi-agent-quality.md` (auto-injected).

## Audit Log

All hook events logged to `.tribunal/audit.jsonl`:
```bash
cat .tribunal/audit.jsonl | jq '.[] | select(.outcome=="blocked")'
```

Fields: `timestamp`, `hook_name`, `file_path`, `outcome`, `duration_ms`, `agent_id`, `detail`

## Context Monitor Thresholds

Configure in `tribunal/settings.json`:
```json
{
  "contextMonitor": {
    "warnThreshold": 80,
    "handoffThreshold": 90
  }
}
```

Set `CLAUDE_CONTEXT_WINDOW=1000000` env var for 1M context window (thresholds auto-scale).

## VS Code Extension

After install, open VS Code in your project. The Tribunal extension:
- Shows `🏛 Passing / 🏛 1 Warning / 🏛 2 Blocked` in status bar
- Adds gutter icons (✅/⚠️/⛔) per file after hooks fire
- Streams hook events to the "Tribunal" output channel
- Reads `.tribunal/audit.jsonl` automatically

## Live Dashboard

```bash
# Open in browser after starting a Claude Code session
open tribunal/ui/viewer.html
```

Shows: live hook feed, context gauge, session stats, filterable audit log.

Full docs: https://tribunal.dev · GitHub: https://github.com/thebotclub/tribunal
