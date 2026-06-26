# LDM OS v0.4.2

Dogfood continues. Doctor hang fixed, bridge renamed, docs completed, git commits on main now blocked globally.

## Fixes

- **Doctor hang** (missing `await` on async function). One character fix. Also adds 5s timeouts to CLI binary detection to prevent zombie processes. Closes #48
- **Boot hook sync.** `ldm install` now updates `~/.ldm/shared/boot/boot-hook.mjs` from the npm package. Sessions, messages, and update surfacing from v0.3.0 were never activating because the deployed boot hook was stale. Closes #49
- **Bridge renamed** from `lesa-bridge` to `wip-bridge`. MCP server name, all log output, CLI headers, docs. Product name, not personal name. Closes #50

## New: Global pre-commit hook

`ldm init` now installs a git pre-commit hook that blocks commits on main/master. Every repo on the machine. Every agent. Git itself refuses the commit before it happens.

```bash
~/.ldm/hooks/pre-commit
git config --global core.hooksPath ~/.ldm/hooks
```

No more agents committing to main by accident. The CC branch guard is a warning layer on top. The git hook is enforcement. Closes #51

## Docs

- Bridge docs added: `docs/bridge/README.md` (protocol comparison chart) + `docs/bridge/TECHNICAL.md` (full original bridge README content)
- All doc READMEs now link to their TECHNICAL.md
- Bridge listed first under "Ships with LDM OS" in main README
- README title: "LDM OS: Learning Dreaming Machines"
- All broken doc links fixed after docs reorg
- Bridge repos renamed to `wip-bridge-deprecated` and `wip-bridge-private-deprecated`
