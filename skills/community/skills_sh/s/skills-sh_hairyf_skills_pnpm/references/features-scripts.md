---
name: features-scripts
description: Lifecycle scripts and pnpm-specific script hooks
---

# Scripts

How pnpm handles the `scripts` field of `package.json` and pnpm-specific lifecycle hooks.

## Lifecycle Scripts

### pnpm:devPreinstall

Runs only on local `pnpm install` (not in CI or when lockfile is present and frozen). Runs **before** any dependency is installed.

Must be set in the **root** project's `package.json`:

```json
{
  "scripts": {
    "pnpm:devPreinstall": "node scripts/preinstall.js"
  }
}
```

Use for: generating config, checking Node version, or setup that must run before `node_modules` is populated. Not run when using `--frozen-lockfile` or in most CI flows.

## Key Points

- Standard npm lifecycle scripts (`preinstall`, `postinstall`, etc.) work as usual.
- `pnpm:devPreinstall` is pnpm-specific; root only; skipped when lockfile is frozen or in non-interactive install.
- Scripts run with the shell/config defined by pnpm (e.g. `script-shell` in config).

<!--
Source references:
- https://pnpm.io/scripts
- sources/pnpm/docs/scripts.md
-->
