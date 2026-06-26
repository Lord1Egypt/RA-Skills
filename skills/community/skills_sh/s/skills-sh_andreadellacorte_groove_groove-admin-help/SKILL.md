---
name: groove-admin-help
description: "Display all groove skills and commands with live config values."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-help

Display a structured overview of all groove skills and their commands.

## Output

Print the following, substituting live config values from `.groove/index.md` where shown:

---

**groove** — compound engineering workflow

```
/groove   /groove-admin-help   /groove-utilities-prime   /groove-admin-install   /groove-admin-config   /groove-admin-update   /groove-utilities-check   /groove-utilities-stats   /groove-admin-doctor
```

**Daily**

| Skill | Purpose |
|---|---|
| `/groove-daily-start` | Start the workday |
| `/groove-daily-end` | End the workday |

**Work**

| Skill | Purpose |
|---|---|
| `/groove-work-brainstorm` | Clarify scope through dialogue |
| `/groove-work-plan` | Write implementation plan |
| `/groove-work-exec` | Execute the plan |
| `/groove-work-review` | Evaluate output |
| `/groove-work-compound` | Capture lessons |
| `/groove-work-spec [topic]` | Create outcome spec (what to build) |
| `/groove-work-doc [topic]` | Create reference doc (how it works) |
| `/groove-work-audit` | Review branch for blindspots |

**Utilities — Tasks**

| Skill | Purpose |
|---|---|
| `/groove-utilities-task-list` | List active tasks |
| `/groove-utilities-task-create` | Create a task |
| `/groove-utilities-task-update` | Update a task |
| `/groove-utilities-task-archive` | Archive a task |
| `/groove-utilities-task-analyse` | Analyse task status |
| `/groove-utilities-task-install` | Set up task backend |
| `/groove-utilities-task-config` | Configure task backend |
| `/groove-utilities-task-doctor` | Check task backend health |

**Utilities — Memory**

| Skill | Purpose |
|---|---|
| `/groove-utilities-memory-log-daily` | Write daily log entry |
| `/groove-utilities-memory-log-weekly` | Roll up weekly log |
| `/groove-utilities-memory-log-monthly` | Roll up monthly log |
| `/groove-utilities-memory-log-git` | Record git activity |
| `/groove-utilities-memory-install` | Set up memory backend |
| `/groove-utilities-memory-doctor` | Check memory backend health |
| `/groove-utilities-memory-mistakes` | Log and resolve a workflow mistake |
| `/groove-utilities-memory-promises` | Capture or resolve a deferred item |
| `/groove-utilities-memory-retrospective [week\|month\|all]` | Analyse ratings, mistakes, learnings |
| `/groove-utilities-memory-graduate [topic]` | Promote a stable lesson to AGENTS.md |

**Utilities — Session**

| Skill | Purpose |
|---|---|
| `/groove-utilities-prime` | Load workflow context into conversation |
| `/groove-utilities-check` | Check if a newer version is available |
| `/groove-utilities-stats` | Compound-loop metrics dashboard |
| `/groove-utilities-onboard` | Generate GROOVE.md onboarding guide for contributors |

**Admin**

| Skill | Purpose |
|---|---|
| `/groove-admin-install` | Install backends and bootstrap AGENTS.md |
| `/groove-admin-config` | Create or update `.groove/index.md` |
| `/groove-admin-update` | Pull latest and apply migrations |
| `/groove-admin-help` | Show this help |
| `/groove-admin-doctor` | Run all health checks |
| `/groove-admin-claude-hooks` | Install Claude Code native shell hooks into `.claude/settings.json` |
| `/groove-admin-cursor-hooks` | Install Cursor native hooks into `.cursor/hooks.json` |

**Groovebook** *(only shown if `groovebook:` is set in `.groove/index.md`)*

| Skill | Purpose |
|---|---|
| `/groove-groovebook-publish` | Publish a workflow learning as a PR |
| `/groove-groovebook-review` | Browse and review open learning PRs |

**Config** (`.groove/index.md`)

```
tasks.backend:       <value>   — task backend (beans | linear | github | none)
tasks.list_limit:    <value>   — max tasks in task-list (default 15)
tasks.analyse_limit: <value>   — max tasks in task-analyse (default 30)
memory.review_days:  <value>   — business days to review at daily start (default 5)
memory path:         .groove/memory/ (hardcoded)
specs path:          .groove/memory/specs/ (hardcoded)
git.memory:          <value>   — memory commit strategy (ignore-all | hybrid | commit-all)
git.tasks:           <value>   — tasks commit strategy (ignore-all | commit-all)
git.hooks:           <value>   — hooks commit strategy (ignore-all | commit-all)
groovebook:          <value>   — shared learning commons repo (optional)
```

---

## Constraints

- Read `.groove/index.md` and substitute actual configured values into the config block
- If `.groove/index.md` does not exist, show defaults and note that config has not been created yet
- Keep output concise — this is a quick-reference, not a manual
