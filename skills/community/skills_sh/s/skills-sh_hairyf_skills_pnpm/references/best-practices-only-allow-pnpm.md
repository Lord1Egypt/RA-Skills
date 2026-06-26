---
name: best-practices-only-allow-pnpm
description: Enforce pnpm as the only package manager (only-allow)
---

# Only Allow pnpm

To prevent others from accidentally running `npm install` or `yarn` in a pnpm project, use the `only-allow` package in a `preinstall` script.

## Usage

Add to root `package.json`:

```json
{
  "scripts": {
    "preinstall": "npx only-allow pnpm"
  }
}
```

If someone runs `npm install` or `yarn`, the script will run and exit with an error so installation does not proceed.

For npm v7+, use:

```json
"preinstall": "npx -y only-allow pnpm"
```

## Key Points

- `preinstall` runs before install; `only-allow pnpm` exits with error if the current package manager is not pnpm.
- Use in monorepos and team projects to keep lockfile and tooling consistent.
- `npx -y` (or `npx --yes`) avoids interactive prompt in npm v7+.

<!--
Source references:
- https://pnpm.io/only-allow-pnpm
- sources/pnpm/docs/only-allow-pnpm.md
-->
