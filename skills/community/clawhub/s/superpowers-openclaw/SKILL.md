---
name: superpowers-open
description: >
  Complete Superpowers methodology for OpenClaw. A 12-skill collection that enforces design-before-code, TDD, systematic debugging, verification, and structured code review. Use when you want rigorous AI-assisted development workflow.
metadata:
  openclaw:
    emoji: "⚡"
    homepage: https://github.com/superpowers-open/superpowers-open
---

# SuperpowersOpen

Superpowers 方法论在 OpenClaw 平台上的完整技能集合。12 个技能协同工作，形成端到端的严格开发工作流。

## How This Collection Works

This is a **skill collection**. The root SKILL.md acts as the manifest. Individual skills live in subdirectories and are auto-discovered by OpenClaw via their `description` fields.

## Skills

### Entry Point
- **using-superpowers-open** — Tool mapping, trigger coordination, instruction priority (always active)

### Workflow Chain
- **brainstorming** — Design-first: no code before design approval
- **writing-plans** — Decompose designs into bite-sized implementation tasks
- **executing-plans** — Load plan, execute tasks inline, verify completion
- **finishing-a-development-branch** — Structured merge/PR/keep/discard workflow

### Practice Disciplines
- **test-driven-development** — RED-GREEN-REFACTOR: test first, watch it fail, minimal code
- **systematic-debugging** — 4-phase debugging: root cause → pattern → hypothesis → fix
- **verification-before-completion** — Evidence before claims, always
- **receiving-code-review** — Verify before implementing, no performative agreement
- **requesting-code-review** — 5-dimension self-review checklist
- **writing-skills** — TDD methodology applied to skill documentation
- **using-git-worktrees** — Isolated git worktree workspaces

## Installation

```bash
cp -r superpowers-open ~/.openclaw/skills/
```

Restart OpenClaw Gateway. All 12 skills are auto-discovered.

## Requirements

- OpenClaw (any version supporting SKILL.md format)
- No additional dependencies

## License

MIT-0

## Credits

Adapted from [obra/superpowers](https://github.com/obra/superpowers) methodology.
