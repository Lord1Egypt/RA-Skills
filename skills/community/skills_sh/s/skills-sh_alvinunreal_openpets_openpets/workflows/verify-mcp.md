# Verify MCP

Use this workflow when MCP tools are missing or unavailable.

## Expected tools

OpenPets MCP exposes:

```text
openpets_status
openpets_react
openpets_say
```

## Server command

For MCP client configuration, use:

```bash
npx -y @open-pets/mcp@latest --pet <pet-id>
```

or through the CLI:

```bash
openpets mcp --pet <pet-id>
```

If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.

## Checklist

1. Confirm the desktop app is running.
2. Confirm the MCP client has an OpenPets server entry.
3. Confirm the server command uses `npx -y @open-pets/mcp@latest --pet <pet-id>` or equivalent.
4. Restart the MCP client.
5. Call `openpets_status`.

If `openpets_status` says the desktop app or local IPC is unavailable, focus on the desktop app/runtime rather than MCP config.
