# OpenClaw Integration

Complete setup and usage guide for integrating `self-optimization` with OpenClaw.

## Overview

OpenClaw is a strong fit for this skill because it supports both:

- workspace prompt files for durable guidance
- event-driven hooks for lightweight reminders

Together, those make it easier to turn single-session lessons into repeatable operating rules.

## Install

### ClawdHub

```bash
clawdhub install self-optimization
```

### Manual

```bash
cp -r self-optimization ~/.openclaw/skills/
```

## Optional Hook

Copy the provided hook:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-optimization
```

Enable it:

```bash
openclaw hooks enable self-optimization
```

## Workspace Layout

```text
~/.openclaw/
├── workspace/
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── MEMORY.md
│   ├── memory/
│   └── .learnings/
│       ├── LEARNINGS.md
│       ├── ERRORS.md
│       └── FEATURE_REQUESTS.md
├── skills/
│   └── self-optimization/
└── hooks/
    └── self-optimization/
```

## Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Or create them inside the installed skill area if your setup prefers that layout:

```bash
mkdir -p ~/.openclaw/skills/self-optimization/.learnings
```

## Promotion Model

Use `.learnings/` as the inbox, then promote stable patterns into workspace guidance:

| Source Signal | Best Target |
|---------------|-------------|
| Repo conventions and recurring project facts | `CLAUDE.md` |
| Workflow improvements and delegation rules | `AGENTS.md` |
| Tool quirks, auth steps, environment gotchas | `TOOLS.md` |
| Behavioral and communication principles | `SOUL.md` |

## Cross-Session Usage

When a learning should survive or spread across sessions:

1. Record the detailed incident in `.learnings/`.
2. Distill it into a short rule.
3. Promote it into the correct workspace file.
4. Optionally send it to another active session if the task is already in flight.

## Verification

Check the hook:

```bash
openclaw hooks list
```

Check the workspace and loaded skills:

```bash
openclaw status
```

## Troubleshooting

### Hook does not fire

1. Confirm the hook was copied into `~/.openclaw/hooks/self-optimization`
2. Confirm it is enabled
3. Restart or reload the OpenClaw environment if needed

### Learnings do not persist

1. Confirm `.learnings/` exists
2. Confirm write permissions
3. Confirm your workspace path is the one OpenClaw is actually using

### Skill does not load

1. Confirm the folder name is `self-optimization`
2. Confirm `SKILL.md` frontmatter uses `name: self-optimization`
3. Recheck `openclaw status`
