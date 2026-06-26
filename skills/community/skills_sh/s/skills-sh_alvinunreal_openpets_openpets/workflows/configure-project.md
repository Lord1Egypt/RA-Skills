# Configure a Project

Use this workflow when the user asks to configure the current project or a named project to use OpenPets.

## Questions to confirm

- Which agent/client should be configured? Common values: `claude`, `opencode`, `cursor`.
- Which project path should be configured?
- Which pet should be selected? If the user has not chosen one, list installed pets and use the catalog API to help them choose or install one.
- Is it okay to update project-local config files?

## Before configuring

Make sure the selected pet exists locally. If the user did not provide a pet id, start by listing installed pets:

```bash
openpets pets
```

If the user wants a pet that is not installed, use the catalog API to confirm the pet id, then install it before writing project config.

- https://openpets.dev/pets/catalog.v3.json

Catalog search flow:

1. Fetch `catalog.v3.json`.
2. Fetch its `search` URL.
3. Fetch the listed `search-page-XXX.json` pages.
4. Match user words against each entry's `searchText`, `id`, and `displayName`.
5. Fetch the matching entry's `catalogPage` from `catalog.v3/page-XXX.json` to get install metadata.

```bash
openpets install <pet-id>
```

## Claude Code

```bash
openpets configure --agent claude --pet <pet-id> --cwd <project-path> --yes
```

Potential files:

```text
<project>/.claude/settings.local.json
~/.claude/settings.json
~/.claude/CLAUDE.md
~/.claude/openpets.md
```

## OpenCode

```bash
openpets configure --agent opencode --pet <pet-id> --cwd <project-path> --yes
```

Potential files:

```text
<project>/.opencode/opencode.jsonc
<project>/.opencode/openpets.md
~/.config/opencode/opencode.json
~/.config/opencode/opencode.jsonc
```

## Cursor

```bash
openpets configure --agent cursor --pet <pet-id> --cwd <project-path> --yes
```

## Safety

- Use `--force` only after explicit approval.
- Prefer project-local configuration when the user asks “for this project”.
- Do not configure a project for a pet that is not installed; install it first.
- Ask the user to restart their agent/client after config changes.
- If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.
