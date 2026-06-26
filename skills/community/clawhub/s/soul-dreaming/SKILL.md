---
name: soul-dreaming
description: >
  Progressive memory management with categorized files, indexed retrieval,
  and survival-merge evolution. Prevents AI amnesia after context compaction.
  Activate when: user mentions "失忆", "记忆管理", "memory", "防遗忘", "compaction",
  "记忆丢失", "记忆持久化", "soul-dreaming", "dreaming", or when you detect
  context loss, repeated questions about already-discussed topics, or need to
  persist critical decisions before session ends.
---

# Dreaming — Progressive Memory Management for AI Agents

Prevent amnesia from context compaction. Persist what matters, forget what doesn't.

## Memory Architecture (v2 — Categorized Split)

```
workspace/
└── memory/
    ├── INDEX.md            # 索引 — 唯一必须全量加载的文件
    ├── decisions.md        # 架构决策 + 理由（为什么选 X 不选 Y）
    ├── lessons.md          # 教训与经验（bug 根因、workaround、踩坑记录）
    ├── project-context.md  # 项目上下文（技术栈、目录结构、部署信息）
    ├── people.md           # 人物信息（偏好、角色、沟通习惯）
    ├── tools-config.md     # 工具与环境（命令备忘、环境配置、代理设置）
    ├── YYYY-MM-DD.md       # 每日日记（自动创建）
    └── archive/            # 归档（低价值淘汰 + 超期条目）
```

### Line Budget per File（每文件行数预算）

| File | Budget | Rationale |
|------|--------|-----------|
| INDEX.md | 80 | Index only — fast to scan |
| decisions.md | 200 | Architecture decisions with rationale |
| lessons.md | 300 | Bug patterns, workarounds — high volume |
| project-context.md | 150 | Stack, schema, config, deploy info |
| people.md | 100 | User preferences, roles |
| tools-config.md | 100 | Commands, env, proxy notes |
| Each daily journal | 100 | Raw events, temporary |

### Record Format（标准记录格式）

Every entry in categorized files uses this format:

```markdown
## [YYYY-MM-DD] Title
- Tags: tag1, tag2, tag3
- Fitness: last_referenced=YYYY-MM-DD, hit_count=N, decision_value=HIGH|MEDIUM|LOW
- Body: one-line summary of the record
```

---

## Three Stages (Core — 三阶段提炼)

### Stage 1: Light Sleep — Every Session End

Scan the current session. Write to today's journal (`memory/YYYY-MM-DD.md`):

1. **Decisions made** — anything that affects future work
2. **Key discoveries** — bugs found, root causes, unexpected behaviors
3. **Pending tasks** — unfinished items that must survive session restart
4. **Context anchors** — file paths, API endpoints, config values

**Iron rule (铁律):** Write decisions the moment they're made, not at session end. Context can vanish at any time.

### Stage 2: Deep Sleep — Every 3 Days

Promote from daily journals to categorized memory files:

1. Scan last 3 days of journals
2. Evaluate each item against promotion criteria
3. Route to the correct file (decisions → decisions.md, bugs → lessons.md, etc.)
4. Delete absorbed journal entries

**Promotion criteria:**
- Referenced across 2+ sessions/days
- Has ongoing decision value
- Contains a hard-won lesson
- Addresses a recurring pattern

**Routing map:**
| Journal item type | Target file |
|---|---|
| Architecture/design choice | `decisions.md` |
| Bug root cause, workaround | `lessons.md` |
| Tech stack, deploy info | `project-context.md` |
| User preference, team role | `people.md` |
| Command, env config | `tools-config.md` |

### Stage 3: REM — Weekly

Memory hygiene via **Survival Merge Protocol** (优胜劣汰):

1. **Evaluate fitness** of all entries across all files
2. **Archive low-value** entries → `memory/archive/`
3. **Promote high-value** — entries hit 5+ times → mark `[PROVEN]`
4. **Handle conflicts** — supersede old with new, keep one-line summary
5. **Rebuild INDEX.md** — update all stats

> Detailed protocol: `references/survival-merge.md`

---

## Mount Strategy（挂载策略 — 三级加载）

### Level 1 — Always Mount（常驻加载）
- `memory/INDEX.md` — the **only** file you must load fully on every wake
- Today's `memory/YYYY-MM-DD.md`
- Yesterday's `memory/YYYY-MM-DD.md`

### Level 2 — On-Demand Mount（按需加载）
Based on INDEX.md search hints, load when the task touches a domain:
- Starting to write code → `decisions.md` + `project-context.md`
- Debugging a bug → `lessons.md`
- User-facing task → `people.md`
- Env/setup work → `tools-config.md`

**Load-and-release:** read the file, use it, do NOT carry it into subsequent turns.

### Level 3 — On-Demand Search（按需检索）
- Use `memory_search` (qmd or equivalent) for `archive/` files
- For cross-day event lookup without loading full journals
- Never load archive files entirely unless specifically needed

> Detailed protocol: `references/mount-strategy.md`

---

## INDEX.md — Memory Index（索引文件）

INDEX.md is the **single source of truth** for what memory exists. Rebuild it after every Deep Sleep or REM cycle.

```markdown
# Memory Index
> Last rebuilt: YYYY-MM-DD | Total files: N | Budget: 500 lines per category

## Hot Files (load on session start)
| File | Lines | Last Updated | Recent Entries |
|------|-------|-------------|----------------|
| decisions.md | 45 | 2026-04-06 | Redis缓存策略, API版本v2 |
| project-context.md | 80 | 2026-04-07 | QMS技术栈, 数据库schema |

## On-Demand Files (load when relevant)
| File | Lines | Last Updated | Search Hint |
|------|-------|-------------|-------------|
| lessons.md | 120 | 2026-04-05 | bug根因, workaround, 踩坑 |
| people.md | 30 | 2026-03-28 | 人物偏好, 角色 |
| tools-config.md | 25 | 2026-04-03 | 命令备忘, 环境配置 |

## Daily Journals
| Date | Exists | Key Events |
|------|--------|------------|
| 2026-04-07 | ✅ | cron修复, Dreaming skill创建 |
| 2026-04-06 | ✅ | PraisonAI研究, GitHub同步 |
```

---

## Session Lifecycle Integration

### On Wake (新会话启动)
```
1. Read memory/INDEX.md
2. Read today + yesterday journals
3. Resume work
```

### Before Context Loss (上下文即将丢失)
→ Dump to today's journal immediately: task state, in-flight decisions, open files, errors, next step.

### Quick Reference

| When | Action | Write to |
|------|--------|----------|
| Decision made | Write immediately | `memory/YYYY-MM-DD.md` |
| Session ending | Dump current state | `memory/YYYY-MM-DD.md` |
| New session | Read INDEX + 2 journals | L1 mount |
| Every 3 days | Promote + route + rebuild INDEX | Deep Sleep |
| Weekly | Fitness eval + archive + supersede | REM |
| Task touches domain | Load relevant file | L2 mount |

---

## References

- `references/memory-lifecycle.md` — 三阶段操作手册 + 文件分类规范
- `references/anti-amnesia-checklist.md` — 防失忆检查清单 + INDEX 维护
- `references/mount-strategy.md` — 挂载策略详细操作手册
- `references/survival-merge.md` — 优胜劣汰融合完整协议
