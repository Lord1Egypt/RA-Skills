---
name: smart-daily-report
description: "Intelligent work report generator that collects activity from project history, task managers, and calendars to produce professional daily/weekly reports. Features smart commit parsing, multi-project aggregation, trend analysis, and customizable templates. Use when user needs to write daily report, weekly report, work summary, standup notes, sprint review, or any status update."
---

# Smart Daily Report | 智能日报生成器

> From scattered work traces to polished reports — automatically.

## When to Activate

- "生成今天的日报" / "帮我写日报"
- "This week's status report"
- "Standup notes for today"
- "我做了什么" / "What did I work on"
- "周报" / "Weekly summary"
- Any request to summarize work activity

---

## Step 1 — Collect Data

### Data Source Priority

Gather data from available sources in this order:

| Priority | Source | What to collect | Fallback |
|----------|--------|----------------|----------|
| 1 | Project history | Commit messages, change stats | Skip if no project found |
| 2 | Task manager | Completed/pending tasks | Skip if unavailable |
| 3 | Calendar | Meetings, events | Ask user to supplement |
| 4 | User input | Manual description | Always available |

### Collection Commands

Use system tools to gather project activity. Adapt to the user's OS:

**Project commit history:**
- Use appropriate system tool to read commit log for the specified date range
- Collect: commit message, timestamp, project name
- Include all branches the user contributed to

**Change statistics:**
- Collect number of files changed, lines added/removed
- Group by project if multiple repos

**Task completion:**
- If todoist CLI is available, query completed tasks for the date
- Otherwise, skip this source

### Multi-Project Handling

If the user has multiple projects:
1. Scan for project directories in common locations (workspace, home, desktop)
2. Collect activity from each
3. Group results by project in the output

---

## Step 2 — Parse & Enrich

### Commit Message Parsing

**Standard format (Conventional Commits):**

| Pattern | Category | Display |
|---------|----------|---------|
| `feat(scope): message` | New Feature | message (scope) |
| `fix(scope): message` | Bug Fix | Fix: message (scope) |
| `docs: message` | Documentation | 📝 message |
| `refactor: message` | Refactor | ♻️ message |
| `test: message` | Testing | 🧪 message |
| `perf: message` | Performance | ⚡ message |
| `chore: message` | Maintenance | 🔧 message |
| `ci: message` | CI/CD | 🔄 message |
| `Merge pull/branch` | Merge | 🔀 Merge #number |

**Non-standard format:**
- Try to extract a verb + object pattern
- Classify based on keywords: "修复/fix" → Bug Fix, "添加/新增/add" → Feature, "更新/update" → Update, "删除/remove" → Cleanup

### Smart Grouping Rules

1. **Collapse related commits** — 3 commits like "add login page", "fix login css", "test login" → "登录页面开发与测试"
2. **Extract project scope** — Infer from directory name or commit prefix
3. **Deduplicate** — Merge + original commit → show once
4. **Prioritize** — Features and fixes first, chores and docs last

### Significance Assessment

| Level | Criteria | Report Placement |
|-------|----------|-----------------|
| Major | New feature, significant refactor, critical fix | "今日重点" section |
| Normal | Regular commits, bug fixes, docs | "完成事项" section |
| Minor | Chore, style, typo fixes | Omit or collapse into stats |

---

## Step 3 — Generate Report

### Daily Report Template

```markdown
# 工作日报 | {YYYY-MM-DD 周X}

## 今日重点
> {1-2 sentence executive summary of the day's core work}

## 完成事项

### {Project A}
- ✅ {Feature or fix description}
- ✅ {Another item}

### {Project B}
- ✅ {Item description}

## 进行中
- 🔄 {Ongoing work that wasn't completed today}

## 明日计划
- 📋 {Next steps based on in-progress work or user hints}

## 数据统计
| 指标 | 数值 |
|------|------|
| 项目数 | {n} |
| 提交数 | {n} |
| 文件变更 | {n} 个文件 |
| 代码量 | +{n} / -{n} 行 |

## 备注
- {Anything notable: blockers, dependencies, achievements}
```

### Weekly Report Template

```markdown
# 周报 | {Monday日期} ~ {Friday日期}

## 本周概览
> {2-3 sentence summary of the week's themes and achievements}

## 核心成果

### {Project A}
- {Major deliverable 1}
- {Major deliverable 2}

### {Project B}
- {Major deliverable}

## 详细进展

| 日期 | 主要工作 |
|------|----------|
| 周一 | {Key items} |
| 周二 | {Key items} |
| ... | ... |

## 数据汇总
| 指标 | 数值 |
|------|------|
| 项目数 | {n} |
| 总提交 | {n} |
| 新增代码 | +{n} 行 |
| 删除代码 | -{n} 行 |
| PR/MR | {n} 个 |
| Bug修复 | {n} 个 |

## 下周计划
1. {Priority 1}
2. {Priority 2}
3. {Priority 3}

## 需要协助
- {Blockers, resource needs, decisions pending}
```

### Standup Notes Template

```markdown
## Standup | {Date}

**Yesterday:**
- {What was completed}

**Today:**
- {What's planned}

**Blockers:**
- {Any impediments} / None
```

---

## Step 4 — Handle Edge Cases

| Situation | Response |
|-----------|----------|
| No commits found | Ask: "今天没有检测到项目提交记录。你今天做了哪些工作？我来帮你整理。" |
| Only chores/minor commits | Generate report with stats, note that work was mainly maintenance |
| User provides manual input | Combine manual descriptions with any available stats |
| Multiple contributors detected | Filter to only the user's commits (by author name/email) |
| Very active day (20+ commits) | Group aggressively, focus on features/fixes, collapse minor commits into stats |
| Across time zones | Use the user's local date (from USER.md timezone setting) |

---

## Advanced Features

### Custom Templates

If user says "用我的模板" or provides a template:
1. Accept their template structure
2. Map data fields to template placeholders
3. Generate report in their exact format

### Trend Analysis (for weekly reports)

Compare this week vs last week:
- Commit count: ↑/↓/→ with percentage
- Focus areas: shifted to different projects?
- Velocity: faster/slower?

### Export Options

| Target | Method |
|--------|--------|
| Chat (default) | Markdown inline |
| Feishu doc | `feishu_doc` → `create` then `write` |
| File | Save to path like `reports/YYYY-MM-DD.md` |
| Clipboard | Tell user the content is ready to copy |

### Auto-Generation Hint

If the user has a regular schedule (e.g., always asks for daily report at 6pm), suggest setting up a cron job or HEARTBEAT.md reminder.
