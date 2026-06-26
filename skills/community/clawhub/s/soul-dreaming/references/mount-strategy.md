# Mount Strategy — 三级加载操作手册

## Overview（概览）

Not all memory files should be loaded at once. Context window is precious — load only what's needed, when it's needed.

```
Level 1 — Always Mount   → INDEX.md + today/yesterday journals  (~200-300 lines)
Level 2 — On-Demand      → categorized files based on task domain (~100-300 lines each)
Level 3 — On-Demand Search → archive/ files via semantic search    (targeted results only)
```

---

## Level 1: Always Mount（常驻加载）

### What loads
1. `memory/INDEX.md` — the **only** file that must be fully loaded on every wake
2. `memory/YYYY-MM-DD.md` (today)
3. `memory/YYYY-MM-DD.md` (yesterday)

### Why
- INDEX.md gives you a map of all available memory without loading everything
- Today/yesterday journals contain the most recent decisions and pending tasks
- Together they provide full session continuity with minimal context cost

### Startup sequence
```
1. Read memory/INDEX.md
2. Read memory/<today>.md (create if doesn't exist)
3. Read memory/<yesterday>.md
4. Check INDEX.md for any critical alerts or notes
5. Resume from last recorded "next step"
```

### Total estimated context cost
- INDEX.md: ~80 lines
- Today's journal: ~50-100 lines
- Yesterday's journal: ~50-100 lines
- **Total: ~180-280 lines** — well within any context budget

---

## Level 2: On-Demand Mount（按需加载）

### Trigger conditions

Load a specific categorized file when the current task touches its domain. Use INDEX.md's "Search Hint" column as your guide.

| Task domain | Files to load | Trigger example |
|---|---|---|
| Writing code / architecture | `decisions.md` + `project-context.md` | "Implement the report caching feature" |
| Debugging / fixing bugs | `lessons.md` | "The form validation is failing again" |
| User-facing work / messaging | `people.md` | "Send a status update to Simon" |
| Environment setup / tools | `tools-config.md` | "Set up qmd for a new collection" |
| Planning a sprint / roadmap | `decisions.md` + `project-context.md` | "What's the current QMS architecture?" |

### Load-and-release pattern（加载即释放）

**Critical:** Level 2 files are loaded for the current turn only. Do NOT carry them into subsequent turns unless the task continues in the same domain.

```
Turn N:   User asks about QMS tech stack
          → Load project-context.md
          → Answer based on it
          → File stays in current context only

Turn N+1: User asks about a different topic
          → project-context.md is NOT in context anymore
          → If needed again, load again (it's cheap)
```

### Why not keep them loaded?
- Each Level 2 file is 100-300 lines
- Loading 3-4 files = 300-1200 lines of context
- That's 10-30% of a typical context window — too expensive for always-on
- Loading is cheap (<1 second), so re-load is fine

---

## Level 3: On-Demand Search（按需检索）

### When to use
- Looking for historical information in `memory/archive/`
- Searching across multiple daily journals for a specific event
- Need to find something without loading entire files

### How to use
Use `qmd search` or `qmd vsearch` (semantic search):

```bash
# Keyword search (fast, no model needed)
qmd search "Redis cache" -c memory

# Semantic search (more accurate, needs model)
proxychains4 -q qmd vsearch "why did we choose Redis over Memcached" -c memory

# Search within archive only
qmd search "JNPF validation bug" -c archive
```

### What NOT to do
- Don't load entire archive files unless you have a specific reason
- Don't search daily journals one by one — use search tools
- Don't load all categorized files "just in case" — use Level 2 triggers

---

## Cross-Level Decision Flow (决策流程图)

```
Task received
    │
    ├─ Is it a new session? ──→ Yes ──→ L1: Load INDEX + 2 journals
    │                         └─ No  ──→ Continue with current context
    │
    ├─ Does the task touch a specific domain? ──→ Yes ──→ L2: Load relevant file(s)
    │                                            └─ No  ──→ Work with L1 only
    │
    ├─ Do you need historical/old information? ──→ Yes ──→ L3: Search archive
    │                                            └─ No  ──→ Continue
    │
    └─ Is the task done? ──→ Yes ──→ Release L2 files (don't carry forward)
```

---

## Examples（实战示例）

### Example 1: QMS Development Session
```
User: "Fix the inspection report generation timeout"

Agent flow:
1. L1 already loaded (INDEX + journals)
2. Task = debugging + QMS → L2: load lessons.md + project-context.md
3. Search lessons.md for "report", "timeout", "generation"
4. Find: "Report generation timeout — root cause: synchronous DB query in loop"
5. Fix the issue
6. Write findings to today's journal
7. Session ends → lessons.md not carried to next session
```

### Example 2: New Sprint Planning
```
User: "Plan the next sprint for QMS"

Agent flow:
1. L1 already loaded
2. Task = planning → L2: load decisions.md + project-context.md
3. Check decisions.md for active decisions under evaluation
4. Check project-context.md for current tech stack constraints
5. Produce sprint plan
6. Write decisions to today's journal
```

### Example 3: Historical Context Lookup
```
User: "What was the conclusion about Redis vs RabbitMQ from last month?"

Agent flow:
1. L1 already loaded
2. Check INDEX.md → search hint says "message queue" → decisions.md
3. Search decisions.md for "Redis", "RabbitMQ", "message queue"
4. If not found in decisions.md → L3: qmd search "Redis vs RabbitMQ" -c memory
5. If still not found → L3: qmd search "Redis vs RabbitMQ" -c archive
```

---

## Anti-Patterns（反模式）

| Anti-pattern | Problem | Fix |
|---|---|---|
| Loading all files on wake | Wastes 1000+ lines of context | L1 only (INDEX + 2 journals) |
| Carrying L2 files across turns | Context bloat | Load-and-release pattern |
| Searching archive by reading all files | Impossible at scale | Use semantic search (L3) |
| Ignoring INDEX search hints | Load wrong file or miss the right one | Always check INDEX first |
| Loading project-context for a people task | Irrelevant context | Follow the trigger table |
