# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-coding skill with OpenClaw.

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
│   └── self-improving-coding/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-coding/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-coding
```

Or copy manually:

```bash
cp -r self-improving-coding ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-coding
openclaw hooks enable self-improving-coding
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Coding-Specific)

When coding learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Code style patterns | Style guide | "Always use early returns over nested if/else" |
| Recurring lint fixes | Lint rules | "Disallow mutable default arguments (B006)" |
| Reusable solutions | Code snippets library | "Retry with exponential backoff template" |
| Debugging workflows | Debug playbooks | "Race condition diagnosis in async code" |
| Tool configuration | `TOOLS.md` | "Enable strictNullChecks in tsconfig" |
| Workflow patterns | `AGENTS.md` | "Run type checker before committing" |

### Promotion Decision Tree

```
Is the learning project-specific?
├── Yes → Keep in .learnings/
└── No → Is it a code style/convention?
    ├── Yes → Promote to style guide or lint rule
    └── No → Is it a debugging technique?
        ├── Yes → Promote to debug playbook
        └── No → Is it a reusable pattern?
            ├── Yes → Promote to code snippets library
            └── No → Promote to TOOLS.md or AGENTS.md
```

## Coding-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Lint error detected | Log bug pattern | BUG_PATTERNS.md |
| Type checker error | Log bug pattern with type details | BUG_PATTERNS.md |
| Runtime exception | Log bug pattern with stack trace | BUG_PATTERNS.md |
| Anti-pattern discovered | Log learning | LEARNINGS.md (anti_pattern) |
| Better idiom found | Log learning | LEARNINGS.md (idiom_gap) |
| Debugging breakthrough | Log learning | LEARNINGS.md (debugging_insight) |
| Tooling issue hit | Log learning | LEARNINGS.md (tooling_issue) |
| Refactoring opportunity | Log learning | LEARNINGS.md (refactor_opportunity) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a coding pattern with another session:
```
sessions_send(sessionKey="session-id", message="Bug pattern: off-by-one in pagination, use (page-1)*size not page*size")
```

### sessions_spawn

Spawn a background agent to analyze code patterns:
```
sessions_spawn(task="Analyze .learnings/BUG_PATTERNS.md for promotion candidates", label="pattern-review")
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
