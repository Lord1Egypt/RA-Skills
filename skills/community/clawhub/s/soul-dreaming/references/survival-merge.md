# Survival Merge Protocol — 优胜劣汰融合完整协议

## Overview（概览）

This protocol replaces simple "60-day archive" with value-based dynamic survival. Memory entries compete for space based on actual utility, not just age.

```
New entries enter via Light Sleep (journals)
    → Survive via Deep Sleep promotion (fitness ≥ threshold)
    → Compete in REM (fitness re-evaluation)
    → Survivors stay, losers get archived
    → PROVEN entries get extra protection
```

---

## Fitness Evaluation (适应度评估)

### Metrics（指标）

Each entry tracks four fitness metrics:

| Metric | Type | How to measure |
|--------|------|----------------|
| `last_referenced` | Date | Last time `memory_search` returned this entry, or manual cite |
| `hit_count` | Integer | Cumulative number of references (search hits + manual citations) |
| `decision_value` | Enum | HIGH = affects active decisions, MEDIUM = useful context, LOW = historical |
| `conflict_status` | Enum | NONE, SUPERSEDED (contradicted by newer entry), CONFLICTS (unresolved) |

### Recording fitness

Every entry in categorized files includes a fitness line:

```markdown
## [YYYY-MM-DD] Entry Title
- Tags: tag1, tag2, tag3
- Fitness: last_referenced=YYYY-MM-DD, hit_count=N, decision_value=HIGH|MEDIUM|LOW
- Body: the actual content...
```

### Updating fitness

- **On memory_search hit:** increment `hit_count`, update `last_referenced`
- **On manual reference:** increment `hit_count`, update `last_referenced`
- **On Deep Sleep promotion:** set `decision_value` based on current relevance
- **On new contradicting entry:** set old entry's `conflict_status=SUPERSEDED`

---

## Scoring Formula (评分公式)

Composite fitness score (computed during REM):

```
score = recency_score + usage_score + value_score

recency_score = max(0, 100 - days_since_last_referenced)
usage_score   = min(50, hit_count * 5)
value_score   = { HIGH: 50, MEDIUM: 25, LOW: 0 }

Total range: 0-200
```

### Thresholds（阈值）

| Score | Action |
|-------|--------|
| ≥ 120 | **Keep** — healthy, active memory |
| 60-119 | **Watch** — declining but not yet expendable |
| < 60 | **Archive candidate** — evaluate for removal |

**Special case — PROVEN entries:** If `hit_count ≥ 5`, add 30 bonus to score. PROVEN entries can't be archived until score drops below 30 (instead of 60).

---

## Merge Rules (融合规则)

### Rule 1: Supersede（新信息覆盖旧信息）

When a new entry contradicts an old one:

```markdown
## [2026-04-07] Redis 缓存策略（v2） — 异步管道
- Tags: caching, performance, architecture
- Fitness: last_referenced=2026-04-07, hit_count=3, decision_value=HIGH
- Use Redis Streams for async report pipeline. Async pipe outperforms batch sync.
- ~~[2026-04-03] Redis 缓存策略（v1）— SUPERSEDED: batch sync was replaced by async pipeline~~
```

**Steps:**
1. Write the new entry in full
2. Append a strikethrough summary of the old entry at the bottom
3. Update old entry in its original location to just: `~~[date] title — SUPERSEDED by YYYY-MM-DD~~`
4. Delete the old entry's full content (keep only the one-line summary)

### Rule 2: Consolidate Duplicates（重复信息合并）

When two or more entries cover the same topic:

1. Compare entries — find the most complete version
2. Merge unique details from all versions into the best version
3. Update the merged entry's timestamp to the latest
4. Add `hit_count` values together
5. Delete the other versions
6. Note the merge: `(merged from [date1], [date2])`

### Rule 3: Value-Based Archival（低价值淘汰）

During REM, archive entries that:
- Score < 60 (per formula above)
- `last_referenced` > 60 days ago
- `decision_value` = LOW
- NOT marked `[PROVEN]`

**Archive format** (`memory/archive/YYYY-MM.md`):
```markdown
# Archived: 2026-04

## [2026-01-15] Old server config
- Tags: server, config
- Archived: 2026-04-07 (fitness score: 35, last_referenced: 2026-01-20)
- Content: [original body preserved]
```

### Rule 4: PROVEN Promotion（高价值晋升）

