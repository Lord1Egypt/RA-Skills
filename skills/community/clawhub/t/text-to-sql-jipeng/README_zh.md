# Text To Sql

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 将自然语言描述转换为语法正确的 SQL 查询

## 解决什么问题

非技术用户知道想要什么数据（"显示前 10 客户每月收入"）但不会写 SQL。这个技能弥合这个差距——接收 schema + 自然语言请求，生成带表别名、正确 JOIN 和 GROUP BY 的语法正确的查询。

**触发条件：** 数据库 schema + 自然语言问题 + 写 SQL 意图。

## 功能特性

- **Schema 感知翻译** — 写查询前先询问表/列 schema（绝不虚构列名）
- **完整 SQL 覆盖** — SELECT、WHERE、GROUP BY、ORDER BY、LIMIT、JOIN（INNER、LEFT、RIGHT）、聚合函数
- **通俗英文解释** — 同时输出查询和一行描述其作用
- **多方法选项** — `/alternatives` 模式展示不同 JOIN 策略或子查询 vs CTE 方法

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install text-to-sql

# 或手动复制
cp -r text-to-sql ~/.openclaw/skills/
```

### 使用方法

```
/text-to-sql
```

提供 schema（表名 + 列）并用英文描述想要什么数据。

```
/text-to-sql/explain
```

输出带内联注释的查询，解释每个子句——用于学习。

```
/text-to-sql/alternatives
```

展示同一问题的 2-3 种不同查询方法。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/text-to-sql` | 将自然语言转换为 SQL 查询 |
| `/text-to-sql/explain` | 带内联注释的查询，解释每个子句 |
| `/text-to-sql/alternatives` | 2-3 种替代查询策略 |

## 示例

| 请求 | 查询 |
|---------|-------|
| Schema: `users(id, name)`，`orders(user_id, total)` | `SELECT u.name, SUM(o.total) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name` |
| "前 10 客户" | 添加 `ORDER BY total DESC LIMIT 10` |
| "按月收入" | `SELECT DATE_TRUNC('month', date), SUM(revenue) FROM orders GROUP BY 1` |
| 未提供 schema | 先询问 schema——不猜测列名 |

## 目录结构

```
text-to-sql/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # SQL 方言速查表、JOIN 指南、意图映射
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。