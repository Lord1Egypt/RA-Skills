---
name: vibe-coding-skills-installer
description: >-
  Install vibe coding skill sets (openspec, gstack, superpowers) for any
  supported agent platform (Cursor, Claude Code, Codex, etc.). Interactively
  asks about target platform, install scope, and configuration options.
  Use when the user wants to install, setup, or configure openspec, gstack,
  superpowers, or vibe coding skills.
---

# Vibe Coding Skills Installer

A cross-platform installer for three curated skill sets: **OpenSpec**, **gstack**, and **Superpowers**.

## Installing this skill

This skill itself can be placed in either location:

- **Project-level** (recommended for teams): copy or clone into `<project>/.cursor/skills/vibe-coding-skills-installer/` (or the equivalent directory for your platform). The skill travels with the repo and is available to all contributors.
- **Global**: copy or clone into `~/.cursor/skills/vibe-coding-skills-installer/` (or the equivalent). The skill is available across all your projects.

Platform auto-detection works identically for both locations — the path substring `/.cursor/` (or `/.claude/`, `/.agents/`, etc.) appears in either case.

## Workflow

Follow these five steps in order. Use AskQuestion (or conversational prompts if unavailable) at each decision point.

---

### Step 1 — Detect or confirm the agent platform

Determine which coding agent is running. Try automatic detection first, then fall back to asking.

**Auto-detection**: check the directory from which this skill was loaded. This works whether the skill is installed globally (`~/.cursor/skills/...`) or at project level (`.cursor/skills/...`):
- Path contains `/.cursor/` -> **cursor**
- Path contains `/.claude/` -> **claude**
- Path contains `/.agents/` -> **codex**
- Path contains `/.windsurf/` -> **windsurf**
- Path contains `/.gemini/` -> **gemini**
- Path contains `/.opencode/` -> **opencode**

If detection fails, ask the user:

```
Which agent platform are you using?
- Cursor
- Claude Code
- Codex (OpenAI)
- Other (specify manually)
```

Store the result as `$HOST`. Resolve directory paths from [platforms.md](platforms.md):
- `$GLOBAL_SKILLS` — user-level skills directory (e.g. `~/.cursor/skills/`)
- `$PROJECT_SKILLS` — project-level skills directory (e.g. `.cursor/skills/`)

---

### Step 2 — Choose skill sets to install

Ask the user which skill sets to install (allow multiple selections):

```
Which skill sets would you like to install?
- OpenSpec    — Spec-driven development framework (CLI + workflow skills)
- gstack      — 23 specialized role skills by Garry Tan (CEO, designer, eng manager, etc.)
- Superpowers — Core skills library (TDD, debugging, collaboration patterns) by obra
```

---

### Step 3 — Choose install scope for each selected skill set

For each selected skill set, ask the user about the desired scope.

#### OpenSpec scope options

```
How would you like to install OpenSpec?
- CLI only          — Install the openspec CLI globally (npm install -g)
- CLI + project     — Also run `openspec init` in the current project
- CLI + project + workflow skills — Also install workflow skills into the project
```

#### gstack scope options

```
How would you like to install gstack?
- Global only        — Install to $GLOBAL_SKILLS/gstack/
- Project only       — Install to $PROJECT_SKILLS/gstack/ (travels with the repo)
- Global + team mode — Global install + configure the current project for team auto-updates
```

#### Superpowers scope options

```
How would you like to install Superpowers?
- Global  — Plugin (Cursor/Claude Code) or git clone to $GLOBAL_SKILLS/superpowers/
- Project — git clone to $PROJECT_SKILLS/superpowers/ (travels with the repo)
```

For Cursor and Claude Code, the **global** option uses the native plugin system:
- Cursor: `/add-plugin superpowers`
- Claude Code: `/plugin install superpowers@claude-plugins-official`

The **project** option always uses git clone regardless of platform.

---

### Step 4 — Check prerequisites and execute

Run the helper script to check the environment. `$SKILL_ROOT` is the directory containing this SKILL.md file:

```bash
bash $SKILL_ROOT/scripts/install.sh --host $HOST --check
```

Read the output. If any required dependency is missing, inform the user and suggest how to install it before proceeding.

Then execute each selected installation. Run them one at a time and verify each before moving on.

#### Install OpenSpec

```bash
# Always: install CLI
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install openspec --scope global

# If scope includes project init:
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install openspec --scope project

# If scope includes workflow skills:
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install openspec --scope workflows
```

#### Install gstack

```bash
# Global install
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install gstack --scope global

# Project install (into current project's skills dir)
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install gstack --scope project

# If team mode (requires global install first):
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install gstack --scope team
```

#### Install Superpowers

```bash
# Global install (for Codex/others; Cursor and Claude Code will get an agent_action hint)
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install superpowers --scope global

# Project install (git clone into project skills dir, works on all platforms)
bash $SKILL_ROOT/scripts/install.sh --host $HOST --install superpowers --scope project
```

After each installation step, verify:

```bash
bash $SKILL_ROOT/scripts/install.sh --host $HOST --verify
```

---

### Step 5 — Post-install summary

Present a summary table to the user:

```
Installation complete!

| Skill Set    | Status | Location                        | Getting Started         |
|--------------|--------|---------------------------------|-------------------------|
| OpenSpec     | ...    | CLI: openspec / Skills: ...     | Run `openspec init`     |
| gstack       | ...    | ~/.xxx/skills/gstack/           | Try `/office-hours`     |
| Superpowers  | ...    | Plugin / ~/.xxx/skills/...      | Ask "Do you have superpowers?" |
```

If any installation failed, explain the error and suggest a manual fix.

---

## Reference

- Platform directory conventions: [platforms.md](platforms.md)
- Install helper script: [scripts/install.sh](scripts/install.sh)
