# Verify OpenCode

Use this workflow when the user asks whether OpenCode is connected to OpenPets.

## Steps

1. Confirm whether the user wants global or project-local setup.
2. For project-local setup, configure with:

```bash
openpets configure --agent opencode --pet <pet-id> --cwd <project-path> --yes
```

3. Check likely project files if needed:

```text
<project>/.opencode/opencode.jsonc
<project>/.opencode/openpets.md
```

4. Check likely global files if needed:

```text
~/.config/opencode/opencode.json
~/.config/opencode/opencode.jsonc
```

5. Ask the user to quit and restart OpenCode.
6. Verify with `openpets_status` or:

```bash
openpets status
```

If the CLI is not installed globally, replace `openpets` with `npx -y @open-pets/cli@latest`.

## Notes

- OpenCode config is loaded at startup; changes are not usually hot-reloaded.
- Prefer the OpenPets CLI configure command over manually editing OpenCode config.
