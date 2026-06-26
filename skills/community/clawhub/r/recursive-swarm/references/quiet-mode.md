# Quiet child execution pattern

Use this pattern when the user wants minimal channel noise.

## Goal

Let child sessions do the work without posting routine completion chatter back to the user channel. The parent/orchestrator should collect the results and send one final merged answer.

## Default policy

For routine child runs:
- keep child completion **silent**
- save results in child `result.md`, session history, or other explicit artifacts
- have the child reply exactly `ANNOUNCE_SKIP` during the announce step
- keep the child session available until the parent harvests the result

Only allow a child announce message when:
- the child is blocked
- the child needs approval
- the child hit an error that must be surfaced immediately
- the child itself is intentionally responsible for final user-facing delivery

## Recommended parent instruction snippet

Use language like this when spawning routine child runs:

> Do the work, save your findings clearly in artifacts and/or your final session output, and during the announce step reply exactly `ANNOUNCE_SKIP` unless you are blocked, need approval, or have been explicitly designated as the final user-facing delivery step.

## Parent responsibilities

The parent/orchestrator should:
- track which child session owns which subtask
- wait for completion or check history on demand
- harvest child results before cleanup
- merge results upward
- send the single user-facing final answer

## Caution

Quiet children are useful only if the parent actually harvests their outputs. Do not delete or clean up child sessions before collecting what you need.
