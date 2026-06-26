# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-hr skill with OpenClaw.

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
│   └── self-improving-hr/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-hr/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-hr
```

Or copy manually:

```bash
cp -r self-improving-hr ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-hr
openclaw hooks enable self-improving-hr
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (HR-Specific)

When HR learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Onboarding patterns | Onboarding checklists | "IT setup must be completed before start date" |
| Interview insights | Interview scorecards | "Structured behavioral questions reduce bias" |
| Compliance findings | Compliance calendars | "I-9 re-verification due dates for visa holders" |
| Policy gaps | Policy documents | "Remote work policy for international contractors" |
| Recruiting patterns | Recruiting playbooks | "48-hour offer deadline improves acceptance rate" |
| Workflow improvements | `AGENTS.md` | "Run compliance check before generating offer letter" |

### Promotion Decision Tree

```
Is the learning organization-specific?
├── Yes → Keep in .learnings/
└── No → Is it a compliance requirement?
    ├── Yes → Promote to compliance calendar or policy document
    └── No → Is it an onboarding pattern?
        ├── Yes → Promote to onboarding checklist
        └── No → Is it a recruiting insight?
            ├── Yes → Promote to recruiting playbook or interview scorecard
            └── No → Promote to AGENTS.md or general HR playbook
```

## HR-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Compliance audit finding | Log HR process issue | HR_PROCESS_ISSUES.md |
| I-9 verification issue | Log HR process issue with compliance_risk | HR_PROCESS_ISSUES.md |
| Benefits enrollment error | Log HR process issue | HR_PROCESS_ISSUES.md |
| Policy gap discovered | Log learning | LEARNINGS.md (policy_gap) |
| Candidate drops off | Log learning | LEARNINGS.md (candidate_experience) |
| New hire leaves <90 days | Log learning | LEARNINGS.md (retention_signal) |
| Exit interview theme | Log learning | LEARNINGS.md (retention_signal) |
| Onboarding delay | Log learning | LEARNINGS.md (onboarding_friction) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share an HR pattern with another session:
```
sessions_send(sessionKey="session-id", message="Compliance risk: I-9 re-verification missed for visa holders, configure HRIS alerts at 90/60/30 days")
```

### sessions_spawn

Spawn a background agent to analyze HR patterns:
```
sessions_spawn(task="Analyze .learnings/HR_PROCESS_ISSUES.md for promotion candidates", label="hr-pattern-review")
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
