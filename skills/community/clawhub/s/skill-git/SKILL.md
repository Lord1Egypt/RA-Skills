---
name: skill-git
description: Version control for AI agent skills. Use when the user wants to initialize, commit, revert, check, scan, or merge their skills. Triggers on: "init my skills", "track skills", "commit skill changes", "save skill snapshot", "new skill version", "revert skill", "roll back skill", "undo skill changes", "restore skill", "check skill conflicts", "validate skill", "scan skills", "find overlapping skills", "merge skills", "combine skills".
argument-hint: [init|commit|revert|check|scan|merge] [options]
---

skill-git is a version control system for AI agent skills. It gives each skill folder its own independent git history, tagged with semantic versions (v1.0.0, v1.1.0, …), so you can commit snapshots and revert to any previous version at any time.

Six commands are available:
- **init** — set up version tracking for all skills under an agent directory
- **commit** — snapshot changed skills with a version bump and commit message
- **revert** — roll back one or more skills to a previous version
- **check** — check a skill for internal rule conflicts, agent config conflicts, and security issues
- **scan** — scan registered skills for semantic overlap and get merge suggestions
- **merge** — merge two or more similar skills into one stronger, more complete skill

## Prerequisites

Before using any command, ensure these tools are installed:
- **git** — `git --version` (install: `brew install git` on macOS, `apt install git` on Linux)
- **jq** — `jq --version` (install: `brew install jq` on macOS, `apt install jq` on Linux)

The `init` command will check for `git` automatically. If `jq` is missing, `commit` and `revert` will fail when updating `config.json`.

## Intent Routing

Parse `$ARGUMENTS`. If `$ARGUMENTS` is empty, infer intent from the user's natural language message.

| Trigger | Action |
|---|---|
| `init` / "initialize" / "set up" / "track my skills" / "start tracking" | Read `$CLAW_SKILL_DIR/init.md` and follow it exactly |
| `commit` / "save" / "snapshot" / "new version" / "save skill changes" | Read `$CLAW_SKILL_DIR/commit.md` and follow it exactly |
| `revert` / "roll back" / "undo" / "restore" / "go back to" | Read `$CLAW_SKILL_DIR/revert.md` and follow it exactly |
| `check` / "check skill" / "validate skill" / "find conflicts" / "skill conflicts" | Read `$CLAW_SKILL_DIR/check.md` and follow it exactly |
| `scan` / "scan skills" / "find overlapping skills" / "which skills can I merge" | Read `$CLAW_SKILL_DIR/scan.md` and follow it exactly |
| `merge` / "merge skills" / "combine skills" / "consolidate skills" | Read `$CLAW_SKILL_DIR/merge.md` and follow it exactly |
| No args or ambiguous intent | Show the menu below and wait for user input |

### Menu (show only when intent is unclear)

```
skill-git — version control for your AI skills

Available commands:

  1. init      Set up version tracking for your skills
  2. commit    Snapshot changed skills with a new version
  3. revert    Roll back a skill to a previous version
  4. check     Check a skill for conflicts and security issues
  5. scan      Scan all skills for overlap and merge candidates
  6. merge     Merge two or more similar skills into one

Which would you like to run? (enter a number, name, or describe what you want)
```

Wait for the user's response, then route to the appropriate `.md` file above.

## Asset Skills

The `check`, `scan`, and `merge` commands depend on two internal library skills located in `assets/`:
- `assets/rule-extraction/SKILL.md` — extracts structured rule lists from skill markdown files
- `assets/conflict-patterns/SKILL.md` — detects conflicts between two rule lists (direct contradiction, semantic contradiction, overlap, security patterns)
