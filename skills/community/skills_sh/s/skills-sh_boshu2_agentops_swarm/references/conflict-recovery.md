# Merge Conflict Recovery Pattern

> When parallel workers produce conflicting changes, capture context and retry intelligently.

## Problem

Parallel workers in the same wave can produce merge conflicts when:
- File manifests were incomplete (worker touched unexpected files)
- Two workers independently refactored the same utility
- Import changes collide (both add imports to the same file)
- Test fixtures overlap

Current behavior: conflict = wave failure. No context preserved for retry.

## Solution: Eviction + Context Capture

When a merge conflict occurs, capture the full context before evicting the conflicting change:

### Step 1: Detect Conflict
```bash
# After worker completes, attempt merge
git merge --no-commit <worker-branch> 2>&1
if [ $? -ne 0 ]; then
    CONFLICT_FILES=$(git diff --name-only --diff-filter=U)
    echo "Merge conflict in: $CONFLICT_FILES"
fi
```

### Step 2: Capture Eviction Context
```bash
mkdir -p .agents/crank/conflicts

cat > ".agents/crank/conflicts/wave-${wave}-${TASK_ID}.json" <<EOF
{
  "wave": ${wave},
  "task_id": "${TASK_ID}",
  "conflict_files": $(echo "$CONFLICT_FILES" | jq -R . | jq -s .),
  "worker_branch": "${WORKER_BRANCH}",
  "worker_diff_summary": "$(git diff --stat ${BASE_SHA}..${WORKER_BRANCH})",
  "conflicting_with": "${MERGED_TASKS}",
  "timestamp": "$(date -Iseconds)",
  "resolution_strategy": null
}
EOF

# Abort the failed merge
git merge --abort
```

### Step 3: Classify Conflict

| Type | Signal | Resolution |
|------|--------|-----------|
| **Import collision** | Only import blocks conflict | Auto-resolve: combine imports |
| **Utility overlap** | Both created similar helper function | Manual: pick one, delete other |
| **Test fixture** | `testdata/` or `_test.go` conflicts | Auto-resolve: merge both fixtures |
| **Logic conflict** | Business logic in same function | Re-queue as serialized sub-wave |
| **Formatting** | Whitespace or formatting-only | Auto-resolve: run formatter after merge |

### Step 4: Retry with Context

For the evicted task, re-queue with conflict context:

```
TaskCreate(
  subject="RETRY: ${TASK_SUBJECT}",
  description="${ORIGINAL_DESCRIPTION}\n\n---\n
CONFLICT CONTEXT (from wave ${wave}):
Your prior attempt conflicted with ${CONFLICTING_WITH} on files: ${CONFLICT_FILES}.

The other worker's changes have been merged. Your changes were evicted.

When re-implementing:
1. Read the current state of ${CONFLICT_FILES} (they now contain the other worker's changes)
2. Integrate your changes without overwriting theirs
3. If you need a utility they already created, use it instead of duplicating

Prior diff summary of your work:
${WORKER_DIFF_SUMMARY}"
)
```

## Integration with Swarm

### Pre-Spawn Conflict Prevention
Before spawning workers, the conflict matrix from `swarm/SKILL.md` catches overlapping file manifests. This reference handles the cases that slip through (incomplete manifests, unexpected file touches).

### Post-Wave Recovery Flow
```
Wave N workers complete
  │
  ├── Merge worker 1 → SUCCESS
  ├── Merge worker 2 → CONFLICT with worker 1
  │   ├── Capture eviction context
  │   ├── Classify conflict type
  │   ├── If auto-resolvable → resolve + merge
  │   └── If not → evict + re-queue for next wave
  │
  └── Continue with remaining workers
```

### Budget
Each task gets **max 1 conflict retry**. If the retry also conflicts, classify as DECOMPOSE (needs manual split).

## Metrics

Track in wave checkpoint:
```json
{
  "conflicts": {
    "count": 1,
    "auto_resolved": 0,
    "evicted_requeued": 1,
    "tasks_affected": ["ag-1234"]
  }
}
```

High conflict rates (>30% of wave tasks) signal poor file manifest quality. Log warning and suggest tighter pre-spawn conflict detection.
