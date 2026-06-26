---
name: skill-stats
description: Query, analyze, and track all skill usage information. This skill should be invoked when users ask about skill usage, call counts, success rates, last used time, redundant installations, duplicates, available skills, or any questions related to skill usage details. Supports independent statistics for both Claude Code and OpenClaw environments.
---

# Skill Stats - Skill Usage Statistics

Analyze and track skill usage across Claude Code and OpenClaw environments.

## Features

### Claude Code
- Scans all session files under `~/.claude/projects/`
- Categorizes by scope (builtin/plugin/user/project)
- Shows usage frequency, success rate, and last used time
- Identifies unused and deleted skills

### OpenClaw
- Scans all session files under `~/.openclaw/agents/main/sessions/`
- Categorizes by scope (openclaw-workspace/openclaw-global)
- Parses toolCall-type skill invocation records
- Stores statistics independently

## Usage

Execute the statistics script with the required `--context` parameter:

**Claude Code Environment:**
```bash
npx -y tsx ${SKILL_DIR}/scripts/main.ts --context claude-code
```

**OpenClaw Environment:**
```bash
npx -y tsx ${SKILL_DIR}/scripts/main.ts --context openclaw
```

## Output Examples

### Claude Code
```
====================================================================================================
Skill Usage Statistics
====================================================================================================
Last Updated: 2026-03-05T09:26:33.759Z

【BUILTIN - Built-in】
----------------------------------------------------------------------------------------------------
  Skill Name                         Calls       Success Rate  Last Used                 Time Ago         Status
  -----------------------------------------------------------------------------------------------
  keybindings-help                   1         100.0%    2026/02/09 19:52      23 days ago      Active

【USER - User】
----------------------------------------------------------------------------------------------------
  skill-stats                        24        100.0%    2026/03/03 22:11      1 day ago        Active
  nano-banana                        10        100.0%    2026/02/24 16:58      9 days ago       Active
```

### OpenClaw
```
====================================================================================================
Skill Usage Statistics
====================================================================================================
Last Updated: 2026-03-05T09:26:06.765Z

【OPENCLAW-GLOBAL - OpenClaw Global】
----------------------------------------------------------------------------------------------------
  Skill Name                         Calls       Success Rate  Last Used                 Time Ago         Status
  -----------------------------------------------------------------------------------------------
  enterprise-doc                     1         100.0%    2026/03/04 14:45      1 day ago        Active
  file-upload                        1         100.0%    2026/03/05 14:46      Today            Active
```

## How It Works

### Claude Code
1. Scans all session files (.jsonl) under `~/.claude/projects/`
2. Extracts `Skill` tool invocation records
3. Calculates call counts, success rates, and project usage for each skill
4. Displays results categorized by scope

### OpenClaw
1. Scans session files (.jsonl) under `~/.openclaw/agents/main/sessions/`
2. Parses toolCall-type skill invocations (via `read` tool reading SKILL.md)
3. Identifies workspace-level and global-level skills
4. Stores statistics independently

## Data Storage

- **Claude Code**: `~/.claude/skill-stats/global-stats.json`
- **OpenClaw**: `~/.openclaw/skill-stats/openclaw-global-stats.json`
