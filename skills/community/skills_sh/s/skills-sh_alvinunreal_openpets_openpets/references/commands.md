# OpenPets Commands

Recommended clean setup:

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

One-off fallback when the user does not want a global install:

```bash
npx -y @open-pets/cli@latest status
```

MCP package:

```bash
npx -y @open-pets/mcp@latest --pet <pet-id>
```

Pet catalog:

```text
https://openpets.dev/pets/catalog.v3.json
```

For search, fetch `catalog.v3.json`, then fetch its `search` URL and the listed search pages. Use matching search entries' `catalogPage` values to fetch `catalog.v3/page-XXX.json` pages for install metadata.
