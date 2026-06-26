# Plan: wip-repo-permissions-hook

**Date:** 2026-03-01
**Agent:** cc-mini
**Location:** `wip-dev-tools-private/tools/wip-repo-permissions-hook/`

---

## Problem

Repos were made public without -private counterparts. This exposes internal plans, todos, dev updates, and development context. We need a guard that blocks this at every surface, just like branch protection blocks direct pushes to main.

## Architecture

Follows the 4-piece pattern (core, CLI, hook, plugin). Lives in wip-dev-tools alongside wip-release and wip-license-hook.

### Core (`core.mjs`)

Pure logic, zero deps:

- `checkPrivateCounterpart(org, repoName)` ... calls `gh api repos/{org}/{name}-private` to check if -private exists. Returns `{ allowed: bool, reason: string }`.
- `auditOrg(org)` ... lists all public repos, checks each one for -private counterpart. Returns list of violations.
- `isThirdPartyFork(org, repoName)` ... checks if repo is a fork (forks are exempt).

Rules encoded in core:
1. If repo is a fork of an external project, allow public (exempt).
2. If repo has a `-private` counterpart on GitHub, allow public.
3. Otherwise, block. "BLOCKED: {repo} cannot be made public without a -private counterpart."

### CLI (`cli.js`)

```bash
# Check a single repo before changing visibility
wip-repo-permissions check wipcomputer/wip-bridge
# -> BLOCKED: wip-bridge has no -private counterpart

# Audit all public repos in the org
wip-repo-permissions audit wipcomputer
# -> Lists violations, exit code 1 if any found

# Check if a repo is allowed to go public
wip-repo-permissions can-publish wipcomputer/memory-crystal
# -> OK: memory-crystal-private exists
```

### Claude Code Hook (`guard.mjs`)

PreToolUse:Bash hook. Reads stdin (same format as wip-file-guard), checks if the bash command contains `gh repo edit` with `--visibility public`. If so:

1. Extract repo name from the command
2. Run `checkPrivateCounterpart()`
3. If blocked, deny with error message
4. If allowed, exit 0 (allow)

Hook config in `~/.claude/settings.json`:
```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "node /path/to/guard.mjs",
    "timeout": 10
  }]
}
```

### OpenClaw Plugin (`openclaw.plugin.json`)

`before_tool_use` lifecycle hook, same pattern as wip-file-guard. Intercepts shell commands that change visibility.

### Cron Audit (`audit-job.sh`)

New job in `tools/ldm-jobs/visibility-audit.sh`. Runs via LDMDevTools.app on schedule (daily or weekly). Calls CLI `audit` command. Logs violations. Could auto-flip repos back to private or just alert.

## File Structure

```
tools/wip-repo-permissions-hook/
  core.mjs          ... pure logic (checkPrivateCounterpart, auditOrg, isThirdPartyFork)
  cli.js            ... CLI wrapper (check, audit, can-publish)
  guard.mjs         ... Claude Code PreToolUse:Bash hook
  openclaw.plugin.json  ... OpenClaw plugin manifest
  package.json
  README.md
  SKILL.md          ... universal installer (any AI can read and understand)
```

## Build Order

1. `core.mjs` ... the logic
2. `cli.js` ... test it manually
3. `guard.mjs` ... wire into Claude Code hooks
4. Test: try `gh repo edit --visibility public` on a repo without -private, verify it blocks
5. `openclaw.plugin.json` ... wire into OpenClaw
6. `visibility-audit.sh` in ldm-jobs ... cron safety net
7. `SKILL.md` + `README.md` ... docs

## Dependencies

- `gh` CLI (already installed, already authenticated)
- No npm dependencies (zero deps, like wip-file-guard)

## Edge Cases

- Repo name already ends in `-private` ... skip (it IS the private repo)
- Repo is a fork ... check `gh api repos/{org}/{name}` for `.fork == true`, exempt if external
- Repo is in the known exceptions list (if needed) ... hardcoded Set in core
- `gh` CLI not available ... fail open (allow, log warning). Don't block dev work if gh is broken.
- Org has hundreds of repos ... `auditOrg` paginates via gh API

## Verification

```
[ ] `wip-repo-permissions check wipcomputer/wip-bridge` -> BLOCKED (no -private)
[ ] `wip-repo-permissions check wipcomputer/memory-crystal` -> OK (has -private)
[ ] `wip-repo-permissions check wipcomputer/paulxstretch` -> OK (fork, exempt)
[ ] `wip-repo-permissions audit wipcomputer` -> lists any violations
[ ] Claude Code hook blocks `gh repo edit wipcomputer/wip-bridge --visibility public`
[ ] Claude Code hook allows `gh repo edit wipcomputer/memory-crystal --visibility public`
[ ] Cron job runs and logs results
```
