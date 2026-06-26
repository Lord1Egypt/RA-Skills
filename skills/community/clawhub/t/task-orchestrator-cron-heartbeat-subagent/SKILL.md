---
name: task-orchestrator
version: 2.3.0
description: Unified Task Orchestration Hub v2.3 - Integrates Heartbeat, Cron, Subagent and Task Management. NEW: Channel Binding Configuration Guide. Provides task identification, standardized setup, execution tracking and best practice templates. Supports dynamic config loading, deadlock prevention and intelligent aggregation.
author: OpenClaw Community
license: MIT
tags:
  - task-management
  - heartbeat
  - cron
  - subagent
  - orchestration
  - automation
  - channel-binding
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["openclaw"]}}}
---

# Task Orchestrator v2.3 - Unified Task Orchestration Hub

> **Core Mission**: Enable agents to learn fundamental task creation and execution capabilities, including task identification, standardized setup, and execution tracking
> 
> **v2.3 New Features**: 
> - ✅ **Channel Binding Configuration** - Teach agents to use correct account for sending messages
> - ✅ **Cron Task Creation Checklist** - 6-step verification process
> - ✅ **Configuration Check Script** - Automated validation tool
> 
> **v2.0 Features**: Dynamic configuration loading, deadlock prevention mechanism, intelligent aggregation rules, 4-level risk confirmation boundaries

---

## 📡 Channel Binding Configuration Guide (v2.3 New) ⭐

### Core Concepts

Each Agent has its own **channel binding** in `openclaw.json`:

```json
{
  "agentId": "kk",
  "match": {
    "channel": "feishu",
    "accountId": "kk-feishu"
  }
}
```

**Meaning**:
- kk agent's messages should be sent via `kk-feishu` account
- Messages sent to `kk-feishu` account will be routed to kk agent
- **Scheduled tasks MUST specify agentId and accountId, otherwise they default to main agent using default account**

### Scheduled Task Configuration (❗Important)

**When creating scheduled tasks, MUST specify**:

```bash
openclaw cron add \
  --agentId "kk" \
  --session "kk" \
  --name "KK Heartbeat" \
  --cron "*/10 * * * *" \
  --channel feishu \
  --to "user:ou_xxx" \
  --accountId "kk-feishu" \
  --message "Execute heartbeat check"
```

**Parameter Description**:
| Parameter | Description | Required |
|------|------|------|
| `--agentId` | Specify which agent executes the task | ✅ Required |
| `--session` | Use agent's dedicated session (inherits channel binding) | ✅ Required |
| `--accountId` | Specify which Feishu account sends the message | ✅ Required |
| `--channel` | Message channel (feishu/telegram/etc) | ✅ Required |
| `--to` | Recipient user ID | ✅ Required |

**Wrong Examples** (will cause messages to be sent from wrong bot):

```bash
# ❌ Wrong 1: No agentId specified, defaults to main execution
openclaw cron add \
  --session isolated \
  --name "KK Heartbeat" \
  ...

# ❌ Wrong 2: Use isolated session, doesn't inherit agent binding
openclaw cron add \
  --session isolated \
  --agentId "kk" \
  ...

# ❌ Wrong 3: No accountId specified, defaults to default account
openclaw cron add \
  --agentId "kk" \
  --channel feishu \
  ...  # Missing --accountId
```

### Find Your AccountId

