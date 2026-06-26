# OpenClaw Integration

Complete setup and usage guide for integrating the conversation self-improvement skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Conversational context is injected from workspace files at session start, and hooks can trigger on lifecycle events to capture dialogue learnings.

## Workspace Structure

```
~/.openclaw/                      
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Dialogue workflows, escalation protocols, handoff procedures
│   ├── SOUL.md                 # Conversational personality, tone guidelines, empathy rules
│   ├── TOOLS.md                # Channel capabilities, integration gotchas, API limits
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── self-improving-conversation/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-conversation/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-conversation
```

Or copy manually:

```bash
cp -r self-improving-conversation ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-conversation
openclaw hooks enable self-improving-conversation
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Injected Prompt Files

### AGENTS.md

Purpose: Dialogue workflows, escalation chains, and handoff protocols.

```markdown
# Dialogue Coordination

## Escalation Protocol
- First escalation request: acknowledge and offer one more attempt
- Second request: initiate handoff immediately
- Never require more than 2 requests

## Multi-Turn Flow Management
- Maintain context summary across turns
- Checkpoint critical data (order ID, address, account)
- Confirm understanding before proceeding to next step
```

### SOUL.md

Purpose: Conversational personality, tone adaptation, empathy guidelines.

```markdown
# Conversational Personality

## Tone Adaptation
- Mirror user's formality level within 2 exchanges
- Match vocabulary complexity to user's language
- Use empathy markers when user shows frustration

## Honesty Policy
- Never fabricate facts, hours, prices, or policies
- Say "Let me check" when uncertain
- Correct errors immediately when discovered
```

### TOOLS.md

Purpose: Channel capabilities, integration limits, conversation constraints.

```markdown
# Channel Knowledge

## Web Chat
- Max message length: 2000 chars
- Supports rich formatting and links

## Slack
- Thread context may be lost after 50+ messages
- Emoji reactions as lightweight feedback signals

## Voice
- Keep responses under 30 seconds spoken
- Avoid complex lists; use sequential confirmation
```

## Learning Workflow

### Promotion Decision Tree

```
Is the learning conversation-specific to one user?
├── Yes → Keep in .learnings/
└── No → Is it about tone or personality?
    ├── Yes → Promote to SOUL.md
    └── No → Is it about channel limits or integration?
        ├── Yes → Promote to TOOLS.md
        └── No → Is it about dialogue flow or escalation?
            ├── Yes → Promote to AGENTS.md
            └── No → Keep in .learnings/ for now
```

### Promotion Format Examples

**From learning:**
> Slack threads lose context after ~50 messages. Agent started repeating questions.

**To TOOLS.md:**
```markdown
## Slack
- Thread context degrades after 50+ messages; summarize context periodically
```

## Detection Triggers

### Standard Conversation Triggers

| Signal | Log Target |
|--------|-----------|
| "That's not what I meant" | DIALOGUE_ISSUES.md (misunderstanding) |
| "Can I talk to a human?" | DIALOGUE_ISSUES.md (escalation_failure) |
| User rephrases 3+ times | LEARNINGS.md (misunderstanding) |
| Sentiment drops mid-conversation | LEARNINGS.md (sentiment_drift) |
| Agent states incorrect facts | LEARNINGS.md (hallucination) |
| Tone mismatch detected | LEARNINGS.md (tone_mismatch) |

### OpenClaw-Specific Triggers

| Trigger | Action |
|---------|--------|
| Channel integration error | Log to TOOLS.md with channel name |
| Handoff protocol confusion | Log to AGENTS.md with escalation pattern |
| Personality inconsistency | Log to SOUL.md with expected vs actual tone |
| Skill-related dialogue issue | Log to .learnings/ or report upstream |

## Verification

```bash
openclaw hooks list          # Check hook is registered
openclaw status              # Check skill is loaded
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
