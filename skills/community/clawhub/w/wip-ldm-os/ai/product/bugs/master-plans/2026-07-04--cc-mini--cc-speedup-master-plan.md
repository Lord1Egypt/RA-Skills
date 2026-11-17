---
title: "Speed up Claude Code on mac-mini: 4 tasks, priority order"
status: in-progress
priority: P1
owner: cc-mini
repo: multiple (see per-task)
created: 2026-07-04
---

# Speed up Claude Code on mac-mini (4 tasks, priority order)

Context: CC sessions get stuck in slow retry loops. Root causes diagnosed 2026-07-04: guard false-positives (main cause), heavy synchronous Stop hook, per-tool-call hook fan-out, duplicated fixed context. Memory/swap was ruled out (0 swap used, 91% RAM free).

Related, same day, already in review: PR #1086 (boot-hook duplicate SessionStart registration + persist bug + `ldm doctor` settings.json repairs). The 10x duplicate boot hook was the first slowness cause found and fixed; the tasks below are the rest.

## Task 1: Fix branch-guard false positives (biggest win, do first)

Repo: `wip-ai-devops-toolbox-private`, subtool `tools/wip-branch-guard/` (deployed copy is `/Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs`; never edit the deployed file).

Bug: `DESTRUCTIVE_PATTERNS` are tested against the entire stripped command string at guard.mjs:1676, but the Gap B redirect patterns (v1.9.83, around lines 540-548) use an unanchored `.*` between the redirect and the protected path:

```
/(>>?|\btee\b).*\.ldm\/extensions\/[^\s|;&]+/
```

So any command containing any `>` (including `2>/dev/null` or `2>&1`) that mentions `.ldm/extensions/`, `.openclaw/(extensions|credentials|secrets)/`, or `openclaw.json` anywhere later in the line... even as a read path... is blocked as destructive. The per-segment helper `isBlockedCompoundCommand()` already exists in the file but is not used for this check.

Fix: run `DESTRUCTIVE_PATTERNS` per shell segment via `isBlockedCompoundCommand()` (or change `.*` to `[^;|&]*` in the six Gap B redirect patterns). Keep the actual protection intact: `echo x > ~/.ldm/extensions/foo/bar.js` must still block.

Regression cases (all must PASS after fix, all currently blocked):
1. `tail -5 /Users/lesa/.ldm/logs/foo.log 2>/dev/null; ls /Users/lesa/.ldm/extensions/wip-branch-guard/`
2. `echo '{"tool_name":"Read"}' | node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs >/dev/null 2>&1`
3. `du -sh ~/.claude/projects/ 2>/dev/null; find ~/.ldm -name "*guard*log*"`

Must still BLOCK: `echo x > ~/.ldm/extensions/foo.js`, `cat y | tee ~/.openclaw/openclaw.json`, `git reset --hard`, `git clean -fd`.

Secondary (same PR or follow-up): `node <script>` invocations get blocked as "file-modifying on main" even for read-only scripts (repro: `node /Users/lesa/.ldm/shared/boot/boot-hook.mjs < /dev/null`). Investigate whether that check can whitelist known read-only invocations or check for write flags.

Serial-blocking fix (already written): the onboarding gate denies before the branch gate is reached, two round trips per write. The onboarding deny now appends a HEADS UP worktree note when the repo is on main.

State at handoff: both fixes written and validated in worktree `.worktrees/wip-ai-devops-toolbox-private--cc-mini--guard-friction-fixes` (branch `cc-mini/guard-friction-fixes`), test suite 132 pass / 0 fail / 8 skip with 6 new regression cases, UNCOMMITTED. Loose ends: verify the HEADS UP note renders on a real on-main repo and add a regression test for it; then release notes, commit (co-authors), push, PR, both reviewers.

## Task 2: Cut Stop-hook cost (memory-crystal cc-hook)

File: memory-crystal repo, source of `dist/cc-hook.js`. Runs synchronously after EVERY CC turn (30s timeout).

1. Incremental scan: the cc-poller re-lists all transcript files every run (66 files in `~/.claude/projects/-Users-lesa-wipcomputerinc/`, growing forever since `cleanupPeriodDays` is 3650). Keep a per-file high-water mark (byte offset or mtime) and only process new content.
2. Kill the per-turn 1Password shell-out: `OPENAI_API_KEY` is not in CC's environment, so `getOpSecret()` runs `op item get` over the network (up to 5s) on capture. Fix: set the key once in CC's env via the env block in `~/.claude/settings.json` (or a login-shell export sourced from op at boot). Never hardcode the key in a committed file.
3. Optional, bigger: move capture out of the Stop hook into a background daemon or async hook so it never delays turn completion.

Note: the inbox-rewake Stop hook (21600s timeout) is fine as-is... it's `async: true` with a lockfile. Don't touch it.

## Task 3: Reduce per-tool-call hook fan-out

File: `~/.claude/settings.json` hooks section (source-controlled home is the dot-claude private repo; change at source, deploy via installer).

Current state: every Bash call spawns 2 node processes (branch-guard + license-guard), every Edit/Write spawns 3 (file-guard + repo-permissions + branch-guard), every Read/Glob spawns 1. Node startup is ~60ms and branch-guard makes up to 14 subprocess calls. Estimated 0.2-0.5s per tool call.

1. Merge the three Edit/Write guards behind one dispatcher script (one node boot, calls the three checks in-process).
2. Evaluate dropping Read|Glob from the branch-guard matcher: on Read/Glob it only records "agent read this file" for the onboarding gate (guard.mjs:1659-1667). If the onboarding gate can source read-tracking another way, drop the matcher entries.

## Task 4: Dedupe fixed context

1. `/Users/lesa/.claude/CLAUDE.md` (22KB) and `/Users/lesa/wipcomputerinc/CLAUDE.md` (23.6KB) are ~80% identical. Make one canonical, reduce the other to the delta plus a pointer. Roughly 5K tokens off every single model call.
2. Trim the SessionStart boot-hook payload (`src/boot/boot-hook.mjs` in wip-ldm-os-private, currently injects ~46KB per session). The SHARED-CONTEXT excerpt it embeds is stale (April content) and could be capped; step 8 re-injects a March journal every session (add a staleness cutoff, emit path only when old).

## Workflow reminders

- Worktree + branch per repo (`cc-mini/` prefix), never edit deployed files under `~/.ldm/` or `~/.openclaw/` directly... repo, PR, merge (`--merge`, never squash), `wip-release`, then stop. Parker installs stable.
- Co-authors on every commit.
- RELEASE-NOTES on the feature branch, not after.
- Task 1 is independent and highest value. Ship it alone first rather than batching.

## Related tickets

- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--installer-sessionstart-hook-duplicate-registration.md`
- `ai/product/bugs/installer/open-tickets/2026-07-04--cc-mini--boot-hook-update-in-place-never-persists.md` (PR #1086)
- `ai/product/bugs/guard/2026-07-04--cc-mini--no-blessed-recipe-for-live-settings-remediation.md` (PR #1086)
- `ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md`
