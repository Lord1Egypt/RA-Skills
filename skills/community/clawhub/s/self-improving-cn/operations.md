# Memory Operations 记忆操作

## User Commands 用户指令

| Command | Action |
|---------|--------|
| "你对 X 有哪些记录？" | Search all tiers, return matches with sources |
| "展示我的记忆" | Display memory.md contents |
| "展示 [project]规则" | Load and display specific namespace |
| "展示 [项目]规则" | Load and display specific namespace |
| "忘记 X" | Remove from all tiers, confirm deletion |
| "忘记一切" | Full wipe with export option |
| "最近有什么变更？" | Show last 20 corrections |
| "导出记忆" | Generate downloadable archive |
| "记忆状态" | Show tier sizes, last compaction, health |


## Automatic Operations 自动操做

### On Session Start
1. Load memory.md (HOT tier)
2. Check index.md for context hints
3. If project detected → preload relevant namespace

### On Correction Received  收到更正时
```
1. Parse correction type (preference, pattern, override)
2. Check if duplicate (exists in any tier)
3. If new:
   - Add to corrections.md with timestamp
   - Increment correction counter
4. If duplicate:
   - Bump counter, update timestamp
   - If counter >= 3: ask to confirm as rule
5. Determine namespace (global, domain, project)
6. Write to appropriate file
7. Update index.md line counts
```

### On Pattern Match 匹配模式时
When applying learned pattern:
```
1. Find pattern source (file:line)
2. Apply pattern
3. Cite source: "Using X (from memory.md:15)"
4. Log usage for decay tracking
```

### Weekly Maintenance (Cron) 每周维护（定时任务）
```
1. Scan all files for decay candidates
2. Move unused >30 days to WARM
3. Archive unused >90 days to COLD
4. Run compaction if any file >limit
5. Update index.md
6. Generate weekly digest (optional)
```

## File Formats 文件格式

### memory.md (HOT)
```markdown
# Self-Improving Memory

## Confirmed Preferences
- format: bullet points over prose (confirmed 2026-01)
- tone: direct, no hedging (confirmed 2026-01)

## Active Patterns
- "looks good" = approval to proceed (used 15x)
- single emoji = acknowledged (used 8x)
- "不错" = approval to proceed (used 12x)
- "好的" = approval to proceed (used 10x)

## Recent (last 7 days)
- prefer SQLite for MVPs (corrected 02-14)
```

### corrections.md
```markdown
# Corrections Log

## 2026-02-15
- [14:32] 把冗长解释 → 项目符号汇总
  Type: communication
  Context: Telegram response
  Confirmed: pending (1/3)

## 2026-02-14
- [09:15] MVP用SQLite不用Postgr
  Type: technical
  Context: database discussion
  Confirmed: yes (said "always")

## 2026-02-13
- [09:15] 使用vue代码代替react
  Type: technical
  Context: front code
  Confirmed: yes (said "好的")
```

### projects/{name}.md
```markdown
# Project: my-app

Inherits: global, domains/code

## Patterns
- Use Tailwind (project standard)
- No Prettier (eslint only)
- Deploy via GitLab CI

## Overrides
- semicolons: yes (overrides global no-semi)

## History
- Created: 2026-01-15
- Last active: 2026-02-15
- Corrections: 12
```

## Edge Case Handling 边界场景处理

### Contradiction Detected 检测到冲突
```
Pattern A: "Use tabs" (global, confirmed)
Pattern B: "Use spaces" (project, corrected today)

Resolution:
1. Project overrides global → use spaces for this project
2. Log conflict in corrections.md
3. Ask: "Should spaces apply only to this project or everywhere?"
```

### User Changes Mind 用户改变想法
```
Old: "Always use formal tone"
New: "Actually, casual is fine"

Action:
1. Archive old pattern with timestamp
2. Add new pattern as tentative
3. Keep archived for reference ("You previously preferred formal")
```

### Context Ambiguity 上下文不明确
```
User says: "Remember I like X"

But which namespace?
1. Check current context (project? domain?)
2. If unclear, ask: "Should this apply globally or just here?"
3. Default to most specific active context
```
