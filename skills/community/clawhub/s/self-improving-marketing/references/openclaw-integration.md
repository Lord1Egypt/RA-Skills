# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-marketing skill with OpenClaw.

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
│   └── self-improving-marketing/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-marketing/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-marketing
```

Or copy manually:

```bash
cp -r self-improving-marketing ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-marketing
openclaw hooks enable self-improving-marketing
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Marketing-Specific)

When marketing learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Messaging patterns | Brand guidelines | "Enterprise segment: lead with ROI, not ease-of-use" |
| Channel insights | Channel playbooks | "LinkedIn carousel outperforms single-image 3x for B2B" |
| Audience shifts | Audience personas | "ICP shifted from SMB founders to mid-market VPs" |
| Content patterns | Content calendar | "Publish comparison posts after competitor launches" |
| Attribution fixes | Attribution model | "Server-side UTM capture as backup for redirect chains" |
| Tool configurations | `TOOLS.md` | "Warm new sending domains 14 days minimum" |

### Promotion Decision Tree

```
Is the learning campaign-specific?
├── Yes → Keep in .learnings/
└── No → Is it a messaging/brand pattern?
    ├── Yes → Promote to brand guidelines
    └── No → Is it a channel optimization?
        ├── Yes → Promote to channel playbook
        └── No → Is it an audience insight?
            ├── Yes → Update audience personas
            └── No → Promote to TOOLS.md or AGENTS.md
```

## Marketing-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| CTR drop detected | Log campaign issue | CAMPAIGN_ISSUES.md |
| Conversion rate decline | Log campaign issue with funnel data | CAMPAIGN_ISSUES.md |
| Email bounce spike | Log campaign issue with deliverability data | CAMPAIGN_ISSUES.md |
| Messaging missed segment | Log learning | LEARNINGS.md (messaging_miss) |
| Channel below benchmark | Log learning | LEARNINGS.md (channel_underperformance) |
| Audience behavior shifted | Log learning | LEARNINGS.md (audience_drift) |
| Brand violation found | Log learning | LEARNINGS.md (brand_inconsistency) |
| Attribution broken | Log learning | LEARNINGS.md (attribution_gap) |
| Content traffic declining | Log learning | LEARNINGS.md (content_decay) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a marketing insight with another session:
```
sessions_send(sessionKey="session-id", message="Attribution gap: Cloudflare redirect strips UTMs, use $1?$query_string in redirect rule")
```

### sessions_spawn

Spawn a background agent to analyze campaign patterns:
```
sessions_spawn(task="Analyze .learnings/CAMPAIGN_ISSUES.md for promotion candidates", label="campaign-review")
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
