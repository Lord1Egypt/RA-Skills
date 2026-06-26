# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-analytics skill with OpenClaw.

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
│   └── self-improving-analytics/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-analytics/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-analytics
```

Or copy manually:

```bash
cp -r self-improving-analytics ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-analytics
openclaw hooks enable self-improving-analytics
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Analytics-Specific)

When analytics learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Metric definitions | Data dictionary | "Active user = login within 7 days, feature interaction" |
| Pipeline failure patterns | Pipeline runbooks | "DST partition handling for hourly ingestion" |
| Visualization standards | Dashboard style guide | "Absolute value charts must start Y-axis at zero" |
| Data quality rules | Data quality SLAs | "NULL rate in key columns must be <0.1%" |
| Governance patterns | `AGENTS.md` | "New metrics require data dictionary entry before dashboard" |
| Tool configuration | `TOOLS.md` | "dbt source freshness checks required on all external sources" |

### Promotion Decision Tree

```
Is the learning project-specific?
├── Yes → Keep in .learnings/
└── No → Is it a metric definition?
    ├── Yes → Promote to data dictionary
    └── No → Is it a pipeline reliability pattern?
        ├── Yes → Promote to pipeline runbook
        └── No → Is it a visualization standard?
            ├── Yes → Promote to dashboard style guide
            └── No → Promote to data quality SLAs or TOOLS.md
```

## Analytics-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| ETL/ELT job failure | Log data issue | DATA_ISSUES.md |
| Data freshness breach | Log data issue with SLA details | DATA_ISSUES.md |
| Metric value anomaly | Log data issue with statistical context | DATA_ISSUES.md |
| NULL rate spike | Log data issue with column details | DATA_ISSUES.md |
| Schema drift detected | Log data issue with diff | DATA_ISSUES.md |
| Definition conflict | Log learning | LEARNINGS.md (definition_mismatch) |
| Visualization misleads | Log learning | LEARNINGS.md (visualization_mislead) |
| Metric drift discovered | Log learning | LEARNINGS.md (metric_drift) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a data quality finding with another session:
```
sessions_send(sessionKey="session-id", message="Data issue: NULL rate in user_id spiked to 2.3% after Oracle→PG migration, add ingestion validation")
```

### sessions_spawn

Spawn a background agent to analyze data quality patterns:
```
sessions_spawn(task="Analyze .learnings/DATA_ISSUES.md for promotion candidates", label="dq-review")
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
