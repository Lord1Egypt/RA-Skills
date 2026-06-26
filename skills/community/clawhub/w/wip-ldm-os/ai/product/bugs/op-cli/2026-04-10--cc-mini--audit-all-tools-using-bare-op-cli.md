# Bug: Audit all tools that shell out to bare `op` CLI

**Date:** 2026-04-10
**Filed by:** cc-mini + Parker
**Component:** All tools that load secrets from 1Password
**Severity:** High (architectural pattern risk, fragility across reboots and upgrades)

## Summary

The `wip-xai-grok` deprecated core exposed a pattern: tools that shell out to `op` via `execSync` are fragile. They depend on the 1Password desktop app being authorized for whichever process they run under. That authorization gets invalidated by:

- OpenClaw upgrades (new binary, new app identity)
- 1Password desktop app upgrades
- macOS reboots
- Any other event that clears the biometric remember state

When the authorization drops, bare `op read` triggers a GUI prompt. If the agent is running headless (cron, heartbeat, remote session), the prompt never gets answered and the tool fails silently.

**The canonical headless pattern already exists:** `@wipcomputer/wip-1password/helper` exports `opRead()` and `opReadMultiple()` using the `@1password/sdk` JS library. It uses the SA token directly, no shell calls, no desktop app, no biometric prompts. Every tool that currently shells out to `op` should migrate to this helper.

## The fix pattern

Before (fragile):

```javascript
import { execSync } from 'node:child_process';

const key = execSync('op read "op://Agent Secrets/X API/api key"', {
  stdio: ['pipe', 'pipe', 'pipe'],
  timeout: 10000,
}).toString().trim();
```

After (headless):

```javascript
import { opRead } from '@wipcomputer/wip-1password/helper';

const key = await opRead('X API', 'api key');
```

Identical behavior when the token is present. No desktop app involvement. Works under exec subprocesses, cron, LaunchAgents, anywhere Node can run.

## Audit scope

Tools to inspect:

**In `~/.openclaw/extensions/`:**
- wip-xai-grok (known offender, already filed as separate ticket)
- wip-agent-pay
- wip-1password (the plugin itself; check it's only using the helper pattern internally)
- Any other extension with a `dist/` folder or `core.mjs`

**In `~/.ldm/extensions/`:**
- Same list (deploys overlap)

**In `/opt/homebrew/bin/`:**
- wip-xai-grok (known)
- wip-release
- wip-xai-x
- Any other `wip-*` binary

**In the source tree:**
- Everything under `ldm-os/apis/`
- Everything under `ldm-os/utilities/`
- Everything under `ldm-os/components/`
- Exclude: `node_modules/`, `dist/`, `_trash/`, `.worktrees/`

## Audit command

```bash
grep -rn "execSync.*op read\|execSync.*'op \\|execSync.*\"op \\|spawnSync.*op " \
  ~/wipcomputerinc/repos/ldm-os \
  --exclude-dir=node_modules \
  --exclude-dir=dist \
  --exclude-dir=_trash \
  --exclude-dir=.worktrees
```

That produces the initial list of offenders.

## Per-offender fix

For each tool that calls bare `op`:

1. Add `@wipcomputer/wip-1password/helper` as a dependency in its `package.json`
2. Replace `execSync('op read ...')` with `await opRead(...)` (note: becomes async, callers must await)
3. Test locally with SA token present (should succeed silently)
4. Test locally with SA token missing (should throw a clear error, not fall through to GUI)
5. Build and publish the updated package
6. Deploy via `ldm install`
7. Verify no residual `op` processes appear in the process tree when the tool runs

## Deliverables

1. **Audit report** (list of offenders) committed to `ai/product/bugs/op-cli/2026-04-10--cc-mini--op-cli-audit-results.md`
2. **Individual fix PRs** (one per offender, small and focused)
3. **Migration summary** documenting which tools were migrated and when
4. **Verification:** a scripted check that runs after `ldm install` and greps the deployed tools for `execSync.*op` patterns. If any match, warn loudly.

## Why this matters

The same pattern that broke `wip-xai-grok` today could be silently broken in any other tool right now. Parker might not hit it until he's away from the keyboard and a cron job fires. We got lucky that this failure was interactive.

Fixing them proactively is cheap (the helper exists, the migration is mechanical) and removes a whole class of fragility.

## Related

- Ticket 1: Deprecated xai-grok still deployed (specific instance of this pattern)
- Ticket 2: Finish deprecating old xai-grok repo
- Ticket 3: Installer must deploy new xai-grok
- Related rule: `~/wipcomputerinc/CLAUDE.md` "1Password CLI: Always Use Service Account Token"
- Canonical helper: `ldm-os/utilities/wip-1password-private/src/helper.ts`
