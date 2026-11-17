# 自我学习事件日志（模块 ④-2）

> 由 `maintainers/scripts/self_evolution.py append` 追加；由 `fold` 定期折叠回主题积木标注。
> 人工可直接阅读与补记（按相同格式手动加 `- date:` 事件即可，引擎会一并聚合）。
> 事件类型：adopt（采纳推荐）/ reject（拒收推荐）/ feedback（用户反馈）/ discover（新发现 skill）。
> 折叠标记：以 `kind: fold` 记录每次折叠的 `learnings_at_fold`，供"自上次折叠增量"计算。

## 事件格式（示意，非真实事件）

```
- date: 2026-08-24T10:15
  kind: adopt
  slug: "@org-gv4zgi7j/stock-volume-12step-analysis"
  theme: investment-analysis
  composite: 5,5
  note: "教授确认采纳，日常用于量能专项"
```

字段说明：
- `date`：ISO 时间戳 `YYYY-MM-DDTHH:MM`（引擎自动填）。
- `kind`：`adopt` / `reject` / `feedback` / `discover`。
- `slug`：技能命名空间 slug（与主题积木 `slug` 字段一致，用于跨文件聚合）。
- `theme`：所属主题（investment-analysis / knowledge-management …），可选。
- `composite`：③-4 二维分 `usability,composable`，可选（用于 `auto_weight`）。
- `note`：原因 / 反馈摘要。

## 事件

<!-- 以下由引擎 append 追加；手动补记请保持上面格式 -->
