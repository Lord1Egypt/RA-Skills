---
name: task-detection-thinking
description: Incomplete task detection + proactive thinking. Automatically scans task status, identifies anomalies, generates solutions, and attempts auto-fixes.
version: 1.0.0
author: OpenDolph
source: https://github.com/OpenDolph/skills/tree/main/task-detection-thinking
---

# Task Detection + Proactive Thinking Skill

> Automatically detect task anomalies, intelligently analyze causes, and proactively propose solutions

---

## Trigger Conditions

| Scenario | Trigger Method |
|----------|----------------|
| Auto-trigger | Execute during Heartbeat detection |
| Manual trigger | User inputs "check tasks", "task status", "anomaly detection" |
| Scheduled trigger | Auto-scan every 6 hours |

---

## Task Management File Standards

### HEARTBEAT.md - Global Task Board Template

```markdown
## Global Task Board
| TaskID | Task Name | Status | Progress | Deadline | Last Update | Block Reason |
|--------|-----------|--------|----------|----------|-------------|--------------|
| T001 | Initialize three-layer memory | Done | 100% | 2026-03-10 | 2026-03-10 | None |
| T002 | Integrate vector retrieval | Active | 60% | 2026-03-15 | 2026-03-12 | Waiting for API key |
| T003 | Test proactive thinking | Waiting | 0% | 2026-03-20 | 2026-03-11 | Depends on T002 |
```

**Status Definitions:**
| Status | Meaning |
|--------|---------|
| Queue | Waiting to start |
| Active | In progress |
| Waiting | Blocked/Waiting |
| Done | Completed |
| Aborted | Cancelled |

### WORKING.md - Project-Level Task Rules

All subtasks must include:
- **Status**: Queue/Active/Waiting/Done
- **Progress**: Percentage (0-100%)
- **Owner**: Person responsible
- **Dependencies**: Task IDs this task depends on

**Auto-Detection Rules:**
- Active tasks stalled >24h → Auto-marked as "Abnormal" 🔴
- Blocked tasks must fill: "Block Reason" + "Support Needed"
- Daily 23:00 → Auto-summary to HEARTBEAT.md

---

## Detection Rules (Auto-execute)

### 1. Scan HEARTBEAT.md

| Detection Item | Condition | Mark |
|----------------|-----------|------|
| Stalled tasks | Active status + last update > 24h | 🔴 Stalled |
| Pending confirmation | Waiting status + empty block reason | 🟡 Pending |
| Overdue tasks | Progress < 100% + deadline < current time | 🔴 Overdue |
| No progress tasks | Active status + 0% progress for > 48h | 🟡 No progress |
| Abnormal tasks | Active + no update > 24h | 🔴 Abnormal |

### 2. Scan WORKING.md

| Detection Item | Condition | Mark |
|----------------|-----------|------|
| Dependency block | Downstream blocked by incomplete upstream | 🔗 Dependency block |
| Duplicate tasks | Task name/content similarity > 80% | ⚠️ Duplicate |
| Zombie tasks | Done status but no completion time | 👻 Zombie |
| Meaningless tasks | Empty title or content < 10 chars | 🗑️ To clean |
| Missing required fields | No status/progress/owner | ⚠️ Incomplete |

---

## Proactive Thinking Logic

### For "Stalled Tasks"

**Analysis Steps:**
1. Check last update content → Determine stall type
2. Scan related memories → Find context
3. Generate 3 advancement solutions

**Auto-attempt (No human needed):**
- Supplement missing info (extract from memory)
- Retry failed interfaces/commands
- Update task status to Waiting (if needed)

**Human intervention required:**
- Generate detailed reminder, push via Feishu

### For "Blocked Tasks"

**Analysis Steps:**
1. Identify block type (resource/dependency/decision/external)
2. Determine if auto-solvable
3. Record solution to warm memory

**Auto-resolve scenarios:**
- Dependency task completed → Auto-unblock
- Resource now available → Auto-retry
- Info supplemented → Auto-advance

### For "Overdue Tasks"

**Analysis Steps:**
1. Assess remaining workload
2. Determine delay impact
3. Generate adjustment plan

**Auto-adjust:**
- Update deadline to reasonable value
- Adjust downstream task schedule
- Mark as high priority

---

## Output Rules

| Output Type | Location | Trigger Condition |
|-------------|----------|-------------------|
| Detection results | `memory/hot/task-alert.md` | After each detection |
| Thinking conclusions | `memory/hot/thinking-log.md` | After each analysis |
| Critical alerts | Feishu push | Overdue/serious block |
| Solutions | `memory/warm/lessons_learned.md` | Record after resolution |

---

## Usage Examples

```bash
# Manual trigger detection
node skills/task-detection-thinking/scripts/detect.js

# View detection results
cat memory/hot/task-alert.md

# View thinking log
cat memory/hot/thinking-log.md
```

---

## Configuration Parameters

```yaml
task_detection:
  # Detection frequency
  heartbeat_check: true      # Detect during Heartbeat
  cron_schedule: "0 */6 * * *"  # Every 6 hours
  
  # Threshold settings
  stale_threshold_hours: 24   # Stall threshold
  overdue_check: true         # Check overdue
  dependency_check: true      # Check dependency chain
  
  # Auto-fix
  auto_fix_enabled: true      # Enable auto-fix
  auto_fix_max_attempts: 3    # Max auto-attempts
  
  # Notification settings
  feishu_alert: true          # Critical alert push
  alert_on_overdue: true      # Overdue alert
  alert_on_blocking: true     # Serious block alert
```

---

## Workflow

```
Heartbeat trigger / Scheduled trigger / Manual trigger
    ↓
Scan HEARTBEAT.md + WORKING.md
    ↓
Identify anomaly tasks (stalled/blocked/overdue/duplicate)
    ↓
Analyze causes (context + historical memory)
    ↓
Generate solutions (3 options)
    ↓
Attempt auto-fix (no-human-needed solutions)
    ↓
Write detection results + thinking log
    ↓
Push critical alerts to Feishu
```

---

## Integration with Existing Systems

- **HEARTBEAT.md** - Read global task board
- **WORKING.md** - Read subtask details
- **Three-layer memory system** - Store detection results and thinking logs
- **ClawMemory** - Query historical solutions
- **Feishu** - Push critical alerts

---

*Transform task management from reactive response to proactive prevention*
