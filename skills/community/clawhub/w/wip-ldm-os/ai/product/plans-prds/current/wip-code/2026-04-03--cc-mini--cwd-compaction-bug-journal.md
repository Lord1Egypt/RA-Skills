# Journal: The CWD Compaction Bug

**Date:** April 3, 2026 (Day 63)
**Author:** CC Mini + Parker
**Severity:** Critical. Causes cascading context loss.

## What happened

During a marathon session building the Kaleidoscope demo (wip.computer/demo/), context compaction triggered mid-session. After compaction, Claude Code's internal CWD silently shifted from the workspace root (`~/wipcomputerinc/`) to the repo being worked on (`~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/`).

The user's shell CWD was unaffected. Only Claude Code's internal state changed. There was no visible indication that the CWD had moved.

## The impact

After the CWD shifted, Claude Code lost all project context:
- Forgot the product name (Kaleidoscope) that had been decided in the session
- Forgot the footer format that had been specified multiple times
- Forgot agent auth decisions made earlier in the session
- Kept rebuilding things wrong, requiring Parker to re-explain from scratch
- Made 10+ incorrect iterations on the agent page because context was gone

Parker spent hours correcting mistakes that wouldn't have happened if the context files had been available. When he finally asked "what is pwd?" and we discovered the CWD had moved to the repo, everything clicked.

## Why it matters

Claude Code loads CLAUDE.md files based on the working directory. The cascade walks up from CWD to find project-level instruction files. When CWD is at the workspace root, it finds the comprehensive CLAUDE.md (366 lines) with all project context. When CWD is at a repo that has no CLAUDE.md, the cascade finds nothing at the repo level and may not properly resolve the parent workspace's CLAUDE.md.

This means:
1. **After compaction:** CWD shifts to last bash command location. If that's a repo with no CLAUDE.md, context is lost.
2. **On iOS/phone (remote):** Session opens in the repo directory. Same problem.
3. **When opening a repo directly:** `claude` from a repo directory. No CLAUDE.md. Blind.

## How we discovered it

Parker noticed that after /exit, his shell was still at `~/wipcomputerinc/` (where he launched Claude Code), but during the session, Claude Code's displayed CWD at the top of the interface showed the repo path. The shell never moved. Claude Code's internal state did.

He said: "When I exited, my PWD was WIP Computer Inc. But Claude was showing me the repo." That's the smoking gun. The user's shell and Claude Code's internal CWD diverged silently.

## The root cause

The Bash tool documentation says: "The working directory persists between commands." During the session, multiple `cd` commands ran to navigate to the repo for git operations (`git pull`, `scp`, etc.). Each `cd` shifted the Bash tool's persistent CWD. After compaction, this shifted CWD became the effective session CWD, but the CLAUDE.md cascade may not reload from the new location, or if it does, the new location has no CLAUDE.md.

## The fix (our side)

Add CLAUDE.md to every repo (Level 3 of the three-level cascade). Each repo's CLAUDE.md says what the repo does and points to the workspace CLAUDE.md for full context. This way, no matter where the CWD ends up, there's always a CLAUDE.md available.

See: `2026-04-03--cc-mini--claude-md-master-plan.md`

## The fix (Anthropic's side)

Two possible fixes:
1. **Preserve the original CWD across compaction.** The CWD at session start should be the CWD after compaction, regardless of where bash commands navigated during the session.
2. **Reload CLAUDE.md cascade after compaction.** If the CWD does shift, at minimum reload the CLAUDE.md files from the new location so the agent has whatever context is available.

## Recommendation to Anthropic

This should be filed as a bug. The CWD shift after compaction is silent, invisible to the user, and causes cascading failures. The user has no way to know it happened until they notice the agent has lost all context. The only diagnostic is checking `pwd` manually, which most users won't think to do.

The impact scales with project complexity. For a simple single-repo project, this might not matter. For a multi-repo workspace with layered CLAUDE.md files, boot sequences, and shared context files, the CWD shift breaks everything.

## Evidence

- Session transcript: previous session (compacted, continued into this one)
- 10+ incorrect iterations on agent.html after compaction
- Parker's observation: shell CWD unchanged, Claude Code CWD shifted
- Confirmed by checking `pwd` at the end of the session vs the beginning