**Method 1: Check openclaw.json**
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for b in d.get('bindings', []):
    print(f\"Agent {b['agentId']}: {b['match']['accountId']}\")
"
```

**Method 2: Check routing rules**
```bash
grep -A 3 '"agentId": "kk"' ~/.openclaw/openclaw.json
```

**Method 3: Use check script**
```bash
python3 ~/.openclaw/skills/task-orchestrator/scripts/check_cron_config.py
```

### Best Practices

✅ **Recommended**:
- Specify `--agentId` explicitly for scheduled tasks
- Use agent's dedicated session (`--session kk`) instead of isolated
- Specify `--accountId` explicitly to ensure messages send from correct account
- Run check script to verify configuration before creating tasks

❌ **Avoid**:
- Not specifying agentId (defaults to main execution)
- Using isolated session (doesn't inherit channel binding)
- Relying on default accountId (defaults to default)
- Creating tasks without verifying configuration

### FAQ

**Q1: Why are my messages sent from default bot instead of kk bot?**

A: Because the scheduled task didn't specify `--agentId` and `--accountId`. By default:
- No agentId specified → executed by main agent
- No accountId specified → sent via default account

Solution: Specify explicitly when creating task:
```bash
openclaw cron add \
  --agentId "kk" \
  --session "kk" \
  --accountId "kk-feishu" \
  ...
```

**Q2: What's the difference between isolated session and agent dedicated session?**

A: 
- `isolated` session: Temporary isolated session, **doesn't inherit** agent's channel binding
- `kk` session: kk agent's dedicated session, **inherits** kk's channel binding (including accountId)

If you want to use a specific agent's configuration, should use agent's dedicated session:
```bash
--session "kk"  # ✅ Inherits kk's configuration
--session isolated  # ❌ Doesn't inherit any configuration
```

**Q3: How to verify scheduled task configuration is correct?**

A: Use these commands to verify:
```bash
# 1. View task list
openclaw cron list

# 2. Run configuration check script
python3 ~/.openclaw/skills/task-orchestrator/scripts/check_cron_config.py

# 3. Test execution
openclaw cron run {task_id}

# 4. Check Feishu message
# Confirm message is sent from correct bot
```

---

## 🎯 Core Capabilities

### 1. Task Type Identification (Enhanced)

Automatically identify user request task types and route to correct execution mode:

| Task Type | Trigger Features | Execution Method | Example |
|----------|----------|----------|------|
| **Heartbeat** | "regular check", "every heartbeat", "periodic monitoring" | Write to HEARTBEAT.md | "Check email every heartbeat" |
| **Cron** | "daily at X", "every Monday", "schedule", "remind me" | openclaw cron add | "Push news every day at 9am" |
| **Subagent** | "multi-step", "complex task", "break down", "parallel" | subagents spawn | "Research competitors and write report" |
| **Task** | "continuous task", "track", "record" | TASKS.md record | "Continuously monitor stock" |
| **Immediate** | Simple single-step task | Execute directly | "Check weather" |

### 2. Task Identification Flowchart (Enhanced)

```
User Request
    ↓
[Task Analysis]
    ├── Has exact time expression? → Cron Task
    ├── Has "heartbeat/regular"? → Heartbeat Task
    ├── Has "multi-step/complex"? → Subagent Task
    ├── Has "continuous/track"? → Task Record
    └── No special markers → Immediate Task
    ↓
[6-Point Checklist]
    ├── Task objective clear?
    ├── Constraints defined?
    ├── Complexity assessment
    ├── Question points identified
    ├── Resource requirements confirmed
    └── Risk points assessed
    ↓
[⚡ Clarification Confirmation] → Has questions/ambiguity/conflict → Generate clarification questions → User confirms
    ↓
[Show Task Plan] → User confirms
    ↓
[Execute] → Create/Dispatch/Record
    ↓
[Track] → Update status → Report results
```

---

## 📋 Task Identification Rules (Enhanced)

### Rule 1: Cron Task Identification

**Trigger Keywords**:
- Time expressions: "daily", "weekly", "monthly", "at X o'clock", "in X minutes"
- Scheduling: "schedule", "remind", "alarm", "cron"
- Cron expression format: "0 9 * * *"

**Judgment Logic**:
```python
def is_cron_task(user_input):
    # Check time expressions
    time_patterns = [
        r'daily\s*at\s*\d+',           # daily at 9
        r'every\s*(mon|tue|wed|thu|fri|sat|sun)',  # every Monday
        r'\d+\s*(minute|hour|day|week)s?\s*(later|from\s*now)',  # 10 minutes later
        r'in\s+\d+\s*(minute|hour|day|week)s?',  # in 10 minutes
        r'\d+\s+[*\d\s]+\d+',    # Cron expression
    ]
    
    # Check keywords
    cron_keywords = ['schedule', 'remind', 'alarm', 'cron', 'timer']
    
    has_time_expr = any(re.search(p, user_input, re.IGNORECASE) for p in time_patterns)
    has_keyword = any(k in user_input.lower() for k in cron_keywords)
    
    return has_time_expr or has_keyword
```

**Examples**:
- ✅ "Push news every day at 9am" → Cron
- ✅ "Remind me to meet in 10 minutes" → Cron (one-time)
- ✅ "Weekly meeting every Monday at 10am" → Cron (periodic)

---

### Rule 2: Heartbeat Task Identification

**Trigger Keywords**:
- "heartbeat", "regular", "every check", "periodic"
- "monitor", "polling", "cycle"
- "keep online", "auto check"

**Judgment Logic**:
```python
def is_heartbeat_task(user_input):
    # First exclude Cron tasks (have exact time)
    if is_cron_task(user_input):
        return False
    
    heartbeat_keywords = [
        'heartbeat', 'regular', 'every', 'periodic',
        'monitor', 'polling', 'cycle',
        'keep online', 'auto check', 'background'
    ]
    
    return any(k in user_input.lower() for k in heartbeat_keywords)
```

**Examples**:
- ✅ "Check unread email every heartbeat" → Heartbeat
- ✅ "Regularly check API status" → Heartbeat
- ❌ "Check at 9am daily" → Cron (has exact time)

---

### Rule 3: Subagent Task Identification (Enhanced)

**Trigger Keywords**:
- "multi-step", "break down", "step by step"
- "complex", "research", "analyze"
- "parallel", "multiple agents", "collaborate"

**Complexity Scoring (Enhanced)**:
```python
def calculate_complexity(user_input):
    score = 0
    
    # Action count (0-4 points)
    actions = count_actions(user_input)
    score += min(actions, 4)
    
    # Dependency relations (0-3 points)
    dependency_keywords = ['based on', 'using', 'then', 'after', 'step']
    if any(k in user_input.lower() for k in dependency_keywords):
        score += 2
        if 'step' in user_input.lower() or 'step-by-step' in user_input:
            score += 1
    
    # Scope size (0-3 points)
    scope_keywords = ['entire', 'complete', 'all', 'full', 'whole']
    if any(k in user_input.lower() for k in scope_keywords):
        score += 2
    
    return min(score, 10)

def is_subagent_task(user_input):
    # Action count >= 3 or complexity >= 5
    return count_actions(user_input) >= 3 or calculate_complexity(user_input) >= 5
```

**Complexity Levels**:
| Level | Score | Handling Method |
|------|------|----------|
| Simple | 1-3 | Single agent execution |
| Normal | 4-6 | Standard pipeline (2-3 agents) |
| Complex | 7-10 | Complex pipeline (multi-stage + review) |

**Examples**:
- ✅ "Research competitors and write analysis report" → Subagent (complexity 6)
- ✅ "Refactor this project, including tests and docs" → Subagent (complexity 8)
- ❌ "Check weather" → Immediate (complexity 1)

---

### Rule 4: Task Record Identification

**Trigger Keywords**:
- "continuous", "track", "tracking"
- "long-term", "ongoing", "project"
- "record to task system"

**Examples**:
- ✅ "Continuously monitor this stock trend" → Task Record
- ✅ "Track this project progress" → Task Record

---

## 🏗️ Standardized Setup Process (Enhanced)

### Process 1: Cron Task Setup (Enhanced)

#### Step 1: Requirements Analysis (6-Point Checklist)

**Checklist**:
1. **Task Objective** - What needs to be achieved?
2. **Constraints** - Time, scope, quality requirements?
3. **Complexity** - Simple/Normal/Complex?
4. **Question Points** - Information gaps need confirmation?
5. **Resource Requirements** - Which agents/tools needed?
6. **Risk Points** - Potential issues?

#### Step 2: Risk Classification (4 Levels)

| Level | Definition | Confirmation Requirement | Example |
|------|------|----------|------|
| 🟢 LOW | Reversible operation, no side effects | Auto-execute | Check weather, simple query |
| 🟡 MEDIUM | Limited side effects, rollback possible | Brief confirmation | Write normal code, send regular email |
| 🔴 HIGH | Major operation, needs backup | Detailed confirmation | Modify config, deploy to test environment |
| ⚫ CRITICAL | Irreversible, permanent impact | Explicit authorization | Delete data, publish to production, permission changes |

#### Step 3: Generate Task Plan

**Output Template**:
```markdown
## ⏰ Cron Task Plan

### Task Information
- **Task Type**: {One-time | Periodic}
- **Task Name**: {Short name}
- **Execution Time**: {ISO time or Cron expression}
- **Timezone**: Asia/Shanghai
- **Risk Level**: {🟢/🟡/🔴/⚫}

### Execution Content
{Specific task description to execute}

### Push Configuration
- **Channel**: Feishu
- **Recipient**: Boss (ou_xxx)

### Confirmation
Please confirm and I'll create this scheduled task ✓
```

#### Step 4: Create Task

**Standard Command Format**:
```bash
# One-time task
openclaw cron add \
  --agentId "{AGENT_ID}" \
  --session "{AGENT_ID}" \
  --name "{Task Name}" \
  --at "{ISO time or relative time}" \
  --channel feishu \
  --to "user:ou_642f1cb74d63462d1037375caac5ea2d" \
  --accountId "{ACCOUNT_ID}" \
  --message "{Execution content}" \
  --tz "Asia/Shanghai" \
  --description "{Task description}"

# Periodic task
openclaw cron add \
  --agentId "{AGENT_ID}" \
  --session "{AGENT_ID}" \
  --name "{Task Name}" \
  --cron "{Cron expression}" \
  --tz "Asia/Shanghai" \
  --channel feishu \
  --to "user:ou_642f1cb74d63462d1037375caac5ea2d" \
  --accountId "{ACCOUNT_ID}" \
  --message "{Execution content}" \
  --description "{Task description}"
```

#### Step 5: Verify and Track

```bash
# Verify task created
openclaw cron list

# Test task (optional)
openclaw cron run {task_id}

# Record to task system
Update TASKS.md, mark task type=Cron
```

---

### Process 2: Heartbeat Task Setup (Enhanced)

#### Step 1: Requirements Analysis

**Checklist**:
- [ ] Monitoring objective clear
- [ ] Check frequency reasonable (recommend 30-60 minutes)
- [ ] Output format defined (HEARTBEAT_OK or specific content)
- [ ] Cost assessment (involves API calls?)
- [ ] Quiet hours defined (default 22:00-08:00)

#### Step 2: Select Heartbeat Mode

**3 Modes**:
| Mode | Default Interval | Burst Interval | Use Case |
|------|----------|------------|----------|
| Conservative | 45m | 10m | Low noise, cost-sensitive |
| Balanced | 30m | 5m | General (default) |
| Aggressive | 15m | 2m | High priority event window |

#### Step 3: Generate HEARTBEAT.md Template

**Standard Template (Enhanced)**:
```markdown
# HEARTBEAT.md

## Core Task: {Task Name}

## Heartbeat Mode
- **Mode**: {Conservative | Balanced | Aggressive}
- **Default Interval**: {N} minutes
- **Quiet Hours**: 22:00-08:00

## Scheduled Task: {Task Description}

Execute following checks every heartbeat:

### Check Content
1. {Check item 1}
2. {Check item 2}

### Execution Flow
```bash
{Specific execution command}
```

### Output Rules
- **No anomaly**: Reply `HEARTBEAT_OK`
- **Anomaly detected**: Report specific content + suggested actions
- **Major event**: Report immediately (regardless of time period)

### Status Tracking
Read `memory/{task-name}-state.json` to avoid repeated execution.

Status file format:
```json
{
  "task_name": "{Task Name}",
  "last_execution": "ISO time",
  "execution_count": 0,
  "last_error": null,
  "last_result": null
}
```

### Cost Protection
- **Add pre-check before expensive operations**: Check if necessary first
- **Rate limit API calls**: Avoid multiple calls in short time
- **Night mode**: 22:00-08:00 silent (check only, no report)

### Trigger Definitions
- **Time trigger**: Every 30 minutes
- **Event trigger**: {Define event condition}
- **Conditional trigger**: {Define threshold condition}

### Alert Rules
Each trigger defines:
1. **Threshold**: {Specific value}
2. **Notification path**: {Feishu/Email etc.}
3. **Cooldown time**: {N} minutes (avoid repeated alerts)
```

#### Step 4: Create Status Tracking File

**memory/heartbeat-state.json**:
```json
{
  "task_name": "{Task Name}",
  "last_execution": null,
  "execution_count": 0,
  "last_error": null,
  "config": {
    "interval_minutes": 30,
    "quiet_hours": {"start": 22, "end": 8},
    "mode": "balanced"
  }
}
```

#### Step 5: Verify and Test

```bash
# Manually trigger heartbeat test
# Check if output meets expectations
# Confirm status file updated
```

---

### Process 3: Subagent Task Setup (Enhanced Version)

#### Step 1: Task Breakdown

**Analysis Dimensions**:
- Action count (file edits, command executions etc.)
- Dependency relations (step B depends on step A output)
- Complexity score (≥5 points recommend breakdown)
- Risk level assessment

#### Step 2: Select Pipeline

**3 Pipelines**:
| Pipeline | Complexity | Stages | Use Case |
|------|--------|------|----------|
| Simple | 1-3 | Execute→Validate→Complete | Simple tasks |
| Standard | 4-6 | Analyze→Execute→Review→Test→Validate | Normal tasks |
| Complex | 7-10 | Deep Analyze→Design Review→Execute→Parallel Review→Aggregate→Test→Validate | Complex/High-risk |

#### Step 3: Generate Task Plan

**Output Template (Enhanced)**:
```markdown
## 📋 Task Breakdown Plan

### Original Task
{User's task}

### Complexity Assessment
- **Action Count**: {N}
- **Dependency Relations**: {Yes/No}
- **Complexity Score**: {N}/10
- **Risk Level**: {🟢/🟡/🔴/⚫}
- **Recommended Pipeline**: {Simple | Standard | Complex}
- **Recommended Parallelism**: {N}

### Task List

| # | Task Description | Agent | Dependencies | Priority | Est. Time |
|---|----------|-------|------|--------|----------|
| 1 | {Task 1} | {agent-id} | - | P1 | {X}min |
| 2 | {Task 2} | {agent-id} | {Dep #} | P2 | {X}min |
| 3 | {Task 3} | {agent-id} | {Dep #} | P3 | {X}min |

### Dispatch Strategy
- **Parallel Tasks**: {Task numbers} (no dependencies)
- **Serial Tasks**: {Task numbers} (has dependencies)
- **Review Mode**: {Parallel | Serial}
- **Aggregation Rules**: {Majority | Unanimous | Veto}
- **Total Est. Time**: {X}min

### ⚡ Clarification Confirmation
{If questions exist, list here}

### Confirmation
Please confirm and I'll start dispatching subagents ✓
```

#### Step 4: Dispatch Execution

```bash
# Parallel dispatch (no dependencies)
subagents(action=spawn, agentId="researcher", task="{Task 1}", label="task-1")
subagents(action=spawn, agentId="coder", task="{Task 2}", label="task-2")

# Serial dispatch (has dependencies)
# Wait for task-1 to complete, then dispatch task-2
```

#### Step 5: Progress Tracking (Deadlock Prevention)

**memory/subagent-state.json**:
```json
{
  "task_id": "{Unique ID}",
  "status": "in_progress",
  "pipeline": "standard",
  "subagents": [
    {
      "label": "task-1",
      "agent_id": "researcher",
      "status": "completed",
      "output": "..."
    }
  ],
  "created_at": "ISO time",
  "updated_at": "ISO time",
  "deadlock_prevention": {
    "max_token": 100000,
    "used_token": 0,
    "max_time_minutes": 30,
    "elapsed_minutes": 0,
    "progress_checks": 0,
    "no_progress_count": 0
  }
}
```

**Deadlock Prevention Mechanism**:
- **Cost Metric**: Single task max token consumption (default 100K)
- **Time Metric**: Base timeout 30 minutes, dynamic adjustment
- **Progress Metric**: Check every 5 minutes, 3 consecutive no-progress → retry

#### Step 6: Result Aggregation (Intelligent Aggregation)

**Aggregation Rules**:
| Mode | Condition | Applicable Risk Level |
|------|------|--------------|
| Majority | >50% agree | LOW, MEDIUM |
| Unanimous | 100% agree | HIGH |
| Veto | Any reject | CRITICAL, Security-related |

**Conflict Resolution Strategy**:
1. **Role Priority**: critic > security > architect > reviewer > tester
2. **Third-party Arbitration**: architect arbitrates
3. **Re-review Mechanism**: Trigger when confidence < 0.7
4. **User Decision**: Ask user when unable to reach agreement

---

### Process 4: Task Record Setup

#### Step 1: Create Task Record

**TASKS.md Format**:
```markdown
## [Task ID] Task Title

- **Created:** YYYY-MM-DD HH:MM
- **Task Type:** Continuous Task | One-time Task
- **Current Status:** Not Started | In Progress | Completed | Paused
- **Task Description:** Detailed task content and objectives
- **System Functions Called:** List used OpenClaw functions/skills
- **Required Permissions:** List needed permissions
- **Dependent Software:** External software required
- **Last Updated:** YYYY-MM-DD HH:MM
- **Notes:** Other information
```

#### Step 2: Regular Status Updates

**Update Rules**:
- Check task progress every heartbeat
- Update "Last Updated" time when status changes
- Move to "Completed" area after completion

---

## 🔍 Task Execution Tracking (Enhanced Version)

### Unified Status Management

**memory/task-registry.json**:
```json
{
  "tasks": [
    {
      "id": "task-001",
      "type": "cron",
      "name": "Daily News Push",
      "status": "active",
      "created_at": "ISO time",
      "last_run": "ISO time",
      "next_run": "ISO time",
      "run_count": 15,
      "last_error": null
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

### Progress Reporting Mechanism

**Reporting Frequency**:
- Cron tasks: Report immediately after execution
- Heartbeat tasks: Report when anomaly detected
- Subagent tasks: Report at key nodes (start/complete/block)
- Task tasks: Report when status changes

**Report Template**:
```markdown
## 📊 Task Progress Report

### Task Name
{Task name}

### Current Status
{In Progress | Completed | Blocked}

### Progress Details
- **Completion**: {X}%
- **Time Elapsed**: {X} minutes
- **Next Step**: {Specific action}

### Issues/Blocks
{Describe issues if any}

### Decisions Needed
{List options if user decision needed}
```

---

## ⚠️ Deadlock Prevention Mechanism (New)

### Three Measurement Dimensions

#### 1. Cost Metric (Token Consumption)

**Threshold Configuration**:
```yaml
deadlock_prevention:
  max_token_per_task: 100000  # Base threshold
  
  # Task type multipliers
  token_multipliers:
    code: 1.0
    research: 1.5  # Search + analysis consumes more tokens
    review: 0.8
    test: 1.2
  
  # Complexity multipliers
  complexity_multipliers:
    simple: 0.5    # 50K
    normal: 1.0    # 100K
    complex: 1.5   # 150K
```

**Calculation Formula**:
```
Actual Threshold = Base Threshold × Task Type Multiplier × Complexity Multiplier
```

**Processing Flow**:
```
[Check Token Consumption]
    ↓
Exceed 80% threshold → [Warn User]
    ↓
Exceed 100% threshold → [Enter Retry Flow]
```

#### 2. Time Metric (Timeout Control)

**Threshold Configuration**:
```yaml
deadlock_prevention:
  base_timeout: 30  # Base timeout (minutes)
  
  # Task type time multipliers
  time_multipliers:
    simple: 0.5    # 15 min
    normal: 1.0    # 30 min
    complex: 2.0   # 60 min
  
  # Dynamic adjustment strategy
  dynamic_adjustment:
    enabled: true
    retry_multiplier: 1.5  # Increase 50% time after each retry
    max_timeout: 120       # Max timeout limit (2 hours)
```

**Timeout Processing Flow**:
```
[Timeout Detection]
    ↓
[Check Progress] → Has progress → [Extend timeout, continue]
    ↓ No progress
[Retry] → Remaining retries > 0 → [Redistribute]
    ↓
[Mark Failed] → [Enter Fallback Processing]
```

#### 3. Progress Metric (No Progress Detection)

**Threshold Configuration**:
```yaml
deadlock_prevention:
  progress_check_interval: 5  # Progress check interval (minutes)
  
  # No progress definition
  no_progress_definition:
    consecutive_checks: 3     # 3 consecutive checks with no state change (15 minutes)
    output_stale_minutes: 20  # Or: output not updated for 20 minutes
  
  # Progress tracking methods
  tracking:
    - agent_status_changes    # Status changes
    - output_file_updates     # File updates
    - message_count           # Message count
```

**Progress Determination Rules**:
| Metric | Has Progress | No Progress |
|------|--------|--------|
| Status | pending → running → completed | Running for 3 consecutive times |
| Output | File added/modified | No change |
| Messages | Has new messages | No messages |

### Complete Deadlock Prevention Flow

```
[Task Dispatch]
    ↓
[Start Timer]
    ↓
Every [progress_check_interval] minutes:
    ├── [Check token consumption] → Exceed 80% threshold → [Warn user]
    ├── [Check time] → Exceed timeout → [Enter no progress detection]
    └── [Check progress] → No progress → [Enter retry flow]
    
[Retry Flow]
    ├── Increase timeout (×1.5)
    ├── Reduce token threshold (×0.8)
    └── Retries count -1
    
[Final Failure]
    ├── Record detailed logs
    ├── Notify user
    └── Enter fallback processing
```

---

## 📚 Best Practice Template Library

### Template 1: Daily News Push (Cron)

**Standard Configuration**:
```bash
openclaw cron add \
  --agentId "main" \
  --session "main" \
  --name "Daily News Push" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --channel feishu \
  --to "user:ou_642f1cb74d63462d1037375caac5ea2d" \
  --accountId "default" \
  --message "Search today's AI industry news, organize into briefing and push to me" \
  --description "Push AI industry news every day at 9am"
```

**KK Agent Configuration Example**:
```bash
openclaw cron add \
  --agentId "kk" \
  --session "kk" \
  --name "KK Heartbeat 10min" \
  --cron "*/10 * * * *" \
  --tz "Asia/Shanghai" \
  --channel feishu \
  --to "user:ou_642f1cb74d63462d1037375caac5ea2d" \
  --accountId "kk-feishu" \
  --message "Execute heartbeat check" \
  --description "Execute heartbeat check every 10 minutes"
```

---

### Template 2: Email Check (Heartbeat)

```markdown
# HEARTBEAT.md

## Scheduled Task: Email Check

**Heartbeat Mode**: Balanced (30 minutes)
**Quiet Hours**: 22:00-08:00

Check unread email every heartbeat (about 30 minutes).

### Execution Flow

1. Read memory/email-state.json to get last check time
2. Call email API to get new emails
3. Has new email → Summarize and report (count + important email summary)
4. No new email → Reply HEARTBEAT_OK
5. Update email-state.json

### Output Rules

- No new email: `HEARTBEAT_OK`
- Has new email (<10): Summarize and report
- Has new email (≥10): Batch report + remind to clean

### Night Mode

During 22:00-08:00:
- Check only, no report (unless urgent)
- Save to morning first report for unified report

### Trigger Definitions

- **Time Trigger**: Every 30 minutes
- **Event Trigger**: New email arrival
- **Conditional Trigger**: Unread email ≥ 10

### Alert Rules

- **Threshold**: Unread email ≥ 20
- **Notification Path**: Feishu
- **Cooldown Time**: 60 minutes
```

---

### Template 3: Competitor Research (Subagent)

```markdown
## 📋 Task Breakdown Plan

### Original Task
Research competitors A, B, C features and pricing strategy, output analysis report

### Complexity Assessment
- **Action Count**: 5
- **Dependency Relations**: Yes
- **Complexity Score**: 7/10 (Complex)
- **Risk Level**: 🟡 MEDIUM
- **Recommended Pipeline**: Standard
- **Recommended Parallelism**: 3

### Task List

| # | Task Description | Agent | Dependencies | Priority | Est. Time |
|---|----------|-------|------|--------|----------|
| 1 | Research Competitor A | researcher | - | P1 | 5min |
| 2 | Research Competitor B | researcher | - | P1 | 5min |
| 3 | Research Competitor C | researcher | - | P1 | 5min |
| 4 | Comparative Analysis | analyst | 1,2,3 | P2 | 10min |
| 5 | Write Report | writer | 4 | P3 | 10min |

### Dispatch Strategy
- **Parallel**: 1,2,3 (no dependencies)
- **Serial**: 4→5 (has dependencies)
- **Review Mode**: Parallel (code + docs independent)
- **Aggregation Rules**: Majority
- **Total Est. Time**: ~25min

### Confirmation
Please confirm and I'll start dispatching subagents ✓
```

---

## 🔧 Configuration Loading Mechanism (New)

### Configuration File Structure

**task-orchestrator-config.yaml**:
```yaml
# ===========================================
# 1. Pipeline Configuration
# ===========================================
pipelines:
  simple:
    stages:
      - execute
      - validate
      - complete
    confirm_after: []
  
  standard:
    stages:
      - analyze
      - execute
      - review
      - test
      - validate
    confirm_after:
      - analyze
      - review
  
  complex:
    stages:
      - deep_analyze
      - design_review
      - execute
      - parallel_reviews
      - aggregate
      - test
      - validate
    confirm_after:
      - deep_analyze
      - design_review
      - aggregate

# ===========================================
# 2. Agent Mappings
# ===========================================
agent_mappings:
  task_types:
    code: coder
    research: researcher
    document: docs_writer
    test: tester
    review: reviewer
    architecture: architect

# ===========================================
# 3. Threshold Parameters
# ===========================================
thresholds:
  complexity:
    simple_max_steps: 1
    normal_max_steps: 3
    complex_min_steps: 4
  
  risk:
    low_cost_threshold: 10
    medium_cost_threshold: 50
    high_cost_threshold: 100
  
  deadlock_prevention:
    max_token_per_task: 100000
    max_time_minutes: 30
    max_retries: 2
    progress_check_interval: 5

# ===========================================
# 4. Business Rules
# ===========================================
business_rules:
  review_modes:
    parallel:
      - code + docs + test
      - multiple_features
    sequential:
      - architecture + implementation
      - security + any
  
  confirm_requirements:
    auto_execute: [LOW]
    brief_confirm: [MEDIUM]
    detailed_confirm: [HIGH]
    explicit_authorization: [CRITICAL]
  
  summary_rules:
    default_mode: majority
    veto_allowed_roles: [critic]
```

### Configuration Loading Timing

**Recommended: Load at task dispatch time**

```python
# Pseudocode
def dispatch_task(task):
    # Load configuration
    config = load_config("task-orchestrator-config.yaml")
    
    # Select pipeline based on task
    pipeline = select_pipeline(task, config.pipelines)
    
    # Select agent based on task type
    agent = select_agent(task, config.agent_mappings)
    
    # Execute
    execute_pipeline(pipeline, agent, config.thresholds)
```

---

## 📖 Related Skills

This skill integrates core capabilities from following skills:

- **agent-autopilot** - Self-driven workflow (3 scheduled tasks)
- **agent-heartbeat** - Heartbeat configuration
- **agent-step-sequencer** - Multi-step scheduling
- **cron-mastery** - Cron best practices
- **heartbeat-manager** - Heartbeat management (health score, intelligent timeout analysis)
- **task-dispatcher** - Task dispatch (6-point checklist, 4-level risk, deadlock prevention)
- **task-tracker** - Task tracking
- **let-me-know** - Long task notification

---

## 🎓 Learning Resources

- `/Users/chloe/Desktop/cron and heartbeat/` - Original skill collection
- `OpenClaw Documentation` - https://docs.openclaw.ai/automation/cron-jobs
- `HEARTBEAT.md Templates` - See this skill's template library
- `task-dispatcher Supplementary Design` - Deadlock prevention mechanism, intelligent aggregation rules

---

**Task Orchestrator v2.0.0** - Making task orchestration simpler, more reliable, and more intelligent
