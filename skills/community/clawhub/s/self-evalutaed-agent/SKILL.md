# Self-Improving Agent

## Description

Self-improving agent system that learns from its own errors. Automatically detects issues, researches solutions, and implements improvements.

**Based on production-ready patterns:** Reflection, PEV (Plan-Execute-Verify), and Meta-Controller architectures.

## Features

- **Auto-Trigger**: Automatically runs when new errors are detected
- **Topic Selection**: Analyzes error patterns and selects high-priority topics
- **Impact Measurement**: Records before/after metrics to measure improvement effectiveness
- **Procedural Memory**: Remembers working commands/scripts between sessions

## What It Does

1. **Error Detection**: Monitors cron jobs, circuit breakers, and error logs
2. **Topic Selection**: Chooses research topics based on error impact
3. **Research**: Generates research files with improvement recommendations
4. **Backlog**: Creates high-impact tasks in backlog
5. **Execution**: Backlog Agent PM executes tasks sorted by impact
6. **Measurement**: Records before/after to measure effectiveness
7. **Learning**: Remembers what worked for future reference

## Architecture

```
Errors → Auto-Trigger → Topic Selector → Research → Backlog → Agent PM
                                              ↓                    ↓
                                      Impact Measurement ← Procedural Memory
```

## Usage

### Run Full Cycle
```bash
python3 skills/self-improving-agent/scripts/self_improvement_cycle.py
```

### Check Errors Only
```bash
python3 skills/self-improving-agent/scripts/topic_selector.py
```

### Record Impact
```bash
python3 skills/self-improving-agent/scripts/impact_measurement.py \
  --record \
  --task "Fix cron timeout" \
  --before '{"error_count": 5}' \
  --after '{"error_count": 0}'
```

### Search Procedural Memory
```bash
python3 skills/self-improving-agent/scripts/procedural_memory.py --search "backup"
```

## Cron Integration

Add to your cron jobs:

```json
{
  "name": "Self-Improvement",
  "schedule": "0 10 * * *",
  "command": "python3 skills/self-improving-agent/scripts/self_improvement_cycle.py"
}
```

## Requirements

- Python 3.10+
- OpenClaw workspace at /root/.openclaw/workspace
- Write access to memory/ directory

## Files

- `scripts/auto_trigger.py` - Auto-triggers on new errors
- `scripts/impact_measurement.py` - Measures improvement impact
- `scripts/procedural_memory.py` - Stores working procedures
- `scripts/self_improvement_cycle.py` - Main orchestrator
- `scripts/topic_selector.py` - Selects topics by priority

## Created By

- Based on production patterns: Reflection, PEV, Meta-Controller
- Tested in production environment
- Ready for ClawHub publication
