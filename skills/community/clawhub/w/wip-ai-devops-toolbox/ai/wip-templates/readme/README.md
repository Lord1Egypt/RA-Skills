# License Templates

These files are the **single source of truth** for all license content across WIP Computer repos. `wip-license-guard` reads these at runtime instead of using hardcoded strings.

## Files

| File | What it is | Used by |
|------|-----------|---------|
| `LICENSE.md` | The full dual MIT+AGPLv3 LICENSE file | `wip-license-guard init`, `wip-license-guard check --fix` |
| `cla.md` | Contributor License Agreement | `wip-license-guard init` |
| `wip-lic-footer.md` | README license section (plain text + markdown formats) | `wip-license-guard readme-license --fix` |

## How it works

When `wip-license-guard` runs, it looks for these templates in this order:

1. `WIP_TEMPLATES_DIR` env var (if set)
2. Walk up from the repo being checked, looking for `ai/wip-templates/readme/`
3. Fall back to hardcoded defaults (for standalone use outside the toolbox)

## Editing

Edit these files directly. The next time `wip-license-guard` runs, it picks up the changes. No code changes needed.

- **LICENSE.md**: Edit the copyright year, holder, or license text
- **cla.md**: Edit the CLA terms
- **wip-lic-footer.md**: Edit the README license section. Has two formats:
  - `// PLAIN TXT` section: for non-markdown contexts
  - `// MD FORMAT` section: for README.md files (used by `readme-license --fix`)

## Adding new templates

If you add new template files here, update `wip-license-guard/core.mjs` to read them.
