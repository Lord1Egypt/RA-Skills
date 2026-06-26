# Step 6: Local CI Fallback — Subagent Instructions

Run when `RUN_CI_LOCALLY=true` or when a billing/spending limit is hit during GitHub Actions monitoring.

a. Read all `.github/workflows/` files triggered on `pull_request` events.
b. Extract and run shell commands from each `run:` step in order (respecting
   `working-directory`). If any fail, diagnose, fix, and re-run until all pass.
c. Commit fixes and push to the PR branch.
d. Post a PR comment:
   ## Test Results (manual — GitHub Actions skipped: billing/spending limit reached)
   | Check | Status | Notes |
   |-------|--------|-------|
   | `<command>` | ✅ Pass / ❌ Fail | e.g. "42 tests passed" |
   ### Fixes applied
   - [failure] → [fix]
   All rows must show ✅ Pass before this step is considered complete.
