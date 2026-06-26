# LDM OS v0.4.0

One dogfood session. Nine releases. Seven bugs found and fixed. One new feature shipped.

## New: ldm stack

Pre-defined tool stacks. Install everything your team needs with one command.

```bash
ldm stack list                    # show available stacks
ldm stack install core            # Memory Crystal, DevOps Toolbox, 1Password, mdview
ldm stack install web             # Playwright, Next.js DevTools, shadcn, Tailwind (MCP)
ldm stack install all             # everything
ldm stack install core --dry-run  # preview first
```

Three stacks ship in catalog.json. Stacks are composable ("all" includes "core" + "web"). The installer checks what's already installed, shows status, only installs what's missing.

This is Layer 1 (local install). Layer 2 (cloud MCP for iOS/web) is specced.

## Bugs fixed (v0.3.2 through v0.3.6)

- CLI self-update warning after install (v0.3.2)
- Stale hook cleanup in `ldm doctor --fix` (v0.3.2)
- /tmp/ paths flagged as stale even when file exists (v0.3.3)
- version.json auto-sync on npm upgrade (v0.3.4)
- CLI install from npm registry instead of /tmp/ symlinks (v0.3.5)
- SKILL.md prompt checks extension updates before summary (v0.3.6)

## Docs reorganized

Every feature now has its own folder with README.md + TECHNICAL.md:
- `docs/universal-installer/`
- `docs/acp/`
- `docs/skills/`
- `docs/recall/`
- `docs/shared-workspace/`
- `docs/system-pulse/`
