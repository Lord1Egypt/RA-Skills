# LDM OS v0.4.74

First stable release after 34 alphas. Visible user-facing changes are small on purpose ... most of the work in this window was strategy, triage, and repo hygiene that sets up the next few releases. What ships here is a small, safe patch plus two foundation pieces you'll feel in the coming weeks.

## What's new for you

**`ldm doctor --fix` now cleans up stale Claude Code env overrides.**

If you set LDM OS up during the Opus 4.6 era, your `~/.claude/settings.json` may have `CLAUDE_CODE_EFFORT_LEVEL` and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` set. These were reasonable then. With Opus 4.7 they actually interfere with adaptive behavior, because the model picks its own effort level and forcing it with an env var undercuts that.

Running `ldm doctor --fix` now removes just those two keys from your settings, leaves everything else in the file untouched, and reports what it did. It's idempotent ... running it again is a silent no-op. If you've already upgraded to 4.7 and noticed Claude Code feels "less responsive" after, this is the fix.

**Kaleidoscope pages now share a template system.**

The Kaleidoscope login page, the demo, and the other hosted pages used to drift visually. Each one shipped its own CSS, so the footer, typography, and little interactive behaviors would diverge quietly over time. This release adds a single `kaleidoscope.css` + `kaleidoscope.js` served from the hosted MCP server, so new pages pull from a shared source of truth.

You won't see anything different in the UI today. The point is that the next wave of work ... the Kaleidoscope + Lēsa install shell ... has a clean foundation to build on. When we add the post-login view with Lēsa offering to install Memory Crystal, Agent Pay, Directory, and the other products, the styling doesn't fork.

## Repo hygiene

`.worktrees/` and `.playwright-mcp/` are now in `.gitignore`. If you've been seeing them show up after worktree creation or Playwright runs, they stop polluting your working tree.

## Coming next (not in this release, but now planned)

Most of the work between v0.4.73-alpha.34 and this release was in `ai/product/` ... strategy docs, vision-quest-01 priorities synthesis, bug triage, and a master plan for the next phase of release pipeline hardening. That work stays private (per `deploy-public.sh`'s `ai/` exclusion) but it's the reason the next few releases will move faster and feel safer.

Specifically queued for upcoming releases:
- Fail-closed `wip-release` ... no more half-released repos if a step fails mid-pipeline.
- `wip-release --rollback` ... revert a bad release with one command.
- Per-PR CI in every private repo ... catch broken installs before they merge, not after.
- Canary install loop ... every alpha gets auto-installed on a clean runner and smoke-tested before you see it.

## Install

```bash
npm install -g @wipcomputer/wip-ldm-os
ldm init
ldm install --dry-run
```

Or, agent-guided:

```
Read https://wip.computer/install/wip-ldm-os.txt
```

Paste into any AI. It walks you through.

Closes wipcomputer/wip-ldm-os#268.
