# Convert Agent to Skill

Converts an existing agent (.md file) into a skill structure.

## Usage

```bash
/skill-manager convert <agent-name>
```

## Workflow

### 1. Read Agent File

```bash
# Global agent
cat ~/.claude/agents/<agent-name>.md

# Project agent
cat .claude/agents/<agent-name>.md
```

### 2. Conversion Rules

| Agent Element | Skill Conversion |
|-----------|-----------|
| `name` | Keep as-is (suffix removal recommended) |
| `description` | Add triggers keywords |
| `tools` | Remove (skills use all tools by default) |
| `model` | Keep (optional) |
| Script references | Copy to `scripts/` folder, change to relative paths |

### 3. Create Skill

Follow the [writer.md](./writer.md) guide to create the skill structure:

1. Create folder: `mkdir -p ~/.claude/skills/<skill-name>/scripts`
2. Write SKILL.md (frontmatter + body)
3. Copy scripts and `chmod +x`

### 4. Move Original

Depending on the agent file location:

```bash
# Global agent
mv ~/.claude/agents/<name>.md ~/.claude/.bak/

# Project agent
mv .claude/agents/<name>.md .claude/.bak/
```

## Example

**Before conversion (Agent)**:
```markdown
---
name: syncthing-conflict-resolver
description: Automatically handles Syncthing sync-conflict files...
tools: Bash, Read
---
~/Sync/AI/scripts/resolve-sync-conflicts.sh
```

**After conversion (Skill)**:
```
skills/syncthing-conflict/
├── SKILL.md
└── scripts/
    └── resolve-conflicts.sh
```

## Checklist

- [ ] Read agent
- [ ] Create skill folder + SKILL.md ([writer.md](./writer.md))
- [ ] Copy scripts + permissions
- [ ] Delete original
