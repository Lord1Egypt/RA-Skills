# Plan: Rename ~/.ldm/shared/ to ~/.ldm/library/

**Date:** 2026-04-08
**Author:** cc-mini (with Parker)
**Status:** plan only. Do NOT execute without a dedicated session.
**Priority:** high (blocking documentation consistency)

## The Problem

Three documentation locations keep getting confused:
- `~/.ldm/shared/` ... agent OS docs (rules, boot, cron, dev guide, prompts)
- `~/wipcomputerinc/library/documentation/` ... human docs
- `~/wipcomputerinc/settings/docs/` ... duplicate that shouldn't exist

"shared" is a confusing name. Shared with whom? Agents don't think of it as shared. It's the OS library. Like `/usr/lib/` on a real OS.

Every session, someone writes to the wrong location. The installer deploys to both `settings/docs/` and `library/documentation/`. CLAUDE.md files point to different paths depending on when they were written. This has caused cascading confusion across multiple sessions.

## The Solution

Rename `~/.ldm/shared/` to `~/.ldm/library/`. Everything that lives in shared moves to library. Same structure, clearer name.

```
~/.ldm/library/                     (was ~/.ldm/shared/)
  boot/                             boot config, BOOT.md
  cron/                             cron definitions
  documentation/                    OS docs for agents (deployed by installer)
  dream-weaver/                     dream weaver protocol files
  prompts/                          system prompts
  rules/                            shared rules (git conventions, writing style, etc.)
  dev-guide-wipcomputerinc.md       org-specific dev guide
```

And separately:

```
~/wipcomputerinc/library/documentation/    human-readable docs (for Parker)
```

Two locations. Clear ownership:
- `~/.ldm/library/` = for agents (the OS)
- `~/wipcomputerinc/library/` = for humans (the home folder)

## What Needs to Change

### Phase 1: Inventory everything that references shared/

Every file that contains `~/.ldm/shared` or `.ldm/shared` or `shared/rules` or `shared/boot` or `shared/docs`:

| Category | Where to search |
|---|---|
| CLAUDE.md files | `~/wipcomputerinc/CLAUDE.md`, `~/.openclaw/CLAUDE.md`, every repo CLAUDE.md |
| Installer | `wip-ldm-os-private/bin/ldm.js`, `lib/deploy.mjs`, `lib/detect.mjs` |
| Hooks | `src/hooks/*.mjs`, `~/.ldm/extensions/*/` |
| Templates | `wip-ldm-os-private/shared/` (the source templates) |
| Rules | `~/.claude/rules/*.md`, `settings/config.json` |
| Boot config | `~/.ldm/shared/boot/`, `~/.openclaw/` boot references |
| OpenClaw workspace | `~/.openclaw/workspace/TOOLS.md`, `MEMORY.md`, etc. |
| Dev guide | `settings/templates/dev-guide-private.md` |
| Guard | `wip-branch-guard/guard.mjs` (if it references shared/) |
| Session hooks | `inbox-check-hook.mjs`, `cc-hook.mjs` |
| Memory crystal | Any remembered paths |
| Lesa workspace | `~/.openclaw/workspace/*.md` |

### Phase 2: Create ~/.ldm/library/ structure

1. Create `~/.ldm/library/`
2. Move everything from `~/.ldm/shared/` to `~/.ldm/library/`
3. Keep `~/.ldm/shared/` as a symlink to `~/.ldm/library/` (temporary, for backwards compat)

### Phase 3: Update the installer

1. `wip-ldm-os-private/shared/` (repo source) stays as-is for now (rename later)
2. `bin/ldm.js` and `lib/deploy.mjs` deploy to `~/.ldm/library/` instead of `~/.ldm/shared/`
3. Stop deploying to `~/wipcomputerinc/settings/docs/` entirely
4. Deploy agent docs to `~/.ldm/library/documentation/`
5. Deploy human docs to `~/wipcomputerinc/library/documentation/`

### Phase 4: Update all references

Every CLAUDE.md, rule, hook, template, workspace file that says `shared/` changes to `library/`. This is the bulk of the work.

### Phase 5: Update Lesa's workspace

`TOOLS.md`, `MEMORY.md`, and any workspace file that references `~/.ldm/shared/` needs updating. Lesa reads these on every boot.

### Phase 6: Remove settings/docs/

Delete `~/wipcomputerinc/settings/docs/` entirely. It was always a duplicate. The installer should never write there again.

### Phase 7: Remove symlink

After confirming nothing reads from `~/.ldm/shared/` anymore, remove the symlink.

### Phase 8: Rename repo source directory

Rename `wip-ldm-os-private/shared/` to `wip-ldm-os-private/library/`. Update all internal references. This is the final step.

## Risks

- **Silent breakage.** Any path that still says `shared/` after the rename will fail silently (file not found, agent loses context, rule not loaded).
- **Lesa's boot.** If BOOT.md or workspace files reference the old path, Lesa can't start properly.
- **Hooks.** If hooks reference old paths, they fail silently on every tool call.
- **Memory.** Crystal memories that reference old paths will be stale. Need to search and update.

## How to Execute Safely

1. Do the full inventory FIRST (Phase 1). Get the complete list.
2. Do the move + symlink (Phase 2). Nothing breaks because symlink covers it.
3. Update everything (Phases 3-5). Test after each phase.
4. Remove the symlink only when grep confirms zero references to old path.
5. Do this in a DEDICATED session. Don't mix with other work.

## Do NOT

- Do this piecemeal across multiple sessions
- Skip the inventory
- Remove the symlink before confirming all references are updated
- Assume you found all references (grep everything, including memory crystal)

## Cross-references

- `docs/doc-pipeline/README.md` ... how docs flow
- `ai/product/plans-prds/current/docs/2026-04-03--cc-mini--doc-architecture-and-update-pipeline.md` ... doc pipeline plan
- `ai/product/plans-prds/current/wip-code/2026-04-03--cc-mini--claude-md-master-plan.md` ... CLAUDE.md cascade (points to these docs)
- Memory crystal session 2026-04-03: detailed discussion about three doc locations
