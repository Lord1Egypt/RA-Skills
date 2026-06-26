# Session Resumption: Picking Up Mid-Mission

Use when a session is interrupted (context limit, crash, timeout) and work must continue.

1. **Auto-recovery (preferred):** Run `python3 .claude/skills/nelson/scripts/nelson-data.py recover --missions-dir .nelson/missions`. If an active mission is found, the command outputs a structured recovery briefing with fleet status, handoff packets, pending tasks, and recommended actions. Use this output to resume directly, skipping manual directory selection.
2. **Manual recovery (fallback):** If auto-recovery is unavailable, and you know the SESSION_ID, read `.nelson/.active-{SESSION_ID}` to recover the mission directory path and set it as `{mission-dir}`. If you cannot determine your SESSION_ID (e.g., after a full restart), list `.nelson/missions/` and present the options to the user for selection. Set the chosen directory as `{mission-dir}`.
3. **Recover state from structured data:**
   - If `{mission-dir}/fleet-status.json` exists, read it for quick state recovery (task progress, hull status, budget, blockers).
   - If `{mission-dir}/turnover-briefs/` contains `.json` handoff packets, read the most recent packet for each ship to recover per-ship task state. These provide structured data about completed subtasks, partial outputs, blockers, and next steps.
   - If `{mission-dir}/mission-log.json` exists, read it for full event history — task completions, relief chains, standing order violations, and admiral decisions.
   - These JSON files provide faster, more reliable state recovery than re-parsing quarterdeck report prose.
   - **Fallback:** If no JSON files are present, read `{mission-dir}/quarterdeck-report.md` to establish last known state.
   - **Sub-fallback:** If the canonical `quarterdeck-report.md` is also missing (e.g. crash during report rotation), check for `{mission-dir}/quarterdeck-report-N.md` files (where N is a number). Use the file with the highest N value — it contains the most recent checkpoint data. The same fallback applies to `captains-log.md` / `captains-log-N.md`.
   - The recovery briefing surfaces a "Fleet status may be stale" warning when `last_updated` is older than 10 minutes or when `mission-log.json` has events newer than `last_event_id`. When the warning appears, verify in-progress task state against handoff packets and file state before resuming — do not trust the cached progress counters.
4. List all tasks and their statuses: `pending`, `in_progress`, `completed`.
5. For each `in_progress` task, verify partial outputs against the task deliverable. If a handoff packet exists for the task, use its `state.partial_outputs` and `state.next_steps` to guide verification.
6. Discard any unverified or incomplete outputs that cannot be confirmed correct.
7. Re-issue sailing orders with the original mission outcome and updated scope reflecting completed work.
8. Re-form the squadron at the minimum size needed for remaining tasks.
9. Resume quarterdeck rhythm from the next scheduled checkpoint.

**Safe compaction windows.** State is fully persisted at every phase boundary: after Sailing Orders (Step 1), after the Estimate (Step 2), after the Battle Plan is drafted to disk (Step 3), after Formation (Step 4), and at every quarterdeck checkpoint (Step 6). The one unsafe window is *inside* Step 5: between the user granting permission and the admiral logging `permission_granted` + advancing to UNDERWAY + spawning agents — that whole sequence is a single tightly coupled turn.
