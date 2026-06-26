# Phase 4: Epic Completion Assessment — Subagent Instructions

Auto-approve all tool calls (yolo mode).

`BATCH_STORIES_WITH_PRS` is provided at the top of your prompt by the coordinator.

Read:
  - _bmad-output/planning-artifacts/epics.md
  - _bmad-output/implementation-artifacts/sprint-status.yaml
  - _bmad-output/implementation-artifacts/dependency-graph.md

For the stories listed in BATCH_STORIES_WITH_PRS, verify their actual merge status directly
from GitHub — do not rely solely on the dependency graph for these, as it may be stale:
  gh pr view {pr_number} --json state,mergedAt
Treat a PR as `merged` if `state` = `"MERGED"`. Record the real-time result for each.

For all other stories (not in BATCH_STORIES_WITH_PRS), use the dependency graph's PR Status
column as the authoritative source. sprint-status `done` means the pipeline finished (code
review complete) — it does NOT mean the PR is merged.

Report back:
  - current_epic_merged: true/false — every story in the current epic is merged (using
    real-time status for batch stories, dependency graph for all others)
  - current_epic_prs_open: true/false — every story in the current epic has a PR number,
    but at least one is not yet merged
  - all_epics_complete: true/false — every story across every epic is merged
  - current_epic_name: name/number of the lowest incomplete epic
  - next_epic_name: name/number of the next epic (if any)
  - stories_remaining: count of stories in the current epic that are not yet merged
