---
name: review-loop
description: Run a bounded review-and-fix loop with fresh, read-only reviewer subagents.
license: MIT-0
---

# Review Loop

Set `max_rounds` to the user's positive integer, or `3` when no limit is given.

## Each round

1. Start one fresh subagent with `fork_turns: "none"` and `$review-agent`. The reviewer may inspect code, tests, and call sites, but must only review. Wait patiently for its conclusion; unless the reviewer is confirmed to be in an abnormal state, do not send prompts to rush or wrap up the review.
2. Ask the reviewer to focus on Critical, Important, and clearly worthwhile issues. Record Minor issues as non-blocking. Every finding must include:
   - Issue
   - File/line number
   - Reason
   - Recommendation
3. Close the subagent after its report. If there are no findings, only Minor findings, or all findings are not accepted, finalize. Otherwise, verify each finding yourself:
   - Record invalid or unaccepted findings as `Not accepted` with the reason.
   - If an implementation subagent owns the change, delegate accepted fixes to it; otherwise fix them yourself. In either case, rerun the relevant tests after each fix.
   - If at least one fix was made and `round < max_rounds`, start a different fresh reviewer for the next round.
4. On the final configured round, apply and test accepted fixes but do not start another reviewer. Report any resulting review boundary or residual risk.

## Finalize

Summarize the implementation, each round's findings and decisions, fixes, verification results, unverified items, and remaining risks.
