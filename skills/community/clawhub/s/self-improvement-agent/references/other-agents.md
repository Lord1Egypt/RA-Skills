# Other Agents: Claude Code, Codex, Copilot

Setup instructions for non-OpenClaw agents that support skills or similar patterns.

## Claude Code

### Hook Setup

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### Manual Learning Reminder

Add to project prompts or AGENTS.md:

```markdown
## Self-Improvement
After solving non-obvious issues, log to `.learnings/`. Format: see self-improvement skill.
```

## Codex CLI

Same hook pattern as Claude Code. Create `.codex/settings.json` with the same structure.

## GitHub Copilot

No hook support. Manual workflow:

1. At session end, review what was learned
2. Add to `.learnings/LEARNINGS.md` if relevant
3. Promote broadly applicable learnings to `.github/copilot-instructions.md`

Example entry in `.github/copilot-instructions.md`:

```markdown
## Project Conventions

- Package manager: **pnpm** — always use `pnpm install`, never `npm install`
- After API changes: run `pnpm run generate:api` to regenerate types
```

## Generic Setup (All Agents)

For any agent that supports custom instructions:

1. Create `.learnings/` directory in project root
2. Copy log templates from `assets/LEARNINGS.md`
3. Add reminder to agent config file (AGENTS.md, CLAUDE.md, .github/copilot-instructions.md)

```bash
mkdir -p .learnings
```

## Agent-Agnostic Triggers

Regardless of agent, log when:

- Discover something non-obvious (required debugging)
- Correct yourself mid-task
- Learn project convention not in docs
- Hit unexpected error (especially if diagnosis was hard)
- Find better approach than originally planned
