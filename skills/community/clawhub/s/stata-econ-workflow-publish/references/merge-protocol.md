---
paths:
  - ".claude/MEMORY.md"
  - "dofiles/**/*.do"
  - "reports/**/*.qmd"
---

# Merge Protocol

> 源自 codex-stata-for-economists (陈铸)

## 核心规则

```
[LEARN] 标签被纠正，立刻记 → 每天/每周回顾学习日志 → 融入工作流
```

## 提交前审查

合并请求（PR）之前的最终审查，由 **全部** 可用agent执行：

1. **领域审查** (Domain Reviewer) — 经济/理论合理
2. **计量审查** (Econometric Reviewer) — 方法正确
3. **日志审查** (Log Validator) — 数字可追溯
4. **教学审查** (Pedagogy Reviewer) — 文档清晰
5. **校对** (Proofreader) — 语言准确

## 学习循环

使用 `[LEARN]` 标签标注被纠正的时刻：

**当用户说"不对"时，必须做：**
1. 承认错误（简短，不辩解）
2. 立即用 `[LEARN]` 标签记录到 MEMORY.md
3. 如果在do文件中有相应的错误写法，修正它
4. 持续修正：之后在类似场景使用正确的写法

**MEMORY.md 条目格式：**
```markdown
## [LEARN] 2025-12-01 — 标准误聚类层级
- **场景:** DiD分析，panel数据
- **错误:** 在个体层面聚类而非州层面
- **纠正:** 使用 `cluster(state_id)` 而非 `cluster(id)`
- **原因:** 处理在同一州内相关；个体层面聚类低估标准误
```

## 合并后

- 生成质量报告：`quality_reports/merges/YYYY-MM-DD_<branch>.md`
- 运行 `python scripts/quality_score.py dofiles/03_analysis/*.do` 确认≥90

## 每天的工作流

1. 检查MEMORY.md中的 [LEARN] 条目
2. 回顾 `quality_reports/plans/` 中的计划
3. 回顾 `quality_reports/session_logs/` 中的会话日志
4. 填写当天的 `quality_reports/session_logs/` 报告
