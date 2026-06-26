# Monitor Pattern

Use this pattern when `MONITOR_SUPPORT=true`. It covers two use cases in BAD: CI status polling (Step 6) and PR-merge watching (Phase 4 Branch B). The caller supplies the poll script and the reaction logic.

> **Requires Claude Code v2.1.98+.** Uses the same Bash permission rules. Not available on Amazon Bedrock, Google Vertex AI, or Microsoft Azure Foundry — set `MONITOR_SUPPORT=false` on those platforms.

## How it works

1. **Write a poll script** — a `while true; do ...; sleep N; done` loop that emits one line per status change to stdout.
2. **Start Monitor** — pass the script to the Monitor tool. Claude receives each stdout line as a live event and can react immediately without blocking the conversation.
3. **React to events** — on each line, apply the caller's reaction logic (e.g. CI green → proceed; PR merged → continue).
4. **Stop Monitor** — call stop/cancel on the Monitor handle when done (success, failure, or user override).

## CI status polling (Step 6)

Poll script (run inside the Step 6 subagent):
```bash
GH_BIN="$(command -v gh)"
while true; do
  "$GH_BIN" run view --json status,conclusion 2>&1
  sleep 30
done
```

React to each output line:
- `"conclusion":"success"` → stop Monitor, report success
- `"conclusion":"failure"` or `"conclusion":"cancelled"` → stop Monitor, diagnose, fix, push, restart Monitor
- Billing/spending limit text in output → stop Monitor, run Local CI Fallback

## PR-merge watching (Phase 4 Branch B)

The coordinator fills in `BATCH_PRS` (space-separated PR numbers from the Phase 0 pending-PR report) before starting Monitor.

Poll script (run by the coordinator):
```bash
GH_BIN="$(command -v gh)"
BATCH_PRS="101 102 103"   # coordinator replaces with actual pending PR numbers
ALREADY_REPORTED=""
while true; do
  MERGED_NOW=$(cd /path/to/repo && "$GH_BIN" pr list --state merged --json number \
    --jq '.[].number' 2>/dev/null | tr '\n' ' ' || echo "")
  ALL_DONE=true
  for PR in $BATCH_PRS; do
    if echo " $MERGED_NOW " | grep -q " $PR "; then
      if ! echo " $ALREADY_REPORTED " | grep -q " $PR "; then
        echo "MERGED: #$PR"
        ALREADY_REPORTED="$ALREADY_REPORTED $PR"
      fi
    else
      ALL_DONE=false
    fi
  done
  [ "$ALL_DONE" = "true" ] && echo "ALL_MERGED" && break
  sleep 60
done
```

> **Note:** Replace `/path/to/repo` with the absolute path to the project repository. Common mistakes: (1) `gh pr list` defaults to `--state open` — merged PRs are invisible without `--state merged`; (2) `gh` has no `-C` flag (unlike `git`) — use `cd` instead; (3) the Monitor shell inherits a stripped PATH — `gh` must be resolved with `command -v gh` before the script runs, not looked up by name inside it.

React to each output line:
- `MERGED: #N` → log progress (e.g. `✅ PR #N merged — waiting for remaining batch PRs`); keep Monitor running
- `ALL_MERGED` → CronDelete the fallback timer, stop Monitor, run Pre-Continuation Checks, re-run Phase 0

## If `MONITOR_SUPPORT=false`

- **CI polling:** use the manual `gh run view` loop in Step 6 (see Step 6 fallback path in SKILL.md).
- **PR-merge watching:** use the CronCreate-only Timer Pattern in Phase 4 Branch B (see fallback path in SKILL.md).
