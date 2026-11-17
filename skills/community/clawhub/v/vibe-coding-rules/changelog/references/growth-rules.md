# Growth Detection Rule Definitions

## Trigger Conditions

Growth detection triggers when any of the following is true:

1. **Same file modified > 1 time within the same session** (fix iteration)
2. **Same file appears in last 3 changelog entries** (high-churn file)
3. **User says "bug again", "still wrong", "fixed this before"** in same session

## Confidence Calculation

```
New observation confidence = 1 (first sighting)

Each reoccurrence:
  confidence += 1

User rejects the suggestion (ignores when modifying / says "skip this"):
  confidence -= 2

False positive (rule fires but actual cause is different):
  confidence -= 3
  false_positive_counter += 1
```

## Promotion / Demotion / Retirement Thresholds

Read from `pipeline.json` `selfGrowth.confidenceThresholds`:

| Threshold | Action |
|:--|:--|
| confidence ≥ 3 | Tier 0 Observation → Tier 1 [SOFT] Soft Rule |
| confidence ≥ 5 | Tier 1 [SOFT] → Tier 2 [HARD] Hard Rule |
| confidence < 1 | Tier 1 → demote back to Tier 0 |
| false_positive_count ≥ 3 | Tier 2 → retire (move to retired.md) |
| user rejects 3 consecutive times | Tier 1/2 → demote to Tier 0 or retire |

## Growth Detection Execution Steps

Executed in changelog Skill Step 0:

1. **Scan current session**: Review all `replace_in_file` / `write_to_file` operations in this session
2. **Identify fix iterations**: Same file modified multiple times + bug fix keywords present ("fix", "bug", "error", "still broken") before and after changes
3. **Extract bug pattern**: Distill general pattern from user feedback and fix content
   - E.g. "events lost after innerHTML" → pattern: dynamic DOM needs event delegation
   - E.g. "0 treated as falsy" → pattern: numeric checks must not use ||
4. **Match against existing observation pool**:
   - Exists → confidence +1
   - Not exists → create new observation entry, confidence = 1
   - **New (V2.2)**: Record `last_triggered` timestamp for staleness tracking
5. **Check promotion/demotion thresholds**: Auto-operate per threshold rules above
6. **Write to corresponding files**: observations.md / self-check-full.md / retired.md / growth-log.md

---

## Rule Lifecycle & Anti-Bloat (V2.2)

> **Why this exists**: Without cleanup, rules accumulate indefinitely. A 6-month-old project could have 100+ [SOFT] rules, bloating every self-check session. This section defines the automatic cleanup that keeps the rule set lean and relevant.

### Anti-Bloat Principles

1. **Staleness is a signal**: A rule that hasn't fired in months is probably no longer relevant to the codebase's current state
2. **Hard cap prevents context bloat**: Agent context is limited — too many rules means the important ones get diluted
3. **Graceful degradation, not deletion**: Demoted rules go back to the observation pool, not into the void

### Step 0.5: Anti-Bloat Check (executed AFTER growth detection, BEFORE changelog write)

Execute `_runAntiBloatCheck()`:

#### 1. Staleness Sweep (SOFT rules)

For each `[SOFT]` rule, check `growth-log.md` for `last_triggered` timestamp:
- If `last_triggered` is older than N sessions (config: `softStalenessSessions`) → demote to observation pool, confidence reset to 1
- Log: "SOFT rule R-0XX demoted due to staleness (last triggered: YYYY-MM-DD, threshold: N sessions)"

#### 2. Hard Cap Enforcement

Count total `[SOFT]` + `[HARD]` rules:
- If total > `maxTotalRules` (default: 30):
  - Sort `[SOFT]` rules by confidence (ascending), demote lowest until under cap
- If `[HARD]` count > `maxHardRules` (default: 15):
  - Sort `[HARD]` rules by confidence (ascending), demote to `[SOFT]` until under cap

#### 3. Observation Pool Pruning

Count observation entries:
- If observations count > `maxObservations` (default: 50):
  - Remove entries with confidence = 1 AND no re-trigger in last 30 days
  - If still over cap: remove lowest-confidence entries first

#### 4. Retired Archives Compaction

Count retired entries:
- If retired entries > `retiredArchiveThreshold` (default: 20):
  - Distill oldest 10 entries into a summary row: "Archived: 10 rules retired between YYYY-MM-DD and YYYY-MM-DD (see growth-log.md for details)"
  - Keep the full detail in `growth-log.md`

#### 5. Write Anti-Bloat Report

Append to changelog:

```
## Anti-Bloat Report

| Action | Details |
|:--|:--|
| Staleness sweep | N SOFT rules demoted to observations (stale) |
| Hard cap enforcement | N rules demoted (cap reached) |
| Observation pruning | N old observations removed |
| Retired compaction | N retired entries distilled |
```

If no actions taken: "Anti-bloat check: no action needed (rule set is within healthy limits)"

---

## Rule Write Formats

### observations.md Entry (V2.2 schema)

```markdown
| O-001 | Bug pattern description | 1 | 2026-07-05 | 1 | 2026-07-05 | active |
```

Columns: `ID | Pattern | Confidence | First Seen | Recurrence Count | Last Triggered | Status`

### self-check-full.md Auto-Grown Rules Zone

```markdown
### Rule 25 [SOFT] — Dynamic DOM Event Delegation
- **Confidence**: 3
- **Last Triggered**: 2026-07-05
- **Trigger**: JavaScript creates DOM with event bindings via innerHTML/appendChild
- **Correct Pattern**: Use event delegation bound to parent container
- **Source**: Auto-grown O-001 → R-025 (2026-07-05)
```

### growth-log.md Entry

```markdown
| 2026-07-05 14:30 | O-001 → R-025 | PROMOTE → SOFT | 2→3 (first Tier 1 threshold) | Dynamic DOM event delegation | 2026-07-05 |
```

Added column: `Last Triggered` (for staleness tracking)

### growth-log.md — Anti-Bloat Event Entry

```markdown
| 2026-07-05 14:35 | R-025 | DEMOTE → OBS | 3→1 (staleness: last triggered 2026-04-01) | — | — |
```

---

## Share Export (Opt-in)

**Pre-condition**: `pipeline.json` → `selfGrowth.shareContact.phone` must NOT be empty.
If phone is empty → skip share block entirely. This is an opt-in privacy design.

When conditions met (Tier 2 [HARD] rules generated AND phone configured), append at end of changelog:

```
💡 Important Rules Auto-Discovered by AI This Session

> Rule X: [HARD] — Rule description
> Source: Auto-grown from project practice, confidence X

These rules come from the Vibe Coding Rules V2.2 self-growing system.
📱 Share: {{pipeline.selfGrowth.shareContact.phone}}
({{pipeline.selfGrowth.shareContact.projectName}})
```
