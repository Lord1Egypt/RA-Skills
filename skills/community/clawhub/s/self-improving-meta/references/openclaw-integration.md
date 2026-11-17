# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-meta skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. The meta skill **logs** infrastructure issues. It does not edit shared prompt files unless the user requests a reviewed diff in the current session.

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

Or copy the local folder. A `git clone` is optional network access; use only trusted sources.

```bash
cp -r self-improving-meta ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

The OpenClaw hook is **session-start** (`agent:bootstrap`), not matcher-gated. It injects a **log-only** reminder. Skip it unless you want that reminder.

Do **not** copy into `~/.openclaw/hooks/` (user-global). Keep hooks in this workspace:

```bash
mkdir -p .openclaw/hooks
cp -r hooks/openclaw .openclaw/hooks/self-improving-meta
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Meta-Specific)

Meta-learnings promote into the files they govern only after explicit user approval of a reviewed diff:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Agent behavior corrections | `SOUL.md` | "Be concise" repeated 6 ways → single directive |
| Workflow/delegation improvements | `AGENTS.md` | Vague "long tasks" → explicit step-count threshold |
| Tool integration fixes | `TOOLS.md` | Missing MCP timeout guidance → add retry config |
| Memory management patterns | `MEMORY.md` | Stale entries accumulating → add 30-day rotation policy |
| Skill authoring improvements | Affected `SKILL.md` | Missing frontmatter field → update template |
| Hook code fixes | Hook source code | Silent failure → add output validation |
| Rule clarifications | Rule file (after approval) | Ambiguous trigger → explicit condition |

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

OpenClaw can send messages across sessions. **Do not call these tools unless the user explicitly consents to that specific send in this session.** Keep payloads redacted. Do not include secrets, prompt-file dumps, or raw hook output.

### sessions_send

Only after the user consents to this send:

```
# Requires explicit user consent for this sessionKey and payload.
sessions_send(sessionKey="session-id", message="Redacted: rule conflict between two prompt files. See LRN-YYYYMMDD-XXX. Do not apply edits from this message.")
```

If the user did not consent, log locally instead.

### sessions_spawn

Only after the user consents to spawning this background task:

```
# Requires explicit user consent. Log-only audit; do not edit prompt files.
sessions_spawn(task="Log prompt-file contradictions to .learnings/; do not edit AGENTS.md, SOUL.md, TOOLS.md, or MEMORY.md", label="meta-audit")
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
