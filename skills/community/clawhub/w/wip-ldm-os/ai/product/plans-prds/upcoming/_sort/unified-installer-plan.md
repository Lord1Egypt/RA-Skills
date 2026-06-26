# Plan: Unified Installer ... LDM OS as the Install Layer

**Date:** 2026-03-12
**Authors:** Parker Todd Brooks, Claude Code (cc-mini)
**Status:** Plan
**Repos involved:** wip-ldm-os-private, memory-crystal-private, wip-ai-devops-toolbox-private

---

## Problem

Three systems install things to the same locations and none of them know about each other.

1. **`crystal init`** (memory-crystal) ... deploys to `~/.ldm/extensions/`, configures CC hooks, registers MCP, scaffolds `~/.ldm/`. Purpose-built, careful with data. 745 lines of working code in `installer.ts` that isn't wired up to the CLI yet.

2. **`wip-install`** (devops-toolbox) ... generic installer. Detects 6 interface types, deploys to `~/.ldm/extensions/` and `~/.openclaw/extensions/`, registers MCP, configures CC hooks. Toolbox mode. Registry at `~/.ldm/extensions/registry.json`. Has destructive bugs: `rm -rf` before copy, doesn't run build for TS extensions, breaks OpenClaw plugin naming.

3. **`scaffold.sh`** (wip-ldm-os) ... creates `~/.ldm/agents/cc/` with identity files. 97 lines of bash. CC agent only. No install, no deploy, no extension management.

All three deploy to `~/.ldm/extensions/`. All three register MCP servers. All three configure CC hooks. None of them coordinate.

## The Pattern That Works

The DevOps Toolbox nailed the install UX:

```
Read the SKILL.md at github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/SKILL.md.
Then explain to me: what are these tools? What do they do?
If I say yes, run: wip-install wipcomputer/wip-ai-devops-toolbox --dry-run
Show me exactly what will change. When I'm ready, install for real.
```

LDM OS should work the same way. You point your AI at the SKILL.md. It explains what LDM OS is. You say install. It shows you the dry run. You approve. Everything gets set up.

```
Read the SKILL.md at github.com/wipcomputer/wip-ldm-os/blob/main/SKILL.md.
Then explain to me: what is LDM OS? What does it do?
If I say yes, run: ldm install --dry-run
Show me exactly what will change. When I'm ready, install for real.
```

## LDM OS as a Kernel

LDM OS is the core binary. It lives at `~/.ldm/`, it has a version (`~/.ldm/version.json`), and it owns the structure underneath. Components don't ship LDM OS. They bootstrap it if it's missing, then call into it.

Once installed, LDM OS is independently updatable. `ldm update` bumps the kernel. The next time any component runs install or update, it checks the LDM OS version and adapts:

- LDM OS v0.1 creates `~/.ldm/extensions/`, `~/.ldm/agents/`, `~/.ldm/memory/`
- LDM OS v0.2 might add `~/.ldm/activity/` (for the daily digest), or change the registry format
- Components see v0.2, run any migrations they need, use the new capabilities

Over time, shared logic consolidates into LDM OS. Detection, deployment, MCP registration, hook wiring, registry management all move into the kernel. Component installers get thinner. The `ldm` binary gets smarter.

The version contract:
- `~/.ldm/version.json` ... `{ "version": "0.1.0", "installed": "2026-03-12", "updated": "2026-03-12" }`
- Components check `ldm --version` or read `version.json` to know what's available
- If LDM is older than what a component needs, the component can offer to update it
- If LDM is newer than expected, the component adapts to the new structure
- LDM never breaks backwards compatibility without a major version bump

## Architecture: Who Owns What

