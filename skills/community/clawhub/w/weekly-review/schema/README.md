# review-input 约定

对齐定稿模板：`# YYYY-MM-DD 周度复盘（weekly-review skill · 六章结构）`。

Agent 采集事实后填本结构；skill 只渲染结构。**图表**用 `dashboard.charts` 引用已生成的 PNG 路径（辅助图表），不以 Mermaid 为主。

## 图表

渲染默认生成两张**定稿样式 SVG**（标准库）：

1. `chart-时间分布-*.svg` — 横向条形「本周时间投入分布」
2. `chart-归因Token-*.svg` — 左右双柱「低效条目归因」+「Token 消耗趋势」

数据优先读 `charts_data`：

```json
"charts_data": {
  "time_distribution": [{ "label": "社媒 Agent 主题", "hours": 15.4 }],
  "attribution": [{ "label": "【用户】指令模糊", "count": 3 }],
  "token_trend": [{ "label": "本周", "millions": 2.74 }]
}
```

报告用 `![...](path)` 嵌入。`--no-charts` 可关闭。


| 字段 | 说明 |
|------|------|
| `period` | `start` / `end`（必填） |
| `meta` | `title` / `methodology` / `version_note` / `task_split` |
| `source.note` | 数据来源一行说明 |
| `dashboard.metrics[]` | `{name,value,note}` 看板表 |
| `dashboard.summary` | 一句话结论 |
| `dashboard.charts[]` | 辅助图 PNG 相对路径 |
| `projects[]` | `{title, dimensions{做了什么,…}}` 主题分节 |
| `other_projects[]` | `{name,hours,note}` |
| `problems[]` / `positives[]` | 问题表 + 正面范本 |
| `actions` | `done` / `observing` / `pending` |
| `open_sessions[]` | 待对齐会话 |
| `automations.narrative` | 自动化概览（条目列表或长文） |
| `corrections*` | 可选第七章事实更正 |

完整示例：`review-input.example.json`。
