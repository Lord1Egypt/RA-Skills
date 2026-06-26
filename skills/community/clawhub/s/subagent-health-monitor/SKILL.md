---
name: Subagent Health Monitor
description: MCP server that tracks Claude Code subagent performance in real-time. Detects silent failures, token waste from idle loops, and duplicate task spawns. Get fleet-wide health scores and actionable alerts.
version: 1.0.0
author: abhinas90
tags: [mcp, claude-code, subagent, monitoring, token-optimization]
price: 29
category: developer-tools
---

# Subagent Health Monitor

Your subagents are dying silently and you don't know until the bill arrives. This MCP server catches it in real-time.

Built from production data: agent teams burn 13-22% of tokens on idle loops and duplicate spawns. This tool surfaces exactly where.

## What it tracks

- Silent failures: subagent with zero progress for >2 minutes → alert
- Token waste: estimates waste from idle notification loops
- Duplicate detection: same task spawning multiple times → alert  
- Fleet health score: 0-100 based on stuck agents + token waste

## Tools exposed to Claude

| Tool | What it does |
|------|-------------|
| `register_subagent` | Register a subagent for tracking |
| `check_agent_health` | Check a specific subagent's health |
| `record_agent_progress` | Log progress after each tool call |
| `get_fleet_health` | Fleet-wide health summary |

## Quick start

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "subagent-health": {
      "command": "python3",
      "args": ["path/to/subagent-health.py", "--mcp"]
    }
  }
}
```

Then in Claude Code: "Check fleet health" or "Is subagent-3 stuck?"

## Example output

```
Fleet Health Report
├── Total agents: 4
├── Active: 3
├── Stuck: 1 (agent-2: no progress for 340s)
├── Total tokens: 142,000
├── Estimated waste: 25,560 tokens (18%)
└── Health score: 68/100

ALERT: agent-2 is stuck. Kill and restart with trimmed context.
```

## Prerequisites

- Python 3.8+
- Claude Code with MCP support
- No API keys required — state stored locally in `~/.claude/`