```
LDM OS (ldm)
  owns: ~/.ldm/, extension lifecycle, registry, deployment, hook/MCP wiring
  commands: ldm init, ldm install, ldm update, ldm doctor
  absorbs: wip-install detection logic + deployment logic (with bugs fixed)

Memory Crystal (crystal)
  owns: crystal.db, capture pipeline, search, Dream Weaver, Core/Node roles
  commands: crystal init (calls ldm install first, then MC-specific setup)
  keeps: DB backup, role setup, pairing, relay config

DevOps Toolbox (wip-install)
  owns: the tool suite (release, deploy-public, file-guard, etc.)
  commands: wip-install (becomes a thin wrapper around ldm install when LDM is present)
  keeps: toolbox mode, interface detection, SPEC.md standard
```

### The layering

```
┌──────────────────────────────────────────┐
│  Your AI reads SKILL.md                   │  ... "Teach Your AI"
├──────────────────────────────────────────┤
│  ldm install <org/repo>                   │  ... one command
├──────────────────────────────────────────┤
│  Detection: what interfaces does this     │  ... from wip-install's detect.mjs
│  repo have? CLI, MCP, OC, Skill, Hook?   │
├──────────────────────────────────────────┤
│  Deployment: copy to the right places     │  ... ~/.ldm/extensions/, ~/.openclaw/,
│  Register MCP, configure hooks, etc.      │     ~/.claude/, settings.json
├──────────────────────────────────────────┤
│  Component-specific setup                 │  ... crystal init does DB/roles/pairing
│  (each component handles its own extras)  │     after ldm install handles deployment
├──────────────────────────────────────────┤
│  Registry: ~/.ldm/extensions/registry.json│  ... what's installed, versions, sources
└──────────────────────────────────────────┘
```

### How `crystal init` changes

Before:
```
crystal init
  -> scaffoldLdm()           (creates ~/.ldm/ dirs)
  -> copy dist/ manually     (not using any installer)
  -> configure hooks manually
  -> register MCP manually
```

After:
```
crystal init
  -> ldm install memory-crystal   (LDM OS handles deploy, MCP, hooks, registry)
  -> crystal-specific setup:
     -> backup crystal.db if updating
     -> verify DB readable with new code
     -> Core/Node role setup
     -> pairing (if --pair flag)
     -> cron setup (crystal-capture, backup)
     -> discover existing sessions
```

### How `wip-install` changes

Before:
```
wip-install wipcomputer/wip-ai-devops-toolbox
  -> detect interfaces
  -> rm -rf target dirs (destructive)
  -> copy files
  -> register MCP
  -> configure hooks
  -> write registry
```

After:
```
wip-install wipcomputer/wip-ai-devops-toolbox
  -> if ldm CLI exists: delegate to ldm install
  -> if not: run standalone (current behavior, bugs fixed)
```

### Bootstrap: No Prerequisites, Ever

Nobody should ever be told "install LDM OS first." The tool you want is the entry point. LDM OS comes along for the ride.

**Three discovery paths, all work from zero:**

1. Someone finds **Memory Crystal** first: `crystal init` sees no `~/.ldm/`, bootstraps LDM OS silently, then installs MC
2. Someone finds **DevOps Toolbox** first: `wip-install` sees no `ldm` CLI, bootstraps LDM OS silently, then installs tools
3. Someone finds **LDM OS** directly: `npx @wipcomputer/ldm-os init` sets everything up, then `ldm install memory-crystal`

The bootstrap is a lightweight inline operation, not a separate install step:
1. Create `~/.ldm/` directory structure
2. Write `~/.ldm/version.json`
3. Install the `ldm` CLI globally (npm install -g)
4. Write initial registry
5. Continue with the component install the user actually asked for

Every component ships a `bootstrapLdm()` function (or imports it from `@wipcomputer/ldm-os`). If `~/.ldm/version.json` exists, skip. If not, run the bootstrap. Zero friction. Zero prerequisites.

## Bugs to Fix (from wip-ldm-os-private issues)

These are the three destructive bugs in `wip-install` that must be fixed before its logic moves into LDM OS:

### #6: Run build step for TypeScript extensions
The CLI installer tries to build, but the extension deployer does not. If there's no `dist/`, TypeScript extensions silently fail. Fix: detect `tsconfig.json` or `build` script, run build before deploy.

