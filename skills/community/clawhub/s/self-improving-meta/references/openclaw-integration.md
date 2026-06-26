# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-meta skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events. The meta skill is unique: it monitors and improves the very infrastructure that OpenClaw and other skills depend on.

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
│   └── self-improving-meta/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-meta/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-meta
```

Or copy manually:

```bash
cp -r self-improving-meta ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-meta
openclaw hooks enable self-improving-meta
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Meta-Specific)

Meta-learnings promote directly into the files they govern:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Agent behavior corrections | `SOUL.md` | "Be concise" repeated 6 ways → single directive |
| Workflow/delegation improvements | `AGENTS.md` | Vague "long tasks" → explicit step-count threshold |
| Tool integration fixes | `TOOLS.md` | Missing MCP timeout guidance → add retry config |
| Memory management patterns | `MEMORY.md` | Stale entries accumulating → add 30-day rotation policy |
| Skill authoring improvements | Affected `SKILL.md` | Missing frontmatter field → update template |
| Hook code fixes | Hook source code | Silent failure → add output validation |
| Rule clarifications | Rule file directly | Ambiguous trigger → explicit condition |

### Promotion Decision Tree

```
Is it about agent behavior or personality?
├── Yes → Promote to SOUL.md
└── No → Is it about workflows or delegation?
    ├── Yes → Promote to AGENTS.md
    └── No → Is it about tool usage or integration?
        ├── Yes → Promote to TOOLS.md
        └── No → Is it about memory management?
            ├── Yes → Promote to MEMORY.md
            └── No → Is it about a specific skill?
                ├── Yes → Update that skill's SKILL.md
                └── No → Is it about hooks?
                    ├── Yes → Update hook code + HOOK.md
                    └── No → Is it about rules?
                        ├── Yes → Update the rule file directly
                        └── No → Log as feature request
```

## Meta-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Agent ignores a prompt file rule | Log learning | LEARNINGS.md (instruction_ambiguity) |
| Two files give contradictory guidance | Log learning | LEARNINGS.md (rule_conflict) |
| Context window truncated or cramped | Log learning | LEARNINGS.md (context_bloat) |
| Memory entry references deleted file | Log learning | LEARNINGS.md (prompt_drift) |
| Hook produces no output | Log meta issue | META_ISSUES.md (hook_failure) |
| Skill doesn't activate on matching trigger | Log meta issue | META_ISSUES.md (skill_gap) |
| Frontmatter malformed or missing fields | Log meta issue | META_ISSUES.md |
| New infrastructure capability needed | Log feature request | FEATURE_REQUESTS.md |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share an infrastructure finding with another session:
```
sessions_send(sessionKey="session-id", message="Rule conflict: CLAUDE.md says pnpm, AGENTS.md says npm. Authoritative source: CLAUDE.md.")
```

### sessions_spawn

Spawn a background agent to audit prompt files:
```
sessions_spawn(task="Audit all prompt files for contradictions and context bloat", label="meta-audit")
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
