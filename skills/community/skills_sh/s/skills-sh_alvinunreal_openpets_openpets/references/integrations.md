# Integrations

## MCP

OpenPets MCP exposes:

```text
openpets_status
openpets_react
openpets_say
```

Server command:

```bash
npx -y @open-pets/mcp@latest --pet <pet-id>
```

## Claude Code

Use the CLI configure flow:

```bash
openpets configure --agent claude --pet <pet-id> --cwd <project-path> --yes
```

Claude hooks are optional and should not be changed without user approval.

## OpenCode

Use the CLI configure flow:

```bash
openpets configure --agent opencode --pet <pet-id> --cwd <project-path> --yes
```

OpenCode usually requires restart after config changes.

## Cursor and other MCP clients

Prefer the official configure flow when available. Otherwise configure an MCP server using:

```bash
npx -y @open-pets/mcp@latest --pet <pet-id>
```

If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.