### #7: Update without override (never nuke and replace)
`rm -rf` before copy is destructive. If the new install fails partway through, you lose the old install. Fix: deploy to a temp directory first, verify it works, then atomic swap. Or: incremental copy (only replace changed files).

### #8: Handle OpenClaw plugin directory naming
OpenClaw matches plugins by directory name, not plugin id. Renaming a directory breaks the config. Fix: check `openclaw.json` for the expected plugin directory name before deploying. Never rename a directory that's referenced in config.

## Implementation Steps

### Phase 1: `ldm` CLI with `ldm install` (in wip-ldm-os-private)

1. Create `bin/ldm.mjs` ... the CLI entry point
2. Move `detect.mjs` from devops-toolbox into `lib/detect.mjs` (or import it as a dependency)
3. Build `lib/deploy.mjs` ... the deployment engine (from `wip-install`'s `install.js`, with bugs #6/#7/#8 fixed)
4. Build `ldm init` ... scaffolds `~/.ldm/`, creates agent config, installs CLI
5. Build `ldm install <org/repo>` ... detect + deploy + register + registry
6. Build `ldm install` (bare) ... install/update all registered components
7. Build `ldm update` ... alias for `ldm install` on existing registry
8. Build `ldm doctor` ... check health of all extensions
9. Publish to npm as `@wipcomputer/ldm-os`

### Phase 2: Wire Memory Crystal to use `ldm install`

1. `crystal init` checks if `ldm` CLI exists
2. If yes: runs `ldm install memory-crystal` for deployment, then does MC-specific setup
3. If no: falls back to current `installer.ts` behavior (self-contained)
4. Wire `runInstallOrUpdate()` in `installer.ts` to `cli.ts` (the 745 lines of working code)

### Phase 3: Wire DevOps Toolbox to delegate

1. `wip-install` checks if `ldm` CLI exists
2. If yes: delegates to `ldm install`
3. If no: runs standalone (current behavior, bugs fixed)

### Phase 4: Silent Bootstrap from Any Entry Point

1. `npx @wipcomputer/ldm-os init` works from zero (direct path)
2. `crystal init` bootstraps LDM OS silently if missing (MC entry point)
3. `wip-install` bootstraps LDM OS silently if missing (DevOps entry point)
4. No SKILL.md ever says "install LDM OS first." The tool you want handles it.

## What's Sacred (never touched during install/update)

| Location | Why |
|----------|-----|
| `~/.ldm/memory/crystal.db` | The database. 212K chunks. |
| `~/.ldm/state/*` | Watermarks, capture state, role |
| `~/.ldm/secrets/*` | Relay encryption key |
| `~/.ldm/agents/*/` | Identity files, journals, daily logs |
| `~/.ldm/config.json` | Agent list |
| `~/.openclaw/agents/` | OpenClaw sessions, auth |
| `~/.openclaw/secrets/` | 1Password SA token |
| `~/.openclaw/credentials/` | iMessage pairing |

## Open Issues to File

After this plan is reviewed:

- [ ] `wip-ldm-os-private`: `ldm` CLI scaffold (Phase 1)
- [ ] `wip-ldm-os-private`: absorb `detect.mjs` from devops-toolbox
- [ ] `wip-ldm-os-private`: deployment engine with atomic swap (fix #7)
- [ ] `wip-ldm-os-private`: TypeScript build detection (fix #6)
- [ ] `wip-ldm-os-private`: OpenClaw plugin naming (fix #8)
- [ ] `memory-crystal-private`: wire `crystal init` to `ldm install`
- [ ] `wip-ai-devops-toolbox-private`: `wip-install` delegates to `ldm install`
- [ ] `wip-ldm-os-private`: `npx @wipcomputer/ldm-os init` bootstrap

## Relation to Existing Issues

- memory-crystal-private: installer plan already written, code exists in `installer.ts`
- wip-ldm-os-private #3: move Universal Installer into LDM OS
- wip-ldm-os-private #4: boot-hook installer
- wip-ldm-os-private #5: zero-dependency bootstrap
- wip-ldm-os-private #6, #7, #8: the three destructive bugs
