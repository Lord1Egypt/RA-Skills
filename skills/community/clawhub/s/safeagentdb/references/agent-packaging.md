# Optional Agent Packaging

SafeAgentDB's primary install path is this skill. The core setup lives in `SKILL.md` plus bundled references and templates.

After installation, users may also choose to add persistent agent guidance so future agents know how to maintain the infrastructure.

## Publishable Skill Location

For `npx skills add Aidan945/SafeAgentDB`, keep the canonical skill at:

```text
skills/safeagentdb/SKILL.md
```

The `skills` CLI discovers `SKILL.md` files at the repository root and under top-level skill container folders such as `skills/` and `.agents/skills/`.

## Recommendation

Use two layers:

1. **Always-on project instructions** for safety rules that should apply every session.
2. **Optional skill** for the reusable setup/maintenance workflow.

## Cursor

Cursor supports project skills in:

```text
.cursor/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
```

Recommended project install:

```text
.cursor/skills/safeagentdb/SKILL.md
```

Alternative cross-agent install:

```text
.agents/skills/safeagentdb/SKILL.md
```

Use the template:

```text
skills/safeagentdb/SKILL.md
```

Cursor also supports project rules/instructions. If the user wants always-on guidance, add the relevant rules from:

```text
templates/agent-instructions/AGENTS.md
```

to their project instruction convention.

## Codex

Codex supports:

```text
AGENTS.md
.agents/skills/<skill-name>/SKILL.md
~/.agents/skills/<skill-name>/SKILL.md
```

Recommended repo install:

```text
AGENTS.md
.agents/skills/safeagentdb/SKILL.md
```

Use:

```text
templates/agent-instructions/AGENTS.md
skills/safeagentdb/SKILL.md
```

`AGENTS.md` is always-on project guidance. The skill is loaded on demand when Codex decides the task matches its description or when explicitly invoked.

## Claude Code

Claude Code supports project skills in:

```text
.claude/skills/<skill-name>/SKILL.md
```

and project instructions in:

```text
CLAUDE.md
.claude/CLAUDE.md
```

Recommended project install:

```text
CLAUDE.md
.claude/skills/safeagentdb/SKILL.md
```

Use:

```text
templates/agent-instructions/CLAUDE.md
skills/safeagentdb/SKILL.md
```

## Cross-Agent Option

For maximum portability, install the skill at:

```text
.agents/skills/safeagentdb/SKILL.md
```

This is a good default for Codex and is also recognized by Cursor. Claude Code may still need the skill copied to `.claude/skills/safeagentdb/SKILL.md`.

## When Not To Add A Skill

Do not add a skill automatically if:

- the user only wants one-time setup
- the project has no agent instruction convention
- the user wants to keep the repo free of AI-specific files
- the target agent does not support skills

In those cases, add only README/deployment docs and the relevant always-on instructions.

