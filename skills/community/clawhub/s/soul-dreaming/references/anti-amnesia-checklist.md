# Anti-Amnesia Checklist — Quick-Scan Reference

## 🚨 Must-Write-Now Triggers (立即写入)

Write to `memory/YYYY-MM-DD.md` IMMEDIATELY when any of these occur:

- [ ] A decision is made that constrains future work
- [ ] A bug root cause is identified (even if not yet fixed)
- [ ] A workaround or non-obvious fix is applied
- [ ] Architecture or design choice is finalized
- [ ] A tool/library/framework is added, removed, or swapped
- [ ] An API contract is defined or changed
- [ ] A critical file path or config location is discovered
- [ ] A dependency version is pinned for a specific reason
- [ ] A blocking issue is identified (and its current status)
- [ ] A commitment is made to a user or another agent
- [ ] A config value is changed for a non-obvious reason
- [ ] A security-relevant finding or credential location is noted

> **Rule:** If losing this information would force you to re-derive it or re-debug it, write it down NOW. Not later. Now.

---

## 📋 Session-End Dump Checklist (会话结束前)

Before a session ends (or when compaction is detected), dump these to the daily journal:

- [ ] **Current task state** — what were you working on? What's done, what's next?
- [ ] **In-flight decisions** — any decision discussed but not yet finalized?
- [ ] **Files open / being edited** — paths, line numbers, branch names
- [ ] **Errors encountered** — even unsolved ones — with what was tried
- [ ] **Next session's first action** — the exact step to resume with
- [ ] **Any commitments** — things promised to the user or other agents
- [ ] **Context that can't be re-derived** — temporary states, runtime observations

### Dump Template

```markdown
## [TIME] — Pre-Compaction Dump
- **Task:** [What you were doing]
- **State:** [Done / In progress / Blocked]
- **Files:** [List paths, branches]
- **Next step:** [Exact first action for next session]
- **Open questions:** [Unresolved decisions or issues]
- **Commits:** [Recent commit hashes for reference]
```

---

## 🔄 Session-Start Recovery Checklist (新会话启动时)

On every session wake, before doing anything else:

- [ ] **Read `memory/INDEX.md`** — the single source of truth for what memory exists
- [ ] Read today's journal (`memory/YYYY-MM-DD.md`) — Level 1 mount
- [ ] Read yesterday's journal — Level 1 mount
- [ ] Check INDEX.md search hints — any Level 2 files needed for anticipated tasks?
- [ ] Check for any pre-compaction dumps that weren't acted on
- [ ] Resume from the last recorded "next step"

### Recovery Priority (v2 — INDEX-first)

1. **INDEX.md** → understand what memory exists, what's fresh, what's stale
2. **Today's + yesterday's journal** → most recent events and pending tasks
3. **Level 2 files** (on-demand) → load based on task domain, guided by INDEX hints
4. **Never load everything** → context window is precious

> If you skip this and start working blind, you *will* make decisions that contradict prior context. Read first.

---

## 📐 Promotion & Routing Judgment Guide (晋升与路由判断)

### ✅ Promote (yes, add to categorized memory)

- Referenced or needed in 2+ sessions
- Has ongoing architectural impact
- Documents a lesson that cost significant time to learn
- Describes a pattern that recurs
- Records a decision with rationale that explains "why" (not just "what")
- Contains knowledge not derivable from code or docs

### ❌ Don't Promote (leave in journal, let it expire)

- One-time event with no future relevance
- Temporary state (server was down, env was broken — now fixed)
- Purely conversational content
- Information already encoded in code/config/git history
- Trivially re-derivable from reading the relevant file

### ⚠️ Borderline (promote if you've looked it up more than once)

- File paths used more than once across sessions
- Config patterns that need to be replicated
- Error message patterns and their meanings
- External service quirks or rate limits

### 🗂️ Routing Quick Map (路由速查)

| Journal item mentions... | Route to |
|---|---|
| "we chose", "decided to", "architecture" | `decisions.md` |
| "bug", "root cause", "workaround", "踩坑" | `lessons.md` |
| "tech stack", "deploy", "schema", "config path" | `project-context.md` |
| "Simon prefers", "team role", "communication style" | `people.md` |
| "command", "proxy", "env variable", "tool setup" | `tools-config.md` |

---

## 📇 INDEX.md Maintenance Checklist (索引维护)

After every Deep Sleep or REM cycle:

- [ ] Rebuild INDEX.md with current file stats (line count, last updated date)
- [ ] Update "Recent Entries" column — show latest 3 entry titles per file
- [ ] Update "Search Hint" column — ensure hints match actual content
- [ ] Verify INDEX.md is under 80 lines (it's the always-loaded file)
- [ ] Update "Daily Journals" table — add new days, remove entries older than 7 days
- [ ] Update "Last rebuilt" timestamp

### INDEX Rebuild Template

```markdown
# Memory Index
> Last rebuilt: YYYY-MM-DD | Total files: N | Budget: varies per file

## Hot Files (load on session start)
<!-- Only files with entries from today/yesterday, or decision_value=HIGH -->

## On-Demand Files (load when relevant)
<!-- All other categorized files with search hints -->

## Daily Journals
<!-- Last 7 days only -->
```

---

## 🧹 Weekly REM + Fusion Checklist (每周 REM + 融合)

Run during REM stage:

- [ ] Run fitness evaluation on all entries across all files
- [ ] Archive low-fitness entries (60+ days unreferenced, low hit_count)
- [ ] Promote high-hit entries (hit_count ≥ 5) to `[PROVEN]` status
- [ ] Check for superseded/conflicting entries — apply supersede format
- [ ] Merge duplicate entries (within file and cross-file)
- [ ] Enforce per-file line budgets (see SKILL.md budget table)
- [ ] Rebuild INDEX.md with updated stats
- [ ] Clean up daily journals older than 14 days
- [ ] Update `memory/dreaming-state.json` with last REM timestamp

---

## ⚡ Quick Decision Matrix

"Should I write this down?"

| Situation | Action |
|-----------|--------|
| Just made a decision | **Write now** → journal |
| Found a bug root cause | **Write now** → journal |
| Changed a config for a reason | **Write now** → journal |
| Had an interesting thought | Skip (unless it affects future work) |
| About to lose context | **Dump now** → journal |
| New session starting | **Read INDEX + 2 journals** → L1 mount |
| Need domain knowledge | **Check INDEX hints** → L2 mount if needed |
| Need old/historical info | **Search archive** → L3 retrieval |
| 3 days since last Deep | Run Deep stage + rebuild INDEX |
| 7 days since last REM | Run REM + fitness eval + fusion |
