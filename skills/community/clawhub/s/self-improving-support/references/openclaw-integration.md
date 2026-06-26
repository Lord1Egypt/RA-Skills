# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-support skill with OpenClaw.

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
│   └── self-improving-support/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-support/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-support
```

Or copy manually:

```bash
cp -r self-improving-support ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-support
openclaw hooks enable self-improving-support
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Support-Specific)

When support learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Diagnostic patterns | KB article | "502 errors on webhooks — check customer WAF first" |
| Triage workflows | Troubleshooting tree | "Login failure: SSO vs local vs MFA decision flow" |
| Escalation insights | Escalation matrix | "Database deadlocks → DBA on-call, not general eng" |
| Common resolutions | Canned response | "Password reset steps for enterprise SSO customers" |
| Communication tone | `SOUL.md` | "Acknowledge frustration before offering solutions" |
| Triage automation | `AGENTS.md` | "Auto-categorize by keyword before human triage" |
| Tool configuration | `TOOLS.md` | "Zendesk macro for bulk SLA extension on outages" |

### Promotion Decision Tree

```
Is the learning customer-specific?
├── Yes → Keep in .learnings/
└── No → Is it a diagnostic pattern?
    ├── Yes → Promote to KB article or troubleshooting tree
    └── No → Is it an escalation insight?
        ├── Yes → Promote to escalation matrix
        └── No → Is it a common resolution?
            ├── Yes → Promote to canned response template
            └── No → Promote to SOUL.md, TOOLS.md, or AGENTS.md
```

## Support-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Repeat ticket detected | Log ticket issue | TICKET_ISSUES.md |
| SLA breach occurred | Log ticket issue with timeline | TICKET_ISSUES.md |
| Misdiagnosis identified | Log ticket issue with root cause | TICKET_ISSUES.md |
| Ticket reopened | Log ticket issue | TICKET_ISSUES.md |
| KB search returned nothing | Log learning | LEARNINGS.md (knowledge_gap) |
| Escalation path unclear | Log learning | LEARNINGS.md (escalation_gap) |
| Customer churn signal | Log learning | LEARNINGS.md (customer_churn_signal) |
| Resolution delayed | Log learning | LEARNINGS.md (resolution_delay) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a support pattern with another session:
```
sessions_send(sessionKey="session-id", message="Misdiagnosis pattern: 502 on webhooks is usually customer WAF, not our infra")
```

### sessions_spawn

Spawn a background agent to analyze support patterns:
```
sessions_spawn(task="Analyze .learnings/TICKET_ISSUES.md for promotion candidates", label="support-review")
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
