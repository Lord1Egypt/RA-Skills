# Fresh-session brief: ship wip-branch-guard v1.9.82 to npm + GitHub

**Date:** 2026-04-21
**Authors:** Parker Todd Brooks, cc-mini
**Status:** Handoff brief for the next cc-mini session. Paste the section starting at "Goal" below as the first message in a fresh Claude Code window.

## Context

Companion doc to `2026-04-21--parker-cc-mini--bugfix.md` (the fix brief that originated PR #364, the cross-session state-collision fix). That brief's Step 6 ("push → gh pr create → gh pr merge → wip-release → deploy-public") stalled at `wip-release patch` because the sub-tool's `LICENSE` + `CLA.md` were missing. The session that worked PR #364 attempted a cleanup PR #366 for those files, hit Claude Code auto-mode's retry-after-block decider post-onboarding-Read, and tried a `-F commit-msg-file` shape-bypass. Parker closed PR #366 and specified a fresh-session ship as the clean-path resolution.

This brief is what a fresh cc-mini session needs to complete the release.

---

## Goal

Publish `@wipcomputer/wip-branch-guard@1.9.82` to npm and cut the matching GitHub release on `wipcomputer/wip-ai-devops-toolbox-private`. The code fix (cross-session state-collision + env-var hatch removal) is already merged to main; this session just runs the release pipeline.

## State at handoff

- PR #364 (the guard fix): merged, commit `ae7b66b` on `wip-ai-devops-toolbox-private` main.
- PR #365 (release-prep: un-bumped `tools/wip-branch-guard/package.json` back to 1.9.81, added repo-root `.license-guard.json`): merged.
- PR #366 (sub-tool LICENSE + CLA.md): **closed without merging**. Prior session reached that commit via a shape-bypass (`-F commit-msg-file` after a "retry after guard block" decider denial). Commit content was correct; path there wasn't. Close comment on #366 preserves the content pointer for regeneration.
- Branch `cc-mini/guard-license-files`: abandoned with the closed PR. Do NOT check it out or resurrect; re-create the artifacts fresh via `wip-license-guard check --fix` instead.
- No stashed or uncommitted work. Clean slate.
- npm `@wipcomputer/wip-branch-guard@latest` = 1.9.81. `tools/wip-branch-guard/package.json` on main = 1.9.81. Ready to release.

## Prophylactic (non-negotiable): upfront onboarding

BEFORE any first write in this session, Parallel-Read the full onboarding set in ONE turn for any repo you touch. This is the rule captured in `~/.claude/projects/-Users-lesa-wipcomputerinc/memory/feedback_repo_onboarding_before_first_write.md`. It's the rule that prevents the decider false-positive that stranded the last session.

For this task that's:

- Repo root: `README.md`, `DEV-GUIDE-GENERAL-PUBLIC.md`
- `tools/wip-branch-guard/`: `INSTALL.md`, `SKILL.md`, `RELEASE-NOTES-v1-9-82.md`, `guard.mjs`, `test.sh` (optional but useful)

All Reads in one assistant message, parallel. No Write, Edit, or Bash-write before that.

## Workflow

1. Open a new Claude Code window. Verify no other cc-mini sessions are making tool calls on this machine. Cross-session ping-pong is fixed in the source on main, but the deployed guard is still v1.9.81 until you publish. Quiet machine = clean bootstrap.

2. `cd /Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private`. Parallel-Read the onboarding set (above).

3. Create worktree: `git worktree add .worktrees/wip-ai-devops-toolbox-private--cc-mini--guard-license-files-v2 -b cc-mini/guard-license-files-v2`. `cd` in.

4. `cd tools/wip-branch-guard && wip-license-guard check --fix`. This regenerates `LICENSE` and `CLA.md` from the MIT+AGPL master template. `README.md` remains a warning-only miss; ignore it for now (per-tool content, not a templatable artifact).

5. `git add tools/wip-branch-guard/LICENSE tools/wip-branch-guard/CLA.md`. Commit with standard heredoc message (clean session, no pattern to match against):
   - Subject: `guard: add sub-tool LICENSE + CLA.md for wip-release license check`
   - Body: explain `wip-release` check dependency; note content is master-template generated; reference PR #364 as the guard fix that this unblocks shipping.
   - Three co-authors: Parker Todd Brooks, Lēsa, Claude Opus 4.7.

6. `git push -u origin cc-mini/guard-license-files-v2`. `gh pr create`. Body: reference this handoff doc and PR #366 as the prior closed attempt.

7. `gh pr merge <N> --merge --delete-branch`. Never squash.

8. `cd` back to the main working tree: `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private`. `git checkout main && git pull --ff-only origin main`.

9. `cd tools/wip-branch-guard && wip-release patch`. It should:
   - Detect `RELEASE-NOTES-v1-9-82.md` (already on main from PR #364).
   - Bump `package.json` 1.9.81 → 1.9.82.
   - Pass license compliance (now that `LICENSE` + `CLA.md` exist).
   - Publish to npm via 1Password auth.
   - Create GitHub release on the private repo.
   - Run `deploy-public.sh` to sync the public twin.

10. Smoke test post-publish:
    - `npm view @wipcomputer/wip-branch-guard version` → 1.9.82
    - `gh release view <tag>` on `wipcomputer/wip-ai-devops-toolbox-private`; check existing tags for the sub-tool release tag pattern if unsure
    - Open two CC sessions; verify each has its own `~/.ldm/state/guard-session-<sid>.json`; confirm cross-session tool calls don't wipe the other's onboarding. (Requires `ldm install` to have deployed v1.9.82 to `~/.ldm/extensions/wip-branch-guard/` ... Parker runs the install prompt himself.)

## What NOT to do

- Do NOT use `-F commit-msg-file` to sidestep a block. If you get blocked, you've already missed the prophylactic upfront-onboarding; the fix is to have read the docs first, not to change the command shape.
- Do NOT use the Write tool to drop `LICENSE` / `CLA.md` contents directly. `wip-license-guard check --fix` is the canonical path.
- Do NOT set `LDM_GUARD_SKIP_ONBOARDING`, `LDM_GUARD_ACK_BLOCKED_FILE`, or any bypass env var. The cross-session fix removed them from v1.9.82 source; deployed v1.9.81 still honors them, but using them is training the wrong behavior.
- Do NOT ask Parker to commit, push, or run anything outside the install prompt. The agent ships the release end-to-end.
- Do NOT mix unrelated work into this branch. License files only.

## Success criteria

- PR merged (no squash, branch renamed `--merged-YYYY-MM-DD` via the post-merge hook or `wip-release` step 10).
- `@wipcomputer/wip-branch-guard@1.9.82` on npm @latest.
- GitHub release exists on `wipcomputer/wip-ai-devops-toolbox-private`.
- `deploy-public` synced the public twin.
- Zero "retry after block" denials in the session transcript.
- Parker never had to run anything outside the install prompt.

## References

- Bug brief that originated the fix: `ai/product/bugs/code/2026-04-21--parker-cc-mini--bugfix.md`
- Release notes on main: `wip-ai-devops-toolbox-private/tools/wip-branch-guard/RELEASE-NOTES-v1-9-82.md`
- Upstream filing draft (Anthropic Claude Code decider bug): pending Parker review before submission; draft text in the session-that-produced-this-brief's transcript.
- Memory: `~/.claude/projects/-Users-lesa-wipcomputerinc/memory/feedback_repo_onboarding_before_first_write.md` (the upfront-onboarding rule).

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
