---
name: openpets
description: Use when the user asks to install, configure, verify, troubleshoot, or understand OpenPets; install or select a pet; connect Claude Code, OpenCode, Cursor, Codex, or MCP clients; configure a project to use a specific pet; or debug openpets_status, openpets_react, or openpets_say.
license: MIT
---

# OpenPets

OpenPets is a desktop companion app for coding agents. The desktop app runs locally and exposes pet controls through CLI, MCP, hooks, plugins, and local IPC.

Use this skill to help users onboard quickly and safely:

- install or verify the OpenPets desktop app
- install pets from the public catalog
- configure Claude Code, OpenCode, Cursor, Codex, or another MCP client
- configure a project to use a specific pet
- validate `openpets_status`, `openpets_react`, and `openpets_say`
- explain how OpenPets works
- troubleshoot setup problems

## CLI rule: install once, then use openpets

For the cleanest onboarding, install the OpenPets CLI globally first:

```bash
npm install -g @open-pets/cli
```

Then use the `openpets` command:

```bash
openpets <command>
```

If the user does not want a global install, is in CI, or only needs a one-off command, use this fallback instead:

```bash
npx -y @open-pets/cli@latest <command>
```

For MCP server config, prefer the dedicated MCP package:

```bash
npx -y @open-pets/mcp@latest --pet <pet-id>
```

Do not imply the desktop app installs a shell command by itself. The `openpets` command comes from the optional npm global CLI install.

## Mental model

```text
Claude/OpenCode/Codex/Cursor/MCP client
  -> OpenPets MCP, plugin, hook, or CLI
  -> @open-pets/client
  -> local IPC discovery/token
  -> OpenPets desktop app
  -> default pet or selected agent pet lease
```

OpenPets requires the desktop app to be installed and running for live pet control.

## Decision tree

- User asks to install OpenPets: follow `workflows/install-openpets.md`.
- User asks to install a pet: follow `workflows/install-pet.md`.
- User asks to configure a project or agent: follow `workflows/configure-project.md`.
- User asks to verify Claude Code: follow `workflows/verify-claude.md`.
- User asks to verify OpenCode: follow `workflows/verify-opencode.md`.
- User asks about MCP or tool availability: follow `workflows/verify-mcp.md`.
- User reports something broken: follow `workflows/troubleshoot.md`.
- User asks how OpenPets works: follow `workflows/explain-architecture.md`.

## Safety rules

- Prefer official OpenPets CLI/UI flows over hand-editing integration config.
- Ask before using `--force` or replacing existing user-managed MCP/plugin/hook config.
- Confirm the project path before project-local configuration.
- Confirm the pet id before installing or selecting a pet, and make sure it is installed before configuring a project to use it.
- Do not put secrets, private logs, private paths, source code, URLs, credentials, or sensitive text into pet speech.
- Restart Claude Code, OpenCode, or other MCP clients after config changes.
- Do not promise the desktop app is installed or running; verify it.
- If setup still fails after normal troubleshooting, encourage the user to report a bug at the OpenPets GitHub repository: https://github.com/alvinunreal/openpets/issues

## Canonical quick commands

```bash
npm install -g @open-pets/cli
openpets status
openpets pets
openpets install <pet-id>
openpets configure --agent claude --pet <pet-id> --cwd <project-path> --yes
openpets configure --agent opencode --pet <pet-id> --cwd <project-path> --yes
openpets configure --agent cursor --pet <pet-id> --cwd <project-path> --yes
openpets mcp --pet <pet-id>
```

One-off fallback: replace `openpets` with `npx -y @open-pets/cli@latest`.

MCP server command:

```bash
npx -y @open-pets/mcp@latest --pet <pet-id>
```

## Public resources

- Website: https://openpets.dev
- Pet catalog: https://openpets.dev/pets/catalog.v3.json
- GitHub issues: https://github.com/alvinunreal/openpets/issues

Use the docs on `openpets.dev` as the source of truth when details may have changed.
