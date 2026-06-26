---
name: workspace-project-standard
description: "Project workspace setup and documentation standard for OpenClaw agents. Enforces a three-layer documentation system and self-contained project structure. Triggers when: (1) starting a new project (new project, create project, 新项目, 开始项目), (2) organizing an existing workspace (clean up workspace, 整理项目, 规范目录), (3) creating project documentation (create project docs, 建项目文档). Ensures all project work stays within its own directory, temp files never pollute the workspace root, and documentation is always maintained alongside code."
---

# Workspace Project Standard

Enforce a self-contained project structure with three-layer documentation.

## Directory Rules

| Directory | Contains | Never contains |
|-----------|----------|----------------|
| `workspace/<name>/` | Code, scripts, config | Notes, AI records |
| `workspace/<name>/tmp/` | Temp files, experiments | Long-term files |
| `workspace/projects/<name>/` | AI records (md only) | Code, scripts |
| `workspace/` root | System files only | Project files |

**Principle: projects are self-contained.** All output stays inside `workspace/<name>/`.

## Starting a New Project

Run the scaffold script, then fill in the templates:

```powershell
# Creates full directory structure in one command
scripts/new-project.ps1 -Name "<project-name>"
```

Then:
1. Fill in `projects/<name>/<name>.md` using `assets/project-template.md`
2. Fill in `projects/<name>/LINKS.md` using `assets/links-template.md`
3. Add one row to MEMORY.md project table
4. Add `workspace/<name>/` to root whitelist in AGENTS.md

## Three-Layer Documentation

**Layer 1 — MEMORY.md** (one-line summary per project)
```
| 🚧 | <name> | `projects/<name>/` | <description> |
```
Update when a major capability is added.

**Layer 2 — `projects/<name>/<name>.md`** (project master doc)
Required sections: `## 当前进展` `## 关键信息` `## 关键文件路径` `## 文档归档` `## 待用户输入` `## 历史记录`

**Layer 3 — `projects/<name>/LINKS.md`** (links & paths index)
Required: all online URLs, local file tree, credentials reference, run parameters, common commands.

See `assets/project-template.md` and `assets/links-template.md` for fill-in templates.

## Update Triggers

| Event | Update |
|-------|--------|
| New service / API connected | Layer 2 关键信息 + Layer 3 |
| New file created | Layer 2 关键文件路径 + Layer 3 |
| Major feature complete | Layer 1 + Layer 2 进展 + 历史记录 |
| Path / config changed | Layer 2 + Layer 3 in sync |

## Workspace Root Whitelist

Only these may exist in `workspace/` root:

**System files:** `AGENTS.md` `SOUL.md` `MEMORY.md` `CREDENTIALS.md` `HEARTBEAT.md` `SESSION-STATE.md` `IDENTITY.md` `USER.md` `CODING-PERSONA.md` `TOOLS.md` `.env` `package.json` `package-lock.json`

**System dirs:** `memory/` `projects/` `scripts/` `backups/` `captures/` `config-backups/` `tmp/` `skills/` `node_modules/` `.agents/` `.clawhub/` `.openclaw/` `.pi/`

Any file not on this list → move to its project's `tmp/` immediately.
