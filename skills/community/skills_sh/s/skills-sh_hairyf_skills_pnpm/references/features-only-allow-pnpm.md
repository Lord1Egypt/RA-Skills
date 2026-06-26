---
name: features-only-allow-pnpm
description: Enforce pnpm usage and prevent npm/yarn from being used
---

# Only Allow pnpm

Prevent developers from accidentally running `npm install` or `yarn` on a pnpm project.

## Setup

Add to `package.json`:

```json
{
  "scripts": {
    "preinstall": "npx only-allow pnpm"
  }
}
```

When someone runs `npm install` or `yarn`, they will see an error and installation will not proceed.

## npm v7+

Use `npx -y` to avoid prompt:

```json
{
  "scripts": {
    "preinstall": "npx -y only-allow pnpm"
  }
}
```

## Key Points

- `preinstall` runs before any package manager's install
- Fails fast with a clear message
- Recommended for team projects to avoid lockfile/format conflicts

<!--
Source references:
- https://pnpm.io/only-allow-pnpm
-->
