# Task Orchestrator v2.0 - Unified Task Orchestration Hub

> **Version**: 2.0.0  
> **Author**: OpenClaw Community  
> **Mission**: Enable agents to learn fundamental task creation and execution capabilities
> 
> **v2.0 New Features**: Dynamic configuration loading, deadlock prevention mechanism, intelligent aggregation rules, 4-level risk confirmation boundaries

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Version](https://img.shields.io/badge/OpenClaw-%3E%3D2026.4.0-blue)](https://openclaw.ai)
[![Skill Category](https://img.shields.io/badge/Category-Productivity-green)](https://clawhub.ai/skills)

---

## 🎯 Core Capabilities

This skill integrates core capabilities from Heartbeat, Cron, Subagent and Task Management:

1. **Task Type Identification** - Automatically identify heartbeat/cron/subagent/ordinary tasks
2. **Standardized Setup Process** - Provide templates and specifications to guide user configuration
3. **Task Execution Tracking** - Unified status management and progress tracking
4. **Best Practice Integration** - Integrate advantages from 17 skills
5. **⚡ v2.0 New Features**:
   - Dynamic configuration loading (YAML config files)
   - Deadlock prevention mechanism (cost/time/progress three dimensions)
   - Intelligent aggregation rules (majority/unanimous/veto)
   - 4-level risk confirmation boundaries (🟢LOW/🟡MEDIUM/🔴HIGH/⚫CRITICAL)

---

## 🚀 Quick Start

### Installation

```bash
# Via ClawHub (recommended)
clawhub install task-orchestrator

# Or manual copy
cp -r task-orchestrator ~/.openclaw/skills/
```

### Test Task Identification

```bash
# Test Cron task identification
python3 scripts/utils.py identify "Push news every day at 9am"

# Test Heartbeat task identification
python3 scripts/utils.py identify "Check email every heartbeat"

# Test Subagent task identification
python3 scripts/utils.py identify "Research competitors and write report"
```

**Output Example**:
```
Task Type: cron
Complexity Score: 3/10 (Simple)
Risk Level: 🟢 Reversible operation, auto-execute
```

---

## 📋 Task Identification Rules

### Cron Tasks
**Triggers**: Time expressions ("daily", "weekly", "at X o'clock", "in X minutes"), scheduling keywords ("schedule", "remind", "alarm")

**Examples**:
- ✅ "Push news every day at 9am" → Cron
- ✅ "Remind me to meet in 10 minutes" → Cron (one-time)

### Heartbeat Tasks
**Triggers**: "heartbeat", "regular", "every check", "monitor", "periodic" (excludes exact time expressions)

**Examples**:
- ✅ "Check unread email every heartbeat" → Heartbeat
- ✅ "Regularly check API status" → Heartbeat

### Subagent Tasks
**Triggers**: Action count ≥3 OR complexity score ≥5, keywords like "multi-step", "break down", "complex"

**Complexity Levels**:
- Simple (1-3): Single agent execution
- Normal (4-6): Standard pipeline (2-3 agents)
- Complex (7-10): Complex pipeline (multi-stage + review)

---

## 🏗️ Standardized Setup Process

### Process 1: Cron Task Setup

**6-Point Checklist**:
1. Task Objective - What needs to be achieved?
2. Constraints - Time, scope, quality requirements?
3. Complexity - Simple/Normal/Complex?
4. Question Points - Information gaps need confirmation?
5. Resource Requirements - Which agents/tools needed?
6. Risk Points - Potential issues?

**4-Level Risk Classification**:
| Level | Icon | Confirmation | Example |
|------|------|----------|------|
| LOW | 🟢 | Auto-execute | Check weather |
| MEDIUM | 🟡 | Brief confirm | Write code |
| HIGH | 🔴 | Detailed confirm | Modify config |
| CRITICAL | ⚫ | Explicit auth | Delete data |

---

### Process 2: Heartbeat Task Setup

**3 Heartbeat Modes**:
| Mode | Interval | Burst | Use Case |
|------|----------|-------|----------|
| Conservative | 45m | 10m | Low noise, cost-sensitive |
| Balanced | 30m | 5m | General (default) |
| Aggressive | 15m | 2m | High priority events |

---

### Process 3: Subagent Task Setup

**3 Pipelines**:
| Pipeline | Complexity | Stages |
|------|--------|------|
| Simple | 1-3 | Execute→Validate→Complete |
| Standard | 4-6 | Analyze→Execute→Review→Test→Validate |
| Complex | 7-10 | Deep Analyze→Design Review→Execute→Parallel Review→Aggregate→Test→Validate |

---

## ⚠️ Deadlock Prevention Mechanism

### Three Measurement Dimensions

#### 1. Cost Metric (Token Consumption)
- Base threshold: 100K tokens
- Dynamic multipliers by task type and complexity
- Warn at 80%, abort at 100%

#### 2. Time Metric (Timeout Control)
- Base timeout: 30 minutes
- Dynamic adjustment with retry multiplier 1.5x
- Max timeout: 120 minutes

#### 3. Progress Metric (No Progress Detection)
- Check interval: 5 minutes
- No progress definition: 3 consecutive checks with no state change
- Action: Retry with adjusted parameters

---

## 🔧 Configuration

### Dynamic Configuration Loading

Edit `config/task-orchestrator-config.yaml`:

```yaml
# Adjust complexity thresholds
thresholds:
  complexity:
    simple_max_steps: 2      # Default 1
    normal_max_steps: 4      # Default 3
    complex_min_steps: 5     # Default 4

# Adjust deadlock prevention thresholds
deadlock_prevention:
  max_token_per_task: 150000  # Default 100K
  max_time_minutes: 45        # Default 30
```

### View Current Configuration

```bash
python3 scripts/utils.py config
```

---

## 📚 Template Files

| Template | Path | Purpose |
|----------|------|---------|
| HEARTBEAT | `templates/HEARTBEAT-template.md` | Heartbeat task configuration |
| TASKS | `templates/TASKS-template.md` | Task record management |
| Subagent | `templates/Subagent-Plan-template.md` | Complex task breakdown |
| Cron | `templates/Cron-template.md` | Scheduled task configuration |

**Usage**:
```bash
# Copy template
cp templates/HEARTBEAT-template.md workspace/HEARTBEAT.md
```

---

## 🔍 Utility Commands

```bash
# Identify task type + complexity + risk
python3 scripts/utils.py identify "Research competitors and write report"

# Parse time
python3 scripts/utils.py parse_time "tonight at 8pm"

# Calculate complexity
python3 scripts/utils.py complexity "Refactor entire project"

# Assess risk
python3 scripts/utils.py risk "Delete production database"

# Select pipeline by complexity score
python3 scripts/utils.py pipeline 7
# Output: Recommended pipeline: complex

# Generate task dashboard
python3 scripts/utils.py dashboard

# Register new task
python3 scripts/utils.py register \
  task-001 cron "Daily News Push"
```

---

## 📊 Task Registry

**Location**: `memory/task-registry.json`

**View Task List**:
```bash
cat memory/task-registry.json
```

**Example Content**:
```json
{
  "tasks": [
    {
      "id": "cron-001",
      "type": "cron",
      "name": "Daily News Push",
      "status": "active",
      "created_at": "2026-04-04T09:00:00+08:00",
      "next_run": "2026-04-05T09:00:00+08:00",
      "run_count": 15
    }
  ],
  "stats": {
    "total": 10,
    "active": 5,
    "completed": 4,
    "failed": 1
  }
}
```

---

## 🎓 Learning Resources

- **SKILL.md** - Complete skill documentation
- **QUICKSTART.md** - Quick start guide
- **templates/** - Template files
- **config/** - Configuration examples
- **scripts/utils.py** - Utility functions source code

---

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines before submitting PRs.

**TODO**:
- [ ] Add more task templates
- [ ] Support more task type identification
- [ ] Optimize complexity scoring algorithm
- [ ] Add web interface

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

This skill integrates best practices from 17 community skills:
- agent-autopilot - Self-driven workflow
- agent-heartbeat - Heartbeat configuration
- agent-step-sequencer - Multi-step scheduling
- cron-mastery - Cron best practices
- heartbeat-manager - Heartbeat management
- task-dispatcher - Task dispatch
- task-tracker - Task tracking
- let-me-know - Long task notification
- And more...

---

**Task Orchestrator v2.0.0** - Making task orchestration simpler, more reliable, and more intelligent

## 📦 Package Info

- **Name**: task-orchestrator
- **Version**: 2.0.0
- **Author**: OpenClaw Community
- **License**: MIT
- **Category**: Productivity
- **Difficulty**: Intermediate
- **Setup Time**: 5 minutes
