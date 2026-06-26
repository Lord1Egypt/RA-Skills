# Periodic Report Content Extraction Rules

**Load when:** `theme: regular-lumen` OR keywords `日报|周报|月报|daily|weekly|monthly|periodic report`.

## Extraction Rules

**1. Core KPIs** (有真实指标才渲染): 只有源内容提供短、明确、可核验的数量指标时，才使用 KPI 区块。可选指标包括项目完成数 (`X/Y`)、进度百分比 (`XX%`)、风险/阻塞数 (`N`)、临时需求处理 (`N`)。

不要为了周期报告版式强行补 KPI。日期、周数、版本号、章节序号不算 KPI。若没有真实业务/工作数字，省略 KPI 区块，并用 callout、timeline、table 或普通段落承载本周期概览；`report-summary.kpis` 使用空数组。

**2. Project Progress** (三段式):
- 状态 badge: `进行中` / `阻塞` / `已完成`
- 本周期进展 prose
- Timeline: 有日期用 `MM-DD`, 无日期用 `Week N` / `Day N`; 未来节点标记 `(future)` → `.timeline-item.future`
- 阻塞 callout: `.callout--warning` + 阻塞原因 + 影响天数

**3. Period Divider**: 本周期 sections 后强制插入 `<hr class="week-divider">`.

**4. Next Period Plan**: Timeline (future) + 待确认 callout (`.callout--note`).

**5. Daily Work**: 表格化 (`类型|内容|耗时|备注`), 分组例行/临时.

## Density Rule

Mixed 规则生效：仅当源内容有真实数字时使用 `:::kpi`/`:::chart`. 若用户只提供文字流水账（"本周开会、写代码"），用 callout/timeline 结构化叙事，**不虚构占位 KPI**.

## Section Order

1. 本周期概览 (callout/prose；有真实指标时才是 KPI)
2. 项目进展 (badge + timeline + callout)
3. 日常工作 (table)
4. **Period Divider**
5. 下周期计划 (future timeline + callout)
