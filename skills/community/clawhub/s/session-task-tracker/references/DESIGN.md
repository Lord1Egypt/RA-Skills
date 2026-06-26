# Task Tracker Reference

## Decision Log

### 2026-03-31: Initial Design
- Decided on task-file-per-task model vs SESSION-STATE.md global snapshot
- Reason: task files survive compaction, are readable by any session, no timeline confusion
- SESSION-STATE.md retained as lightweight index only

## Design Rationale

### Why not just AGENTS.md rules?
- Rules in AGENTS.md have low enforcement — agent forgets to follow them
- Skill triggers on system scan, forcing the agent to read and follow the workflow
- Skill is reusable across OpenClaw instances

### Why not daily logs (memory/YYYY-MM-DD.md)?
- Sessions span multiple days — can't determine which day content belongs to
- Task dimension is more natural than time dimension for context recovery
- Daily logs still useful for audit trail, but not for context continuity

### Relationship with other skills
- `agent-memory`: handles vector/keyword memory search — complementary
- `proactive-agent`: handles proactive behavior patterns — complementary
- `self-improvement`: handles learning from errors — complementary
- `task-tracker`: handles structured task persistence — fills a unique gap

## Advanced Patterns

### Cross-session handoff phrase
When user says: "继续[任务名]", "上次[任务名]怎么样了", "我之前让你做的[任务]"
→ Read the corresponding task file, summarize current state, ask what to continue

### Implicit task detection
When user discusses something new that sounds like a project/task:
→ Ask: "这个要作为新任务记录吗？"
→ If yes, create task file

### Task status transitions
```
待启动 → 进行中 → 已完成 → archive/
                → 暂停 → 进行中 (resume)
                → 已搁置 → archive/ (after 30 days)
```
