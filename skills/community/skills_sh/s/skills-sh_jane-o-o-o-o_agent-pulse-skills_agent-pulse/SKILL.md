---
name: agent-pulse
description: Use Agent Pulse to inspect local AI-agent activity across Hermes, Claude Code, Codex, DeepSeek, OpenClaw, Copilot, Aider, Qwen, OpenCode, Goose, Cursor, Antigravity, and Amp logs. Use when the user asks about AI-agent sessions, tokens, tool/search calls, model usage, estimated cost, budgets, forecasts, health checks, reports, setup diagnosis, web/API/metrics exports, or MCP integration.
---

# Agent Pulse

## Purpose

Use the installed `agent-pulse` CLI as the source of truth for local AI-agent activity. The PyPI package is `agentpulse-cli`, while the command remains `agent-pulse`. Prefer running commands and summarizing their output over reading the Agent Pulse source code.

Always enable UTF-8 on Windows before running commands because Agent Pulse output contains emoji and box drawing:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
```

If `agent-pulse` is not on PATH, ask before installing dependencies. If the user approves, install the PyPI package or try running from a local project checkout:

```powershell
pip install agentpulse-cli
```

```powershell
python -m agent_pulse.cli --version
```

## Source Keys

Use `-P/--platform` when the user asks about one agent tool instead of all local data:

```text
hermes, claude, codex, deepseek, openclaw, copilot, aider, qwen,
opencode, goose, cursor, antigravity, amp
```

## Choose Commands

Use this command selection table first:

| User wants | Run |
|---|---|
| Current status | `agent-pulse status --json` |
| Full dashboard | `agent-pulse --json` or `agent-pulse --no-banner` |
| Demo data | `agent-pulse demo --json` |
| Setup diagnosis | `agent-pulse doctor --json` |
| Recent sessions | `agent-pulse --json --hours 24 --limit 20` |
| Top sessions | `agent-pulse top --sort tokens --json` |
| Top expensive sessions | `agent-pulse top --sort cost --json --hours 168` |
| Model cost analysis | `agent-pulse models --json` |
| Model ranking | `agent-pulse leaderboard --json --rank-by efficiency` |
| Cost savings | `agent-pulse optimize --json` |
| Budget status | `agent-pulse budget --json` |
| Cost forecast | `agent-pulse forecast --json` |
| Cost anomaly check | `agent-pulse anomaly --json` |
| Health/CI check | `agent-pulse health --json` |
| Composite score | `agent-pulse score --json` |
| Search sessions | `agent-pulse search "<query>" --json` |
| Compare periods | `agent-pulse compare --json` |
| Compare projects | `agent-pulse compare-projects --json` |
| Activity calendar | `agent-pulse heatmap --json` |
| Smart recommendations | `agent-pulse insights --json` |
| Prometheus metrics | `agent-pulse metrics --format prometheus` |
| Export report | `agent-pulse export -f markdown` or `agent-pulse export-html` |
| Web dashboard | `agent-pulse web --port 8765` |
| REST API | `agent-pulse api --port 8766` |
| MCP tools | `agent-pulse mcp --list-tools` |

If the installed command lacks an option, run `agent-pulse <command> --help` and adapt.

## Workflow

1. Start with `agent-pulse doctor --json` only when the user asks why data is missing, asks for setup help, or a normal data command returns no sessions.
2. Use JSON output whenever possible. Summarize the fields that matter: sessions, tokens, tools, search calls, model breakdown, source breakdown, estimated cost, warnings.
3. Use time filters for scoped questions. Default to 24 hours for "recent" and 168 hours for "this week":

```powershell
agent-pulse status --json --hours 24
agent-pulse --json --hours 168 --limit 50
```

4. Use platform filters when the user asks about a specific agent system:

```powershell
agent-pulse --json -P codex --hours 24
agent-pulse --json -P claude --hours 24
agent-pulse top --json -P aider --sort cost
agent-pulse status --json -P cursor
```

5. For cost questions, pair summary, model, and top-session views:

```powershell
agent-pulse status --json --hours 24
agent-pulse models --json --hours 24
agent-pulse top --sort cost --json --hours 24
agent-pulse optimize --json --hours 168
```

6. For trend and risk questions, use forecast/history/compare/anomaly:

```powershell
agent-pulse forecast --json
agent-pulse history --json
agent-pulse compare --json
agent-pulse anomaly --json
```

7. For setup, use the discovery commands before guessing paths:

```powershell
agent-pulse doctor --json
agent-pulse scan --json --details
agent-pulse config show
```

## Interpreting Results

- Treat `total_cost_usd` as an estimate based on Agent Pulse's local model pricing table.
- Report both cost and token volume; low-cost models can still have very high token usage.
- Distinguish sources such as `codex`, `claude`, `hermes`, `deepseek`, `openclaw`, `aider`, `cursor`, `opencode`, and `goose`.
- Mention if `doctor` reports missing optional sources, missing `dev_root`, or optional web dependencies.
- If no sessions appear, check `doctor`, then try a wider time window such as `--hours 168`.
- Check whether the user asked for a source (`-P`) filter, a model filter, or a project comparison before giving overall totals.
- If a command emits plain text instead of JSON or fails because an installed version is older, run `agent-pulse <command> --help` and use the closest supported option.

## Reports

For a short human-readable answer, run JSON commands and summarize.

For artifacts, prefer:

```powershell
agent-pulse report --period daily
agent-pulse export -f markdown
agent-pulse export-html
```

Do not invent exact savings or costs. Use the CLI output.

## Integrations

Use the web and API extras only when the user asks for a browser dashboard or programmatic server. Ask before installing missing extras:

```powershell
pip install "agentpulse-cli[web]"
agent-pulse web --port 8765
agent-pulse api --port 8766
```

For monitoring pipelines:

```powershell
agent-pulse metrics --format prometheus
agent-pulse health --cost-limit 100 --token-limit 1000000 --json
```

## MCP

Use MCP mode when the user wants other AI clients to query Agent Pulse:

```powershell
agent-pulse mcp --list-tools
agent-pulse mcp
```

When explaining MCP, mention that it exposes tools such as status, forecast, top sessions, model analytics, optimization, health, search, and leaderboard.

## Local Helper

This skill includes `scripts/run_agent_pulse_snapshot.py`, which runs a compact set of JSON-friendly Agent Pulse checks and prints a combined summary:

```powershell
python scripts/run_agent_pulse_snapshot.py --hours 24 --days 7
```
