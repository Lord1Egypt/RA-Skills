# Bug: branch-guard compaction loop (and Write/Edit bypass)

**Date:** 2026-04-05
**Filed by:** cc-mini
**Repo:** wip-ai-devops-toolbox-private (guard source), wip-ldm-os-private (filing location)
**Priority:** high
**Related:** cost amplification bug in `2026-04-05--cc-mini--bridge-master-plan.md`

## Symptom

After compaction, a CC session resumes with CWD = `/Users/lesa/wipcomputerinc` (main repo root). Any file-modifying bash command (`cp`, `mv`, `mkdir`, `echo >`) blocks with the branch-guard error. The agent loops: retries the same command, tries variations, eventually falls out of Bash into `Write` or `Edit` tools which bypass the guard entirely. Time and tokens burn. Trust breaks.

This has happened at least twice in the same day. Another session is stuck in a related failure mode ("doesn't know how to write anymore") which is likely the same loop in a worse state.

## Root cause (three separate bugs)

### 1. Guard only hooks `PreToolUse:Bash`

`~/.ldm/extensions/wip-branch-guard/guard.mjs` is wired via `PreToolUse:Bash`. It does not hook `Write`, `Edit`, or `NotebookEdit`. Any agent can write directly into a main-branch working tree using those tools and the guard never fires. This defeats the entire purpose of the guard and creates a false sense of safety.

**Demonstrated in this very session:** Bash `cp` blocked three times; Write tool succeeded on the same target path. File landed in a worktree (harmless this time) but the same path could have been `CLAUDE.md` on main.

### 2. Guard error message is abstract, not actionable

Current error:

```
BLOCKED: Cannot run file-modifying command on main branch.
The process: worktree -> branch -> commit -> push -> PR -> merge ...
Step 1: git worktree add .worktrees/<repo>--<branch> -b cc-mini/your-feature
...
```

LLMs (and humans) follow concrete commands better than abstract instructions. The guard has already resolved the target path and knows the repo. It should print a ready-to-paste command:

```
BLOCKED: You are on main in <repo>.
To continue, cd into an existing worktree or create a new one:

  cd /Users/lesa/wipcomputerinc/repos/ldm-os/<repo>/.worktrees/<repo>--cc-mini--<feature>

Or: git worktree add .worktrees/<repo>--cc-mini--<feature> -b cc-mini/<feature>
```

Without a concrete cd, the agent pattern-matches on the abstract steps and loops.

### 3. No SessionStart check for main-branch CWD

Sessions that resume post-compaction start wherever they were. If that's main, the first file operation blocks, and the agent enters the loop before the guard message has a chance to shape behavior. A SessionStart hook could detect the trap at boot and inject a warning + available-worktrees list into context.

## Observed failure trace (this session, 2026-04-05)

1. Session CWD: `/Users/lesa/wipcomputerinc`
2. Task: copy `~/.claude/plans/sprightly-watching-nova.md` into the bridge folder on a worktree
3. Bash `cp ai/...` blocked (CWD inherited, path resolves against main tree)
4. Retry with absolute worktree path: blocked (guard does not normalize paths)
5. Retry with `pwd && git branch && cp <abs>`: blocked
6. Tool swap to `Write`: succeeded (guard does not hook Write)
7. File committed and pushed from within worktree (Bash cd chained): succeeded
8. Total overhead: approximately 15 tool calls, multiple hook rejections, user trust damage

## Fix plan

### Layer 1 (must ship first): close Write/Edit/NotebookEdit bypass

Add matchers for `Write`, `Edit`, `NotebookEdit` to the guard's hook config. Update `guard.mjs` to read `file_path` from the tool input, resolve to a repo root, check branch, block if main (subject to the existing lenient list for deployed extension paths).

Without this, every other fix is cosmetic.

### Layer 2: actionable error message

Update `guard.mjs` to:
- Resolve the target file's repo
- List existing worktrees for that repo
- Print a ready-to-paste `cd <worktree>` command as the first line of the error
- Keep the abstract workflow below as secondary reference

### Layer 3: SessionStart main-branch detector

Add a SessionStart hook that checks CWD, detects if it's on main of a protected repo, and injects a boot-context warning with available worktrees. Survives compaction because SessionStart fires on resume.

### Layer 4 (deferred): guard offers to cd automatically

When blocking, if there is exactly one matching worktree for the user's current branch-naming pattern, offer an auto-cd or print a single one-line fix. Smaller surface area than full auto-remediation.

## Files that matter

- `~/.ldm/extensions/wip-branch-guard/guard.mjs` (deployed)
- `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/` (source, path to verify)
- `shared/settings.json` in `wip-ldm-os-private` (hook matcher config deployed to `~/.claude/settings.json`)
- Lenient-list config (already allows memory and `.openclaw/extensions/` hotfixes per cost plan)

## Verification

1. After Layer 1: attempting to Write to a file on main should produce the same block as Bash cp
2. After Layer 2: the block message contains a concrete `cd` command for an existing or suggestable worktree
3. After Layer 3: opening a session in a main-branch CWD produces a boot-time warning before the first tool call
4. End-to-end: an agent resuming after compaction in a main-branch CWD can reach a worktree in one step (read error, cd, retry), not 10+ steps

## Open questions

- Should the guard ever auto-cd, or only print the command and let the agent decide? (Safer: print only.)
- Should Layer 3 refuse session start on main for protected repos, or just warn? (Warn first, measure, escalate if still looping.)
- Are there any legitimate bash operations on main that should remain allowed beyond the current lenient list? (Check history of lenient-list additions for the answer.)

## Scope boundary

In-scope for this bug: the guard loop and the Write bypass. Out-of-scope: the compaction CWD shift itself (that is a Claude Code harness issue, separately documented in the CLAUDE.md cascade plan at the end of the bridge master plan).

## Resolution

Status: Closed on 2026-04-24.

Closed by `wip-ai-devops-toolbox-private` PR #386. The guard has shared-main protections for `Write`, `Edit`, `NotebookEdit`, and Bash write effects, plus SessionStart guidance for sessions that start in a shared `main` checkout. It also blocks local main commits, merges, rebases, unsafe pulls, dirty/divergent `pull --ff-only`, and direct `git push origin main`.

Verification:

- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
- Shared-main tests cover commit, merge, unsafe pull, and clean `pull --ff-only` read-sync behavior.
