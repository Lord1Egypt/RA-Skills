# Verify Claude Code

Use this workflow when the user asks whether Claude Code is connected to OpenPets.

## Steps

1. Check Claude is available:

```bash
claude --version
```

2. Check the OpenPets MCP entry:

```bash
claude mcp list
claude mcp get openpets
```

3. If configuration is missing, configure it:

```bash
openpets configure --agent claude --pet <pet-id> --cwd <project-path> --yes
```

If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.

4. Ask the user to restart Claude Code.
5. Verify from Claude with the MCP tool `openpets_status`.

## Hooks

Claude hooks are optional. Do not install or modify hooks unless the user asks for automatic reactions/status behavior.

If hooks are requested, prefer the official OpenPets configure flow or OpenPets Claude tooling instead of manual edits.
