# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-operations skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events.

## Workspace Structure

```
~/.openclaw/
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Multi-agent coordination patterns
│   ├── SOUL.md                 # Behavioral guidelines and personality
│   ├── TOOLS.md                # Tool capabilities and gotchas
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── self-improving-operations/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-operations/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-operations
```

Or copy manually:

```bash
cp -r self-improving-operations ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-operations
openclaw hooks enable self-improving-operations
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Operations-Specific)

When operations learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Incident response steps | Runbook | "DB connection pool exhaustion recovery procedure" |
| Root cause analysis | Postmortem | "Monthly batch job causes OOM in worker pods" |
| Automation candidates | Automation backlog | "Certificate renewal should be fully automated" |
| Resource projections | Capacity model | "Storage grows 15%/month, need expansion by Q3" |
| Shift handoff gaps | On-call checklist | "Always verify cron job status at shift start" |
| Reliability targets | SLO definition | "API P99 latency must stay below 500ms" |
| Tool configuration | `TOOLS.md` | "PgBouncer pool_mode=transaction for batch workloads" |
| Workflow patterns | `AGENTS.md` | "Run pre-deploy checklist before production pushes" |

### Promotion Decision Tree

```
Is the learning service-specific?
├── Yes → Keep in .learnings/
└── No → Is it an incident response pattern?
    ├── Yes → Promote to runbook
    └── No → Is it a reliability target?
        ├── Yes → Promote to SLO definition
        └── No → Is it a toil/automation candidate?
            ├── Yes → Promote to automation backlog
            └── No → Promote to TOOLS.md or AGENTS.md
```

## Operations-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Incident repeats within 30 days | Log operations issue | OPERATIONS_ISSUES.md |
| MTTR exceeds target | Log with root cause | OPERATIONS_ISSUES.md |
| SLO/SLA breach | Log with error budget impact | OPERATIONS_ISSUES.md |
| Capacity threshold exceeded | Log with utilization data | OPERATIONS_ISSUES.md |
| Process bottleneck discovered | Log learning | LEARNINGS.md (process_bottleneck) |
| Manual step in pipeline | Log learning | LEARNINGS.md (automation_gap) |
| Alert fatigue detected | Log learning | LEARNINGS.md (monitoring) |
| Toil exceeds 50% of on-call | Log learning | LEARNINGS.md (toil_accumulation) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share an operational pattern with another session:
```
sessions_send(sessionKey="session-id", message="Incident pattern: DB connection pool exhaustion during batch ETL, use PgBouncer with separate pools")
```

### sessions_spawn

Spawn a background agent to analyze operational patterns:
```
sessions_spawn(task="Analyze .learnings/OPERATIONS_ISSUES.md for recurring incidents and promotion candidates", label="ops-pattern-review")
```

## Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `agent:bootstrap` | Before workspace files inject |
| `command:new` | When `/new` command issued |
| `command:reset` | When `/reset` command issued |
| `command:stop` | When `/stop` command issued |
| `gateway:startup` | When gateway starts |

## Verification

```bash
openclaw hooks list        # Check hook is registered
openclaw status            # Check skill is loaded
```

## Troubleshooting

### Hook not firing
1. Ensure hooks enabled in config
2. Restart gateway after config changes
3. Check gateway logs for errors

### Learnings not persisting
1. Verify `.learnings/` directory exists
2. Check file permissions
3. Ensure workspace path is configured correctly

### Skill not loading
1. Check skill is in skills directory
2. Verify SKILL.md has correct frontmatter
3. Run `openclaw status` to see loaded skills
