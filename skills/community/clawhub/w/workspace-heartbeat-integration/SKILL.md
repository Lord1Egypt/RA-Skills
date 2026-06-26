# Workspace Heartbeat Integration

## When to Use

Use this skill when you want to:
- Automatically record work成果 during heartbeat checks
- Synchronize workspace HEARTBEAT.md with self-improving heartbeat-state.md
- Reduce manual memory updates by automating the logging process
- Maintain consistent heartbeat state across different memory systems

**Triggers:**
- During routine heartbeat checks (every 30min/1h/2h/daily)
- When manually syncing work logs to MEMORY.md
- When updating TASK_BOARD.md progress
- When you want to automate self-tracking

## Architecture

This skill integrates three systems:
1. **Workspace HEARTBEAT.md** - Task checklist and timing rules
2. **Self-improving heartbeat-state.md** - Per-skill heartbeat tracking
3. **Workspace memory/** - Daily learning logs and MEMORY.md

```
~/.openclaw/workspace/
├── HEARTBEAT.md              # Workspace heartbeat rules
├── MEMORY.md                 # Long-term memory (curated)
├── memory/
│   ├── 2026-03-20.md        # Daily logs (raw)
│   └── heartbeat-state.json # Workspace heartbeat state
└── skills/
    └── workspace-heartbeat-integration/
        ├── SKILL.md
        ├── skill.json
        └── source/
            └── integration.py  # Core logic
```

## Actions

### Sync Heartbeat State

```bash
workspace-heartbeat-integration --sync
```

Performs a full synchronization:
1. Reads current workspace heartbeat-state.json
2. Updates timestamps based on last check times
3. Scans memory/YYYY-MM-DD.md for today's entries
4. Generates a summary of today's work
5. Optionally updates MEMORY.md with new insights

### Auto-log Work Session

```bash
workspace-heartbeat-integration --log "Completed skill X development"
```

Adds a work entry to today's memory file:
- Date and timestamp
- Work category (learning, development, debugging, etc.)
- Detailed description
- Links to related files (if any)

### Generate Heartbeat Report

```bash
workspace-heartbeat-integration --report [--format text|markdown|json]
```

Generates a comprehensive heartbeat report:
- Last check times for all intervals
- Today's work summary
- Pending tasks from TASK_BOARD.md
- Skill development progress
- Suggestions for next actions

## Configuration

The skill reads configuration from:
- `~/.config/workspace-heartbeat-integration/config.json` (optional)

Example config:
```json
{
  "auto_sync": true,
  "log_retention_days": 30,
  "memory_update_threshold": 3,
  "excluded_dirs": [".git", "node_modules", "__pycache__"]
}
```

## Integration with Self-Improving

When installed alongside the `self-improving` skill:
- Heartbeat logs become candidate patterns for self-improvement
- Repeated work patterns can be promoted to HOT memory
- Corrections from manual reviews feed into corrections.md

## Setup

1. Install the skill:
```bash
clawhub install workspace-heartbeat-integration
```

2. (Optional) Configure integration in HEARTBEAT.md:
Add to your heartbeat check routine:
```markdown
### 每 30 分钟检查：
1. 📊 回顾当前进度，更新学习日志
2. 📋 查看任务看板，找下一个任务
3. 💡 同步心跳状态：workspace-heartbeat-integration --sync
```

3. Test the integration:
```bash
workspace-heartbeat-integration --sync
```

## Example Workflow

**Typical heartbeat check (30min interval):**
```
1. 查看是否有紧急消息/邮件
2. 检查任务看板，选择下一个任务
3. 开始执行（例如：开发 skill-validator）
4. 完成后记录：workspace-heartbeat-integration --log "Finished parsing SKILL.md frontmatter"
5. Sync state: workspace-heartbeat-integration --sync
```

**Daily summary (end of day):**
```bash
workspace-heartbeat-integration --report --format markdown > daily_summary.md
```

## Benefits

- **Automation**: No manual copying of timestamps and work entries
- **Consistency**: Uniform format for all daily logs
- **Traceability**: Every heartbeat check is logged with context
- **Self-improvement**: Work patterns become visible for optimization
- **Accountability**: Clear record of what was done each day

## Technical Details

- **Language**: Python 3.8+
- **Dependencies**: None (uses only standard library)
- **Python modules**: json, os, datetime, pathlib, glob, re
- **Thread-safe**: Uses file locks to prevent concurrent modifications
- **Idempotent**: Safe to run multiple times (won't duplicate entries)

## Limitations

- Does not automatically update ClawHub download stats (browser tool required)
- Requires write access to workspace memory/ directory
- Does not parse git history for commit messages (future enhancement)

## Future Enhancements

- Integration with browser tool for ClawHub stats
- Git commit message parsing
- Automatic TASK_BOARD.md progress updates
- Weekly/Monthly trend analysis
- Export to Notion/Google Sheets

---

**Version**: 1.0.0
**Last Updated**: 2026-03-20
**Author**: 小叮当 (智脑)