When an entry's `hit_count` reaches 5:
1. Mark entry with `[PROVEN]` prefix
2. Update fitness line to reflect bonus: `decision_value=HIGH` (if not already)
3. PROVEN entries get archival threshold raised to 120 days

```markdown
## [2026-04-03] [PROVEN] JNPF formEngine null return bug
- Tags: jnpf, bug, validation, workaround
- Fitness: last_referenced=2026-04-07, hit_count=7, decision_value=HIGH
- customValidator must return boolean, never null. Silent failure pattern.
```

### Rule 5: Conflict Resolution（冲突处理）

When two entries disagree and neither clearly supersedes:

1. Mark both with `conflict_status=CONFLICTS`
2. Do NOT archive either — unresolved conflicts must stay visible
3. Add a note: `⚠️ CONFLICTS with [YYYY-MM-DD entry] — needs resolution`
4. Flag in INDEX.md under a "Conflicts" section

---

## REM Cycle Procedure (REM 周期操作)

Run weekly. Full procedure:

### Step 1: Gather all entries
Read all categorized files: decisions.md, lessons.md, project-context.md, people.md, tools-config.md

### Step 2: Compute fitness scores
For each entry, calculate the composite score using the formula above.

### Step 3: Sort and categorize
- **Keep (≥120):** No action needed
- **Watch (60-119):** Review — any that can be consolidated?
- **Archive (<60):** Mark for archival

### Step 4: Process archives
For archive candidates:
1. Check PROVEN status — skip if PROVEN
2. Check conflict status — skip if CONFLICTS
3. Move to `memory/archive/YYYY-MM.md`
4. Remove from source file

### Step 5: Process supersessions
For entries with `conflict_status=SUPERSEDED`:
1. Verify the superseding entry exists and is newer
2. Replace full content with one-line summary
3. Remove from main file (or keep as strikethrough if useful for traceability)

### Step 6: Process consolidations
For duplicate or overlapping entries:
1. Merge into most complete version
2. Sum hit_counts
3. Delete duplicates

### Step 7: Promote PROVEN entries
1. Scan for entries with hit_count ≥ 5
2. Mark `[PROVEN]`
3. Update decision_value to HIGH if applicable

### Step 8: Enforce line budgets
Per-file budget check:
- If over budget, archive lowest-scored entries first
- Never archive PROVEN entries for budget reasons

### Step 9: Rebuild INDEX.md
Update INDEX with:
- New line counts
- Updated last-referenced dates
- Current recent entries
- Any conflicts flagged

---

## Conflict Handling Template (冲突处理模板)

```markdown
## [2026-04-07] Redis 缓存策略（v2）— 异步管道
- Tags: caching, performance, architecture
- Fitness: last_referenced=2026-04-07, hit_count=3, decision_value=HIGH
- Use Redis Streams for async report pipeline. Async pipe outperforms batch sync by 3x.
- ~~[2026-04-03] Redis 缓存策略（v1）— SUPERSEDED: 异步管道比同步批量更优~~
```

### Unresolved conflict template:

```markdown
## [2026-04-01] Database schema approach
- Tags: database, schema, architecture
- Fitness: last_referenced=2026-04-05, hit_count=2, decision_value=HIGH
- ⚠️ CONFLICTS with [2026-04-07] entry — needs resolution
- Current stance: normalize aggressively for query flexibility
```

---

## Practical Notes for QMS Agents (项目实战备注)

### For Zero / Ciici (QMS development agents):

**High-frequency decisions.md entries:**
- API versioning, authentication approach, data model changes
- IATF16949 compliance decisions (workflow approval chains, audit trails)
- Integration decisions (ERP ↔ QMS data sync strategy)

**High-frequency lessons.md entries:**
- JNPF platform quirks and workarounds
- MyBatis-Plus mapper edge cases
- Vue3 + Ant Design component gotchas
- Spring Boot + Sa-Token permission pitfalls

**project-context.md essentials:**
- JNPF v6.0 module structure
- Database schema (key tables: inspections, nc_reports, corrective_actions)
- IATF16949 workflow requirements
- Deploy environment (JNPF dev server, MySQL connection details)

### Fitness scoring tips:
- JNPF workaround entries tend to be high-value (HIGH decision_value) — they save hours
- Temporary config entries tend to be low-value (LOW) — they change frequently
- Architecture decisions start HIGH but decay if the code stabilizes
- Lesson entries should almost always be MEDIUM+ — bugs recur
