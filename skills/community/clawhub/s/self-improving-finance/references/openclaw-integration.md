# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-finance skill with OpenClaw.

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
│   └── self-improving-finance/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-finance/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-finance
```

Or copy manually:

```bash
cp -r self-improving-finance ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-finance
openclaw hooks enable self-improving-finance
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Finance-Specific)

When finance learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Close procedures | Close checklists | "Verify IC eliminations match both counterparties" |
| Reconciliation patterns | Reconciliation procedures | "Three-way match: PO, receipt, invoice" |
| Control gaps | Control matrices | "All JEs require dual approval regardless of amount" |
| Tax compliance | Tax calendars | "Embedded lease reassessment every Q4" |
| Forecast improvements | Forecast models | "Weight pipeline deals by stage probability" |
| Audit findings | Audit response templates | "Standard response for revenue recognition queries" |
| Workflow patterns | `AGENTS.md` | "Run trial balance before close meeting" |

### Promotion Decision Tree

```
Is the learning entity-specific?
├── Yes → Keep in .learnings/
└── No → Is it a close procedure?
    ├── Yes → Promote to close checklist
    └── No → Is it a control gap?
        ├── Yes → Promote to control matrix
        └── No → Is it a reconciliation pattern?
            ├── Yes → Promote to reconciliation procedures
            └── No → Promote to tax calendar, forecast model, or AGENTS.md
```

## Finance-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Reconciliation break | Log finance issue | FINANCE_ISSUES.md |
| SOX control failure | Log finance issue with control details | FINANCE_ISSUES.md |
| Budget variance >10% | Log finance issue with variance analysis | FINANCE_ISSUES.md |
| Late close item | Log finance issue with deadline impact | FINANCE_ISSUES.md |
| Intercompany imbalance | Log finance issue | FINANCE_ISSUES.md |
| Unusual JE flagged | Log finance issue with audit trigger | FINANCE_ISSUES.md |
| AR aging >90 days | Log finance issue with aging analysis | FINANCE_ISSUES.md |
| Control weakness found | Log learning | LEARNINGS.md (control_weakness) |
| Regulatory gap found | Log learning | LEARNINGS.md (regulatory_gap) |
| Valuation error | Log learning | LEARNINGS.md (valuation_error) |
| Cash flow anomaly | Log learning | LEARNINGS.md (cash_flow_anomaly) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a finance pattern with another session:
```
sessions_send(sessionKey="session-id", message="Reconciliation pattern: verify IC balances with both counterparties before posting eliminations")
```

### sessions_spawn

Spawn a background agent to analyze finance patterns:
```
sessions_spawn(task="Analyze .learnings/FINANCE_ISSUES.md for promotion candidates", label="finance-review")
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
