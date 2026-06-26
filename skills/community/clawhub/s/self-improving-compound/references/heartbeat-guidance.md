# Heartbeat guidance

This reference describes how to integrate the self-improving memory lifecycle into a periodic heartbeat without creating noise or destructive churn.

## Design principle

Heartbeat should be **conservative and transparent**. Most runs should do nothing. When they do act, they should only perform safe, reversible moves.

## Recommended heartbeat snippet

Add this to your workspace `HEARTBEAT.md` or equivalent recurring-check file:

```markdown
## Self-Improving Memory Check

- Run `python3 scripts/learnings.py --root <workspace> maintain --dry-run`
- If the report shows only healthy entries or minor recommendations, return `HEARTBEAT_OK`
- If the report shows clearly safe moves (e.g., stale HOT entries with unambiguous WARM targets), you may run `maintain --apply` automatically
- If the report shows ambiguous conflicts, promotion candidates, or missing metadata, log a recommendation and ask the user instead of applying
- `maintain` updates `learning/heartbeat-state.md` with the last run timestamp and result
```

## State file template

Create `learning/heartbeat-state.md` to track heartbeat activity:

```markdown
# Self-Improving Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```

## Safety rules for heartbeat automation

1. **Prefer `maintain --dry-run`** in automated contexts.
2. **Only auto-apply** when:
   - The lifecycle update is unambiguous (e.g., an `admitted` entry with `Last-Seen` 60 days ago).
   - No promotion candidates are flagged.
   - No conflicts are detected.
3. **Never auto-apply** when:
   - Metadata is missing or incomplete.
   - A conflict is detected between namespaces.
   - A promotion candidate has `Recurrence-Count >= 3` (ask user first).
   - The target namespace is unclear.
4. **Preserve source transparency**: after any promotion/export, the SQLite entry should retain `Status` and `Promoted-To` metadata so future readers can trace the history.

## Minimal example

```bash
# In heartbeat or cron script
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"

# Dry-run review
REPORT=$(python3 scripts/learnings.py --root "$WORKSPACE" maintain --format json)
STALE_COUNT=$(echo "$REPORT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('stale_hot',[])))")

if [ "$STALE_COUNT" -eq 0 ]; then
    echo "HEARTBEAT_OK"
else
    echo "HEARTBEAT_RECOMMENDATIONS: $STALE_COUNT stale entries found"
    echo "$REPORT"
fi
```

## Integration with OpenClaw

If your workspace uses an OpenClaw `HEARTBEAT.md`, add the snippet above under a `## Self-Improving Memory Check` heading. The skill will then participate in the existing heartbeat flow without adding new files outside `learning/`.
