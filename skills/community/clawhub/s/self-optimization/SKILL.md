---
name: self-optimization
description: "Turn mistakes, corrections, dead ends, and repeated fixes into durable improvements. Use when work reveals a non-obvious lesson, a recurring failure, a missing capability, or a rule that should be promoted into agent memory, workflow guidance, or a reusable skill."
metadata:
---

# Self-Optimization

Use this skill to close the loop after real work. The goal is not just to log what went wrong. The goal is to convert signal from mistakes, corrections, and repeated effort into stronger future behavior.

## Core Loop

1. Detect meaningful signal.
2. Capture it in `.learnings/`.
3. De-duplicate and link related entries.
4. Promote stable patterns into durable guidance.
5. Extract reusable skills when the pattern is broad and proven.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command, tool, or integration fails unexpectedly | Append an entry to `.learnings/ERRORS.md` |
| User corrects the agent or provides missing facts | Append an entry to `.learnings/LEARNINGS.md` |
| A better repeatable approach is discovered | Append an entry to `.learnings/LEARNINGS.md` |
| User asks for a missing capability | Append an entry to `.learnings/FEATURE_REQUESTS.md` |
| Same issue keeps reappearing | Link entries, bump priority, and consider promotion |
| Pattern is stable across tasks | Promote to `AGENTS.md`, `CLAUDE.md`, `TOOLS.md`, `SOUL.md`, or `.github/copilot-instructions.md` |
| Pattern is reusable beyond one repo | Extract a new skill scaffold |

## Detection Triggers

Capture a learning when any of these happen:

- The first attempt was wrong and needed correction.
- A tool or command failed in a non-obvious way.
- The user revealed a project convention that was not documented.
- The agent discovered a stronger pattern than the one it started with.
- The same workaround or warning has appeared more than once.
- The user asked for a capability the current system does not provide.

Skip noisy one-off trivia. Capture things that would realistically save a future session time, confusion, or rework.

## Log Files

Create a local `.learnings/` directory in the workspace or in the OpenClaw workspace.

```text
.learnings/
├── LEARNINGS.md
├── ERRORS.md
└── FEATURE_REQUESTS.md
```

### `LEARNINGS.md`

Use for:

- corrections
- knowledge gaps
- best practices
- project conventions
- improved workflows

Template:

````markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: 2026-04-01T10:00:00Z
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line statement of the lesson.

### Details
What was wrong, what changed, and what is now known to be correct.

### Suggested Action
What to do differently next time.

### Metadata
- Source: conversation | debugging | user_feedback | simplify-and-harden
- Related Files: path/to/file
- Tags: tag-a, tag-b
- See Also: LRN-20260401-001
- Pattern-Key: optional.stable.key
- Recurrence-Count: 1
- First-Seen: 2026-04-01
- Last-Seen: 2026-04-01

---
````

### `ERRORS.md`

Use for:

- command failures
- exceptions
- bad tool assumptions
- API or integration breakage

Template:

````markdown
## [ERR-YYYYMMDD-XXX] command_or_tool

**Logged**: 2026-04-01T10:00:00Z
**Priority**: medium
**Status**: pending
**Area**: backend | infra | tests | docs | config

### Summary
Short description of the failure.

### Error
```text
Actual error output goes here.
```

### Context
- Command or action attempted
- Relevant inputs
- Environment details if useful

### Suggested Fix
What should be tried next or documented.

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file
- See Also: ERR-20260401-001

---
````

### `FEATURE_REQUESTS.md`

Use for:

- missing tooling
- automation requests
- product gaps
- missing agent behaviors

Template:

````markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: 2026-04-01T10:00:00Z
**Priority**: low | medium | high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted.

### User Context
Why they wanted it.

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How it might be built or extended.

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature

---
````

## ID Format

Use `TYPE-YYYYMMDD-XXX`.

- `LRN` for learning
- `ERR` for error
- `FEAT` for feature request

Examples:

- `LRN-20260401-001`
- `ERR-20260401-002`
- `FEAT-20260401-003`

## Promotion Rules

Promote an entry when it becomes more valuable as guidance than as a historical note.

| Target | Promote When |
|--------|---------------|
| `CLAUDE.md` | Project facts, conventions, or recurring gotchas |
| `AGENTS.md` | Workflow rules, delegation patterns, automation steps |
| `.github/copilot-instructions.md` | Repo guidance that should reach Copilot |
| `TOOLS.md` | Tool quirks, auth requirements, environment gotchas |
| `SOUL.md` | Behavioral or communication rules for OpenClaw sessions |

Promotion checklist:

1. Distill the learning into a short prevention rule.
2. Add it to the right target file.
3. Update the original entry status to `promoted`.
4. Record where it was promoted.

## Recurrence And Dedupe

Before creating a new entry for a familiar issue:

1. Search `.learnings/` for a related keyword or `Pattern-Key`.
2. If a related item exists, link it with `See Also`.
3. Increase `Recurrence-Count` and refresh `Last-Seen`.
4. Escalate priority if the pattern is recurring and costly.

Recurring issues often mean one of three things:

- documentation is missing
- automation is missing
- the architecture or workflow is inviting the same failure

## When To Extract A Skill

Extract a reusable skill when the pattern is:

- resolved and trustworthy
- useful across multiple tasks
- non-obvious enough to justify explicit guidance
- portable beyond a single private incident

Use the helper:

```bash
./skills/self-optimization/scripts/extract-skill.sh my-new-skill --dry-run
./skills/self-optimization/scripts/extract-skill.sh my-new-skill
```

Then customize the generated `SKILL.md` and update the original learning entry with:

- `Status: promoted_to_skill`
- `Skill-Path: skills/my-new-skill`

## Review Rhythm

Review `.learnings/` at these checkpoints:

- before major tasks
- after finishing a feature or bugfix
- when working in an area with previous failures
- during periodic maintenance

Useful checks:

```bash
grep -h "Status\\*\\*: pending" .learnings/*.md | wc -l
grep -B5 "Priority\\*\\*: high" .learnings/*.md | grep "^## \\["
grep -l "Area\\*\\*: backend" .learnings/*.md
```

## OpenClaw Setup

OpenClaw works especially well with this skill because workspace files and hooks let the improvement loop stay visible between sessions.

### Install

```bash
clawdhub install self-optimization
```

Manual install:

```bash
git clone <your-fork-or-source-repo> ~/.openclaw/skills/self-optimization
```

This package is an OpenClaw-oriented evolution of the earlier self-learning workflow.

### Hook Setup

Optional bootstrap reminder:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-optimization
openclaw hooks enable self-optimization
```

### Workspace Layout

```text
~/.openclaw/workspace/
├── AGENTS.md
├── SOUL.md
├── TOOLS.md
├── MEMORY.md
├── memory/
└── .learnings/
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

## Hook Support For Other Agents

### Claude Code / Codex

Use hook scripts in settings:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-optimization/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-optimization/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### GitHub Copilot

Add a reminder to `.github/copilot-instructions.md`:

```markdown
## Self-Optimization

After solving non-obvious issues, consider:
1. Logging the lesson to `.learnings/`
2. Linking related recurring entries
3. Promoting stable rules into repo guidance
4. Extracting reusable skills when the pattern is broad
```

## Best Practices

1. Log signal, not noise.
2. Prefer prevention rules over postmortems.
3. Link related incidents instead of duplicating them.
4. Promote broadly useful guidance quickly.
5. Treat repeated friction as a systems problem, not just a note-taking problem.
6. Review learnings before repeating the same class of work.
