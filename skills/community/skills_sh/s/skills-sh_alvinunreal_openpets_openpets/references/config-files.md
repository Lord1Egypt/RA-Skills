# Config Files

Prefer official OpenPets configure commands over manual edits.

## Claude Code

```text
~/.claude/settings.json
~/.claude/CLAUDE.md
~/.claude/openpets.md
<project>/.claude/settings.local.json
```

Project command:

```bash
openpets configure --agent claude --pet <pet-id> --cwd <project-path> --yes
```

## OpenCode

```text
~/.config/opencode/opencode.json
~/.config/opencode/opencode.jsonc
<project>/.opencode/opencode.jsonc
<project>/.opencode/openpets.md
```

Project command:

```bash
openpets configure --agent opencode --pet <pet-id> --cwd <project-path> --yes
```

If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.

## Restart required

After MCP/plugin/hook/config changes, ask the user to restart Claude Code, OpenCode, Cursor, Codex, or their MCP client.
