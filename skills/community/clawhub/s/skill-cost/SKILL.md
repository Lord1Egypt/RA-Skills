---
name: skill-cost
version: 0.1.0
author: dzwalker
description: >
  Track per-skill token usage and costs from OpenClaw session logs. Use when user asks about skill-level spending, which skill costs the most, or wants a per-skill cost breakdown.
  IMPORTANT: This is a bash-tool skill. You MUST use the bash/shell tool to execute commands.
triggers:
  - skill cost
  - skill spending
  - skill usage
  - which skill costs
  - per-skill cost
  - skill token
  - cost by skill
  - token by skill
  - skill breakdown
  - cost breakdown by skill
repository: https://github.com/dzwalker/skill-cost
license: MIT
dependencies: []
tools:
  - skill_cost_report
  - skill_cost_detail
  - skill_cost_compare
metadata: {"clawdbot":{"emoji":"💰","requires":{"anyBins":["python3","bash"]},"os":["linux","darwin","win32"]}}
---

# Skill Cost — USE BASH TOOL

**You MUST use the `bash` or `shell` tool to run these commands. No other method works.**

## Commands

Per-skill cost report:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report
```

Last 7 days:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --days 7
```

Since a specific date:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --since 2026-03-01
```

JSON output:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh report --format json
```

Top skills by cost:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh ranking
```

Detail for a specific skill:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh detail poe-connector
```

Compare two skills:
```bash
bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh compare poe-connector web-search
```

## DO NOT

- Do NOT use `sessions_spawn` — it will fail
- Do NOT use browser — it will fail
- Do NOT use any approach other than `bash` tool — only bash works

## How It Works

1. Scans OpenClaw session JSONL files at `~/.openclaw/agents/*/sessions/`
2. Parses assistant messages for tool calls and token usage
3. Attributes token usage to skills by matching bash command paths and tool names
4. Aggregates and reports per-skill costs with model and daily breakdowns

## Notes

- No API keys required — reads directly from local session files
- No external Python dependencies (stdlib only)
- Skill attribution uses bash command paths and SKILL.md tool mappings
- Tokens for multi-skill messages are proportionally split across skills
- Usage not attributable to any skill is categorized as (built-in) or (conversation)
