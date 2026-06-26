# Memory Lifecycle — Detailed Operations Manual

## Stage 1: Light Sleep (每次心跳/会话结束)

### Purpose
Capture raw events before they vanish from context. Light = fast, low-cost, high-frequency.

### When to Run
- Every HEARTBEAT if the session produced new information since last capture
- When a session is about to end (detected or signaled)
- When compaction is imminent (context window approaching limits)
- Immediately after any critical decision is made (don't wait for session end)

### What to Capture

**Must capture (必须写入):**
1. **Decisions** — choices that constrain or direct future work
2. **Discoveries** — new knowledge about the system or environment
3. **Pending tasks** — anything that must survive session restart
4. **Context anchors** — data you'll need to resume work

**Skip these (不需要写入):**
- Pure conversation (greetings, chitchat)
- Successfully completed routine tasks (no future relevance)
- Information already committed to code/config (it's in git)
- Temporary states that won't recur

### Format

Append to `memory/YYYY-MM-DD.md` with timestamps:

```markdown
# 2026-04-07

## 14:30 — Session Notes
- **Decision:** [What] — [Why]
- **Discovery:** [What] — [Implication]
- **Pending:** [Task] — [Next step] — [Blocked by?]
- **Context:** [Key-value data for resumption]
```

---

## Stage 2: Deep Sleep (每 3 天)

### Purpose
Distill raw journals into categorized long-term memory files. Deep = selective, evaluative.

### When to Run
- Every 3 days (configure in HEARTBEAT or cron)
- On-demand when memory files feel stale

### Process

**Step 1: Gather candidates**
Read the last 3 daily journals.

**Step 2: Evaluate each item**

| Criterion | Weight | How to evaluate |
|-----------|--------|-----------------|
| Cross-session reference | High | Mentioned or needed in 2+ separate sessions? |
| Decision durability | High | Still holds? Affects work next week? |
| Lesson value | Medium | Would knowing this have saved debugging time? |
| Frequency of need | Medium | How often will this be looked up? |
| Re-derivability | Low (inverse) | Can this be found in code/docs? If yes, lower priority |

**Step 3: Route and promote qualifying items**

Use the routing map to place each item in the correct file:

| Journal item type | Target file | Format template |
|---|---|---|
| Architecture/design choice | `decisions.md` | `## [YYYY-MM-DD] Title` with Tags, Fitness, rationale |
| Bug root cause, workaround | `lessons.md` | `## [YYYY-MM-DD] Title` with Tags, Fitness, root cause |
| Tech stack, deploy info | `project-context.md` | `## [YYYY-MM-DD] Title` with Tags, Fitness, details |
| User preference, team role | `people.md` | `## [YYYY-MM-DD] Title` with Tags, Fitness, preference |
| Command, env config | `tools-config.md` | `## [YYYY-MM-DD] Title` with Tags, Fitness, command |

**Step 4: Clean journals**
- Delete promoted entries from daily journals
- Keep unpromoted entries (they may qualify later)
- Delete journals older than 14 days if all entries promoted or expired

**Step 5: Rebuild INDEX.md**
Update INDEX.md with current file stats (see INDEX format in SKILL.md).

### Promotion Examples

**From journal → lessons.md:**
```markdown
## [2026-04-03] JNPF formEngine customValidator silent failure
- Tags: jnpf, bug, validation, workaround
- Fitness: last_referenced=2026-04-03, hit_count=1, decision_value=MEDIUM
- customValidator must return boolean, never null — silent failure, no logs, no error. Cost 2h to debug.
```

**From journal → decisions.md:**
```markdown
## [2026-04-05] Report caching via Redis
- Tags: caching, performance, architecture
- Fitness: last_referenced=2026-04-05, hit_count=1, decision_value=HIGH
- Redis for report generation cache — 8s→200ms, ~50MB footprint, async pipeline
```

---

## Stage 3: REM (每周)

### Purpose
Memory hygiene — fitness-based survival evaluation, not just time-based archival.

### When to Run
- Weekly (configure via HEARTBEAT or cron)

### Process

**Step 1: Fitness evaluation**
For each entry across all categorized files, compute fitness score:
- `last_referenced`: days since last memory_search hit or manual cite
- `hit_count`: cumulative references
- `decision_value`: HIGH/MEDIUM/LOW based on current relevance
- `conflict_status`: does a newer entry contradict this?

> Full fitness protocol: `references/survival-merge.md`

**Step 2: Archive low-fitness entries**
- Move entries with 60+ days unreferenced AND low hit_count to `memory/archive/`
- Preserve the entry with date stamp and archive reason

**Step 3: Promote high-value entries**
- Entries with hit_count ≥ 5 → mark `[PROVEN]`
- PROVEN entries have higher archival threshold (120 days instead of 60)

**Step 4: Handle conflicts (supersede)**
When a new entry contradicts an old one:
- Old entry gets `[SUPERSEDED by YYYY-MM-DD]` tag
- Keep one-line summary of the old conclusion
- New entry notes the supersession

**Step 5: Consolidate and trim**
- Merge duplicates within and across files
- Enforce per-file line budgets (see SKILL.md)
- Rebuild INDEX.md

**Step 6: Clean old journals**
- Delete daily journals older than 14 days (after all entries promoted or expired)

---

## File Taxonomy Quick Reference (文件分类速查)

### decisions.md — 架构决策
- **Content:** Why we chose X over Y, API contracts, schema decisions, tech choices
- **Example:** `## [2026-04-05] API versioning strategy — URL-based /v2/ prefix, not headers`

### lessons.md — 教训与经验
- **Content:** Bug root causes, workarounds, pitfalls, gotchas
- **Example:** `## [2026-04-03] JNPF formEngine null return — silent skip, no error`

### project-context.md — 项目上下文
- **Content:** Tech stack, directory structure, deploy info, key configs, compliance requirements
- **Example:** `## [2026-04-01] QMS tech stack — JNPF v6.0 + MySQL + Vue3 + Ant Design Vue 4.2`

### people.md — 人物信息
- **Content:** User preferences, roles, communication habits, team roles
- **Example:** `## [2026-04-01] Simon preferences — direct, structured code, 飞书卡片优先`

### tools-config.md — 工具与环境
- **Content:** Command cheatsheets, env configs, proxy settings, tool quirks
- **Example:** `## [2026-04-03] qmd must use proxychains4 for model inference`

---

## Anti-Patterns to Avoid

| Anti-pattern | Why it's bad | Fix |
|-------------|--------------|-----|
| Writing everything | Files become noise, hit budgets fast | Be selective — promote only decision-value content |
| Never promoting | Journals accumulate, nothing in long-term memory | Run Deep stage every 3 days minimum |
| Wrong file routing | decisions in lessons, context in people | Use the routing map above |
| No timestamps | Can't tell current vs. stale | Always include `[YYYY-MM-DD]` |
| No fitness tracking | Can't evaluate what to archive | Track references and hit counts |
| Loading everything | Wastes context window | Follow mount strategy — INDEX first, rest on-demand |
