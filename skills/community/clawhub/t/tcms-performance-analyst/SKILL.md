---
slug: tcms-performance-analyst
displayName: Tcms Performance Analyst
name: tcms-performance-analyst
version: "1.1.10"
not_for:
  - Real-time or per-article analytics (monthly aggregation focus)
  - Modifying the content calendar or triggering writing (advisory output only)
  - Channel-side operations like scheduling or boosting
  - A/B testing design or execution
description: |
  Monthly content performance and output-analysis skill. Aggregates published content, the content calendar, channel-effect data, product-line coverage, and knowledge-base health; outputs a monthly report and next-cycle optimization suggestions. Does not auto-modify the schedule or trigger writing.
description_zh: "月度内容绩效分析器：聚合已发内容、内容日历、渠道效果、产品线覆盖与知识库健康度，输出月报与下周期优化建议，不自动改排期或触发写作。"

read_when:
  - 月度报告
  - 效果分析
  - 内容复盘
  - 月度复盘
  - 数据复盘
  - 发文统计
  - monthly report
  - content review
  - performance analysis
metadata:
  openclaw:
    tags:
      - content-marketing
      - analytics
      - performance-analysis
      - monthly-report
      - data-review
      - tech-product
      - b2b
disable: false
---

# Content Performance Analyst

Runs a monthly analysis of project-level content output and produces a structured report with optimization suggestions.

## When to use

- Need to tally last calendar month's content output, product-line coverage, and type distribution.
- Need to compare the planned schedule against actual output.
- Need observations based on available effect data.
- Need topic and knowledge-base adjustment suggestions for next month.

## Do not use

- Single-article pre-review — handled by `content-compliance-reviewer`.
- Auto-modifying the content calendar, published content, or product priority.
- Fabricating numbers when effect data is missing.

## Input

```yaml
calendar_path:
published_dir:
channel_data: path or null
product_line_map:
performance_profile:
  - product_priority:
  - content_type_weights:
  - channel_distribution_targets:
analysis_month: YYYY-MM
```

When effect data is missing, analyze only observable dimensions.

## Workflow

### Step 1: [Deterministic] Confirm scope

Analyze the previous calendar month by default. Confirm the calendar, published directory, and effect data.

### Step 2: [Deterministic] Collect data

1. Scan the published-content directory; extract title, date, product, type, channel.
2. Read the schedule; compare plan vs actual output.
3. If channel-effect data exists, extract reads, saves, forwards, and read-completion metrics.
4. Check the knowledge base for recent updates and backlog.

### Step 3: [LLM] Analyze

- Output completion: plan vs actual.
- Product-line coverage: article count and type per product.
- Product-priority alignment.
- Content-type distribution.
- Effect-data boundaries (mark `DATA_MISSING` when missing).
- Knowledge-base health.

### Step 4: [LLM] Produce monthly report

```markdown
# Content Monthly Report: YYYY-MM

## Output overview

| Date | Title | Product | Type | Channel | Status |
|---|---|---|---|---|---|

## Plan vs actual

- Planned / Produced / Deferred / Missing.

## Product-line coverage

| Product | Count | Type mix | Priority alignment |
|---|---:|---|---|

## Performance data (if available)

| Article | Reads | Saves | Forwards | Read-completion |
|---|---|---|---|---|

Mark missing data as DATA_MISSING.

## Key findings

- Positive.
- Gaps.
- Action items.

## Recommendations for next month

- Topic suggestions.
- Product and format adjustments.
- Knowledge-base maintenance.

## Knowledge-base health

- Recently updated:
- Thin sections:
- Stale entries:
```

### Step 5: [Deterministic] Save

Save to: `reports/YYYY-MM-monthly-report.md`

## Hard Rules

1. Never fabricate performance data. Missing data is marked `DATA_MISSING`.
2. Never modify the content calendar or trigger downstream writing.
3. Product-line analysis uses the private product map, not inference from titles.
4. Vendor- or platform-reported metrics must carry a "reported by {party}, not independently verified" caveat; a bare number is a fail.
5. Dataset gaps must be reported with the observed scope and data boundary.
6. Human confirmation required before the plan team acts on recommendations.
7. Every finding must reference a date, file or data point.

## Failure Handling

| Scenario | Action |
|---|---|
| Calendar missing | Stop; report the missing file |
| Published directory empty | Output zero-production report |
| Channel data missing | Analyze only output dimensions |
| Knowledge-base not found | Skip the health section |
| Product map missing | Stop product-line coverage analysis and mark PRODUCT_MAP_MISSING — title-based inference is forbidden by Hard Rule 3; still report output/type counts that need no product mapping |

## Output Format

```text
reports/YYYY-MM-monthly-report.md
```

## Verification

- [ ] Output count matches actual directory scan.
- [ ] Plan-vs-actual uses the calendar as reference.
- [ ] Every performance figure has an observable source or is marked DATA_MISSING.
- [ ] Recommendations reference concrete gaps.
- [ ] Report does not trigger downstream tasks.
- [ ] Missing product-line data is listed as a data gap naming the affected report section, and no section silently substitutes an inferred label.

---

## 中文摘要

Content Performance Analyst 做项目级内容的月度分析，输出结构化报告与下月优化建议。统计产出完成度、产品线覆盖、类型分布与效果数据（缺失标 DATA_MISSING），对比排期与实际，检查知识库健康度。硬性规则：不编造数据、不改排期、产品线分析用私有映射而非标题推断、每条发现须有日期/文件/数据点支撑。
