# Self-Improving Agent

Self-improving agent system for OpenClaw that learns from its own errors. Automatically detects issues, researches solutions, and implements improvements.

## Features

- **Auto-Trigger**: Automatically runs when new errors are detected
- **Topic Selection**: Analyzes error patterns and selects high-priority topics
- **Impact Measurement**: Records before/after metrics to measure improvement effectiveness
- **Procedural Memory**: Remembers working commands/scripts between sessions

## Installation

```bash
# Clone the repo
git clone https://github.com/mopga/self-improving-agent.git
cd self-improving-agent

# Copy scripts to your OpenClaw workspace
cp -r scripts/* /root/.openclaw/workspace/scripts/

# Or set custom workspace
export OPENCLAW_WORKSPACE=/path/to/your/workspace
```

## Configuration

The skill uses environment variables for paths:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENCLAW_WORKSPACE` | `/root/.openclaw/workspace` | Your OpenClaw workspace |

## Usage

### Run Full Cycle
```bash
python3 scripts/self_improvement_cycle.py
```

### Check Errors Only
```bash
python3 scripts/topic_selector.py --analyze-only
```

### Record Impact
```bash
python3 scripts/impact_measurement.py \
  --record \
  --task "Fix cron timeout" \
  --before '{"error_count": 5}' \
  --after '{"error_count": 0}'
```

### Search Procedural Memory
```bash
python3 scripts/procedural_memory.py --search "backup"
```

## Cron Integration

Add to your OpenClaw cron jobs:

```json
{
  "name": "Self-Improvement",
  "schedule": "0 10 * * *",
  "command": "python3 /path/to/workspace/scripts/self_improvement_cycle.py"
}
```

## Architecture

```
Errors → Auto-Trigger → Topic Selector → Research → Backlog → Agent PM
                                              ↓                    ↓
                                      Impact Measurement ← Procedural Memory
```

## Files

- `config.py` - Configuration (paths, workspace)
- `auto_trigger.py` - Auto-triggers on new errors
- `impact_measurement.py` - Measures improvement impact
- `procedural_memory.py` - Stores working procedures
- `self_improvement_cycle.py` - Main orchestrator
- `topic_selector.py` - Selects topics by priority

## Requirements

- Python 3.10+
- OpenClaw workspace
- Write access to memory/ directory

## Based On

- Reflection patterns (self-critique)
- PEV (Plan-Execute-Verify)
- Meta-Controller (topic routing)

## License

MIT
