# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-sales skill with OpenClaw.

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
│   └── self-improving-sales/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-sales/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-sales
```

Or copy manually:

```bash
cp -r self-improving-sales ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-sales
openclaw hooks enable self-improving-sales
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Sales-Specific)

When sales learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Objection patterns | Objection handling scripts | "When they say 'too expensive', reframe to ROI" |
| Competitor intelligence | Battle cards | "Competitor Y free tier — counter with TCO analysis" |
| Qualification gaps | MEDDIC/BANT frameworks | "Always confirm budget approval in writing before commit" |
| Pricing patterns | Pricing playbooks | "Never discount >15% without VP approval + multi-year" |
| Win/loss patterns | Deal review templates | "No champion by Stage 3 = 12% close rate" |
| Process improvements | `AGENTS.md` | "Update CRM within 24 hours of every meeting" |

### Promotion Decision Tree

```
Is the learning deal-specific?
├── Yes → Keep in .learnings/
└── No → Is it an objection pattern?
    ├── Yes → Promote to battle card or objection handler
    └── No → Is it competitive intelligence?
        ├── Yes → Promote to battle card
        └── No → Is it a qualification insight?
            ├── Yes → Promote to MEDDIC/BANT framework
            └── No → Promote to pricing playbook or AGENTS.md
```

## Sales-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Deal stuck >30 days | Log deal issue | DEAL_ISSUES.md (pipeline_leak) |
| Objection couldn't handle | Log learning | LEARNINGS.md (objection_pattern) |
| Pricing mistake found | Log deal issue | DEAL_ISSUES.md (pricing_error) |
| Forecast miss >20% | Log deal issue | DEAL_ISSUES.md (forecast_miss) |
| Lost to competitor | Log learning | LEARNINGS.md (competitor_shift) |
| Deal velocity dropping | Log learning | LEARNINGS.md (deal_velocity_drop) |
| Discount >20% requested | Log deal issue | DEAL_ISSUES.md (pricing_error) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a deal pattern with another session:
```
sessions_send(sessionKey="session-id", message="Competitor Y launched free tier — update all SMB deal battle cards")
```

### sessions_spawn

Spawn a background agent to analyze deal patterns:
```
sessions_spawn(task="Analyze .learnings/DEAL_ISSUES.md for promotion candidates", label="deal-review")
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
