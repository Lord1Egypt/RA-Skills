# Sql To Dashboard

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将 SQL 查询结果转换为图表规格 — 折线图、柱状图、散点图、饼图和仪表盘面板

## 解决什么问题

SQL 查询返回行和列，但趋势和异常没有可视化是不可见的。这个技能分析查询结构（GROUP BY、聚合、日期列）和数据形状，推荐并生成正确的图表类型。

**触发条件：** SQL 查询或结果集 + 图表/仪表盘/可视化意图。

## 功能特性

- **查询结构分析** — 从 SELECT 列、GROUP BY、ORDER BY 和聚合推断结果形状
- **自动图表选择** — 时序 → 折线图，Top-N + 计数 → 水平柱状图，两个数值列 → 散点图
- **多平台输出** — Plotly JSON、Grafana panel JSON 或简单数据的 Mermaid
- **处理空结果** — 明确报告"无数据返回"而不是渲染空图表 |

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install sql-to-dashboard

# 或手动复制
cp -r sql-to-dashboard ~/.openclaw/skills/
```

### 使用方法

```
/sql-to-dashboard
```

粘贴 SQL 查询或结果 CSV，要求可视化。

```
/sql-to-dashboard/multi
```

将多个相关查询组合到一个仪表盘中，有多个面板。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/sql-to-dashboard` | 单个查询 → 图表规格 |
| `/sql-to-dashboard/multi` | 多个查询 → 带多个面板的仪表盘 |

## 示例

| 查询模式 | 图表类型 |
|--------------|------------|
| `SELECT date, COUNT(*)` 按月分组 | 折线图（时序 = 趋势） |
| `SELECT status, COUNT(*)` 3 个状态 | 带图例的甜甜圈图 |
| `SELECT category, SUM(revenue)` | 比例的饼图 |
| 空结果集 | "查询返回 0 行——无图表可显示" |
| 10000 行结果 | 聚合到前 100 条，注明"显示 10,000 条中的前 100 条" |

## 目录结构

```
sql-to-dashboard/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # 图表类型决策树、Plotly/Grafana 规格
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。