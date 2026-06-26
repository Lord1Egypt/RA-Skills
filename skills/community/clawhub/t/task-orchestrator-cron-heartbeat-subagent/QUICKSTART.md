# Task Orchestrator v2.3 - Quick Start Guide

> Get started in 5 minutes - Enable agents to learn task orchestration
> 
> **v2.3 New**: Channel Binding Configuration Guide - Ensure messages send from correct account

---

## 🚀 Quick Start

### Step 1: Confirm Skill is Installed

```bash
ls ~/.openclaw/skills/task-orchestrator/
```

Should see:
```
├── SKILL.md
├── README.md
├── config/
├── scripts/
└── templates/
```

---

### Step 2: Test Task Identification

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

### Step 3: Create Your First Task

#### Scenario A: Create Cron Task (Scheduled Reminder)

**User Input**:
```
Remind me to meet in 10 minutes
```

**Agent Processing Flow**:
1. Identify as Cron task
2. Generate task plan
3. User confirms
4. Execute creation command
5. Record to task registry

**Agent Output**:
```markdown
## ⏰ Cron Task Plan

### Task Information
- **Task Type**: One-time
- **Task Name**: Meeting Reminder
- **Execution Time**: In 10 minutes
- **Timezone**: Asia/Shanghai
- **Risk Level**: 🟢 LOW

### Execution Content
Remind me to meet

### Confirmation
Please confirm and I'll create this scheduled task ✓
```

**After Confirmation**:
```bash
openclaw cron add \
  --agentId "main" \
  --session "main" \
  --name "Meeting Reminder" \
  --at "+10m" \
  --session "main" \
  --channel feishu \
  --to "user:ou_642f1cb74d63462d1037375caac5ea2d" \
  --accountId "default" \
  --message "Reminder: Meeting in 10 minutes" \
  --tz "Asia/Shanghai" \
  --description "Remind meeting in 10 minutes"
```

**❗Important**:
- `--agentId "main"` - Specify main agent executes
- `--session "main"` - Use main's dedicated session (inherits channel binding)
- `--accountId "default"` - Specify send from default account

If it's kk agent's task, should use:
```bash
openclaw cron add \
  --agentId "kk" \
  --session "kk" \
  --accountId "kk-feishu" \
  ...
```

**Run Configuration Check**:
```bash
python3 ~/.openclaw/skills/task-orchestrator/scripts/check_cron_config.py
```

---

#### Scenario B: Create Heartbeat Task (Regular Check)

**User Input**:
```
Check GitHub Issues every heartbeat
```

**Agent Processing Flow**:
1. Identify as Heartbeat task
2. Select heartbeat mode (default Balanced)
3. Generate HEARTBEAT.md template
4. Create status tracking file
5. Test execution

**Agent Output**:
```markdown
## 💓 Heartbeat Task Configuration

### Task Information
- **Task Type**: Heartbeat
- **Task Name**: GitHub Issues Check
- **Heartbeat Mode**: Balanced (30 minutes)
- **Quiet Hours**: 22:00-08:00

### Check Content
1. Read last check time
2. Query GitHub Issues
3. Has new issue → Summarize and report
4. No new issue → HEARTBEAT_OK

### Confirmation
Please confirm and I'll write to HEARTBEAT.md ✓
```

**After Confirmation**:
1. Copy template to `workspace/HEARTBEAT.md`
2. Create `memory/github-issues-state.json`
3. Test execution once

---

#### Scenario C: Create Subagent Task (Complex Task)

**User Input**:
```
Research AI Agent trends and write report
```

**Agent Processing Flow**:
1. Identify as Subagent task
2. Calculate complexity score (7/10, Complex)
3. Select pipeline (Complex)
4. Break down tasks
5. Show plan and confirm
6. Dispatch subagents

