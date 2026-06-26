# Auto-Sync Checklist

Use this whenever one of these happens:
- a new skill is installed
- an existing skill is updated
- `shared-memory-os` changes
- workspace memory governance rules change

## Sync steps

### 1. Re-check the changed skill
- Is it unrelated / adjacent / conflicting?
- Does it now need a shared-memory note?
- Did it stop needing one?

### 2. Update governance records
- `memory/intake-log.md`
- `memory/conflict-log.md` if conflict status changed
- `memory/promotion-log.md` if a candidate became rule
- `memory/pattern-candidates.md` if a new candidate appeared

### 3. Update routing docs if needed
- `memory/index.md`
- `memory/README.md`
- `memory/routines.md`
- `HEARTBEAT.md`

### 4. Update dashboard counts
- intake entries
- promotion entries
- conflict entries
- open conflicts
- pattern candidates

### 5. Sanity check
- Did the shared-memory model stay lean?
- Did we accidentally create parallel memory guidance?
- Did we over-edit unrelated skills?

## Principle
Sync the smallest surface necessary. Do not create churn just because something changed.
