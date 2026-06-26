---
name: features-env
description: Manage Node.js versions with pnpm env (similar to nvm/fnm)
---

# pnpm env

Manage Node.js versions without nvm or fnm.

:::warning
`pnpm env` does not include Corepack. Install separately if needed: `pnpm add -g corepack`
:::

## use - Install and activate

```bash
# Install and use LTS
pnpm env use --global lts

# Use specific version
pnpm env use --global 20
pnpm env use --global 18

# Prerelease
pnpm env use --global nightly
pnpm env use --global rc
pnpm env use --global 16.0.0-rc.0

# LTS by codename
pnpm env use --global argon

# Latest
pnpm env use --global latest
```

## add - Install without activating

```bash
pnpm env add --global lts 18 20.0.1
```

## remove / rm

```bash
pnpm env remove --global 14.0.0
pnpm env remove --global 14.0.0 16.2.3
```

## list / ls

```bash
# Local versions
pnpm env list

# Remote (available)
pnpm env list --remote

# Remote for v16
pnpm env list --remote 16
```

## Options

- `--global`, `-g` - Apply systemwide

## Key Points

- Alternative to nvm, fnm, volta for Node.js version management
- `use` installs and activates; `add` installs only
- Works well with standalone pnpm (no Node.js required for pnpm itself)

<!--
Source references:
- https://pnpm.io/cli/env
-->