**Agent Output**:
```markdown
## 📋 Task Breakdown Plan

### Original Task
Research AI Agent trends and write report

### Complexity Assessment
- **Action Count**: 5
- **Dependency Relations**: Yes
- **Complexity Score**: 7/10 (Complex)
- **Risk Level**: 🟡 MEDIUM
- **Recommended Pipeline**: Complex
- **Recommended Parallelism**: 2

### Task List

| # | Task Description | Agent | Dependencies | Est. Time |
|---|----------|-------|------|----------|
| 1 | Research AI Agent tech trends | researcher | - | 5min |
| 2 | Research mainstream products | researcher | - | 5min |
| 3 | Comparative analysis | analyst | 1,2 | 10min |
| 4 | Write report | writer | 3 | 10min |

### Dispatch Strategy
- **Parallel**: 1,2 (no dependencies)
- **Serial**: 3→4 (has dependencies)
- **Review Mode**: Parallel (research + analysis independent)
- **Aggregation Rules**: Majority
- **Total Est. Time**: ~30min

### Confirmation
Please confirm and I'll start dispatching subagents ✓
```

---

## 🔧 Common Commands

### Task Identification Tests

```bash
# Identify task type + complexity + risk
python3 scripts/utils.py identify "Research competitors and write report"

# Parse time
python3 scripts/utils.py parse_time "tonight at 8pm"

# Calculate complexity
python3 scripts/utils.py complexity "Refactor entire project"

# Assess risk
python3 scripts/utils.py risk "Delete production database"
```

### Configuration Management

```bash
# View current configuration
python3 scripts/utils.py config

# Select pipeline (by complexity score)
python3 scripts/utils.py pipeline 7
# Output: Recommended pipeline: complex
```

### Task Registration

```bash
# Register new task
python3 scripts/utils.py register \
  task-001 cron "Daily News Push"

# Generate dashboard
python3 scripts/utils.py dashboard
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

## 🎯 Task Identification Quick Reference

| User Input | Identified As | Handling Method |
|----------|----------|----------|
| "Daily at 9am push" | Cron | openclaw cron add |
| "Remind in 10 minutes" | Cron | openclaw cron add --at "+10m" |
| "Every heartbeat check" | Heartbeat | Write to HEARTBEAT.md |
| "Regularly check" | Heartbeat | Write to HEARTBEAT.md |
| "Research and write report" | Subagent | Break down tasks → Dispatch |
| "Refactor this project" | Subagent | Select pipeline → Execute |
| "Continuously monitor" | Task | Record to TASKS.md |
| "Check weather" | Immediate | Execute directly |

---

## ⚠️ Risk Level Quick Reference

| Level | Icon | Confirmation | Example |
|------|------|----------|------|
| LOW | 🟢 | Auto-execute | Check weather, simple query |
| MEDIUM | 🟡 | Brief confirm | Write code, send email |
| HIGH | 🔴 | Detailed confirm | Modify config, deploy to test |
| CRITICAL | ⚫ | Explicit auth | Delete data, publish to production |

---

## 📚 Template File Locations

| Template | Path | Purpose |
|----------|------|------|
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

## 🔍 Troubleshooting

### Issue 1: Task Identification Error

**Symptom**: Task type identified incorrectly

**Solution**:
1. Manually test identification: `python3 scripts/utils.py identify "task description"`
2. Check if keywords match
3. Adjust identification rules

### Issue 2: Cron Task Not Executing

**Symptom**: Scheduled task not executing after creation

**Solution**:
1. Check if Gateway is running
2. Verify timezone setting: `--tz "Asia/Shanghai"`
3. Manual test: `openclaw cron run {task_id}`
4. View task list: `openclaw cron list`

### Issue 3: Heartbeat No Response

**Symptom**: No response after HEARTBEAT.md configuration

**Solution**:
1. Check if HEARTBEAT.md format is correct
2. Confirm status file path
3. Test output is `HEARTBEAT_OK`
4. Check Gateway heartbeat interval configuration

### Issue 4: Subagent Dispatch Failure

**Symptom**: No response after subagent dispatch

**Solution**:
1. Check deadlock prevention status
2. View subagent status: `subagents(action=list)`
3. Check token consumption and time
4. Retry or redistribute

---

## 📖 Advanced Usage

### Custom Configuration

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

### Custom Agent Mappings

```yaml
agent_mappings:
  task_types:
    my_custom_task: my_specialist_agent
```

### Add New Triggers

```yaml
triggers:
  event_based:
    - event: "my_custom_event"
      threshold: 5
      action: "notify"
```

---

## 🎓 Learning Resources

- **SKILL.md** - Complete skill documentation
- **templates/** - Template files
- **config/** - Configuration examples
- **scripts/utils.py** - Utility functions source code

---

**Task Orchestrator v2.0.0** - Making task orchestration simpler, more reliable, and more intelligent
