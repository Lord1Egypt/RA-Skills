# Agent OS Architecture Guide

This guide defines the structure and purpose of each file in the Agent OS. Each file serves a distinct function and must not overlap with others.

## File Architecture

| File | Purpose | Analogy | Source of Truth |
|------|---------|---------|-----------------|
| `SOUL.md` | Personality, values, tone, behavioral boundaries | Character sheet | Tacit Profile → Communication Preferences |
| `AGENTS.md` | Step-by-step workflows and operating procedures | Operating manual | Tacit Profile → Workflow Steps + Decision Rules |
| `USER.md` | User profile, preferences, schedule, communication style | Employee handbook | Tacit Profile → Communication Preferences + Quality Criteria |
| `HEARTBEAT.md` | Periodic task checklist (cron-like recurring tasks) | Daily standup agenda | Tacit Profile → Workflow Steps (recurring) |
| `TOOLS.md` | Authorized tools and their usage constraints | Toolbox inventory | Tacit Profile → Workflow Steps (tools column) |

## File Generation Rules

### SOUL.md
Extract from the Tacit Profile's "Communication Preferences" and "Personal Best Practices" sections.
Structure:
```
# Soul
## Identity
[Who this agent is and what it stands for]
## Tone
[Communication style: formal/casual, direct/diplomatic, etc.]
## Boundaries
[What this agent will NOT do, ethical guardrails]
## Values
[What this agent prioritizes when making trade-offs]
```

### AGENTS.md
Extract from the Tacit Profile's "Workflow Steps" and "Decision Rules" sections.
Structure:
```
# Operating Manual
## Workflow: {{TASK_NAME}}
### Step 1: {{STEP}}
[Detailed instructions]
### Decision Point: {{DECISION}}
IF {{CONDITION}} THEN {{ACTION}}
### Edge Case: {{EXCEPTION}}
WHEN {{TRIGGER}} THEN {{RESPONSE}}
```

### USER.md
Extract from the Tacit Profile's "Communication Preferences" and "Quality Criteria" sections.
Structure:
```
# User Profile
## Name: {{USER_NAME}}
## Role: {{ROLE}}
## Preferences
[Schedule, communication channels, output format preferences]
## Quality Standards
[What "good" looks like, what "done" means]
```

### HEARTBEAT.md
Extract from the Tacit Profile's recurring workflow steps.
Structure:
```
# Heartbeat
## Daily
- [ ] {{DAILY_TASK_1}}
- [ ] {{DAILY_TASK_2}}
## Weekly
- [ ] {{WEEKLY_TASK_1}}
## Monthly
- [ ] {{MONTHLY_TASK_1}}
```

### TOOLS.md
Extract from the Tacit Profile's "Tools Used" column in workflow steps.
Structure:
```
# Authorized Tools
## {{TOOL_NAME}}
- Purpose: {{PURPOSE}}
- Access Level: {{READ/WRITE/EXECUTE}}
- Constraints: {{LIMITS}}
```

## Validation Checklist

After generating all files, verify:
1. Every workflow step from the Tacit Profile is represented in AGENTS.md.
2. Every decision rule is an explicit IF/THEN in AGENTS.md.
3. Every edge case is a WHEN/THEN exception in AGENTS.md.
4. SOUL.md tone matches the Tacit Profile's communication preferences.
5. TOOLS.md lists only tools mentioned in the Tacit Profile.
6. No information is duplicated across files.
