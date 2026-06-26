# OpenClaw Hooks Reference

OpenClaw supports server-side hooks that execute automatically without the LLM needing to remember. These are configured in `openclaw.config.json`.

## Hook Types

### afterFileWrite

Runs after the agent writes a file. Use for auto-formatting and linting.

```json5
{
  "hooks": {
    "afterFileWrite": {
      "pattern": "src/**/*.{ts,tsx,js,jsx}",
      "command": "npx eslint --fix $FILE && npx prettier --write $FILE"
    }
  }
}
```

### beforeReply

Runs before the agent sends a reply. Use for type checking.

```json5
{
  "hooks": {
    "beforeReply": {
      "command": "npx tsc --noEmit 2>&1 | head -20"
    }
  }
}
```

### beforeFileRead

Runs before the agent reads a file. Use for access control or preprocessing.

```json5
{
  "hooks": {
    "beforeFileRead": {
      "pattern": ".env*",
      "command": "echo 'WARNING: Reading sensitive file'"
    }
  }
}
```

## Context File Priority

OpenClaw loads context files in a specific order. Higher priority files can override lower ones:

| File | Priority | Typical Content |
|------|----------|----------------|
| agents.md | 10 | Multi-agent routing rules |
| soul.md | 20 | Persona, tone, communication style |
| identity.md | 30 | Agent identity constraints |
| user.md | 40 | User-specific preferences |
| tools.md | 50 | Tool usage rules and restrictions |
| bootstrap.md | 60 | Bootstrap workflow rules |
| memory.md | 70 | Memory management rules |

## Cleanup Templates

After converting rules to hooks, update the relevant context files.

### tools.md (after toolifying lint/format rules)

```markdown
## Tool Rules

Automated rules enforced by hooks in `openclaw.config.json`:
- Linting: `npx eslint .`
- Formatting: `npx prettier --write .`
- Type checking: `npx tsc --noEmit`

### Remaining Rules (require human judgment)
- [list non-toolifiable rules here]
```

### bootstrap.md (after adding hooks)

```markdown
## Automated Checks

Hooks configured in `openclaw.config.json`:
- `afterFileWrite`: auto-lint + format on `src/**/*.{ts,tsx}`
- `beforeReply`: type check before agent replies

No manual lint step needed.
```

## SAFETY.md

`SAFETY.md` is hardcoded in OpenClaw's `system-prompt.ts` and cannot be modified by hooks or plugins. Safety constraints written in this file must remain as prompt-level rules — they cannot be toolified.

## Slot System

OpenClaw has two exclusive plugin slots:
- `memory` — for memory plugins (memory-core, memory-lancedb, memory-wiki)
- `contextEngine` — for context engine plugins

Only one plugin can occupy each slot at a time. Hooks operate independently of the slot system.
