---
name: sql-optimizer
description: "This skill should be used when the user wants SQL queries written from business requirements, or has an existing SQL query that needs performance tuning. Trigger phrases include '写个 SQL', '帮我优化这条 SQL', '这个查询很慢', 'SQL 优化', 'WHERE 条件怎么写', 'SQL for this request'. It produces dialect-appropriate SQL plus concrete index and rewrite recommendations."
agent_created: true
---

# SQL 语句编写与优化

## Overview

根据业务需求与表结构写出正确 SQL，并给出可执行的性能优化方案。核心不是丢一句语句了事，而是：先确认需求与方言，写出可读且正确的 SQL，再系统性检查能不能走索引、有没有更优写法，最后明确风险。

## When to use

- 用户描述业务需求要查数据、写报表 SQL。
- 用户贴出一条 SQL 说慢、要优化。
- 用户问索引该怎么建、为什么没走索引。

## 输入要求

- 业务需求 + 涉及表的结构（字段名、类型、索引、大致数据量）。
- **数据库方言必问或明确假设**（MySQL / PostgreSQL / Oracle / SQL Server / Hive / ClickHouse），语法差异极大。
- 缺表结构时：先给出基于合理假设的 SQL，并把假设显式列出，要求用户确认字段名。

## Workflow

1. **澄清需求**：要什么结果、过滤条件、分组维度、排序、是否分页、是否需要去重。
2. **确认环境与结构**：方言、版本、表结构、索引、数据量级、是否有读写分离。
3. **编写 SQL**：优先正确性与可读性，再做优化。复杂逻辑用 CTE 分层表达，避免一坨嵌套。
4. **优化检查**（逐条过下方清单）。
5. **给出优化建议**：每条标明「改了什么 / 为什么更快 / 适用条件 / 副作用」。
6. **安全提示**：写操作（UPDATE / DELETE / DDL）给出回滚与预演方案。

## 分析类 SQL 模板

```
需求摘要：…
假设：…
涉及表与字段：…

## 推荐 SQL
（带注释的完整语句）

## 优化点
1. …（原因 / 收益 / 注意）
2. …

## 索引建议
- CREATE INDEX …（说明为什么是这个字段顺序）

## 验证方式
- EXPLAIN / EXPLAIN ANALYZE 期望看到：…
```

## 性能优化检查清单

- **避免 `SELECT *`**：只取需要的列，有机会命中覆盖索引。
- **避免索引列上套函数**：`DATE(created_at) = '2026-01-01'` 会让索引失效，改写成范围查询 `created_at >= '2026-01-01' AND created_at < '2026-01-02'`。
- **避免隐式类型转换**：字段是字符串却传数字，或反之，会导致索引失效；注意字符集/排序规则不一致的 JOIN。
- **前缀模糊不走索引**：`'%abc%'` 必然全表扫描；有搜索需求考虑全文索引、倒排或冗余规范化字段。
- **复合索引最左前缀**：条件顺序要与索引列顺序匹配，区分度高的列放前面。
- **OR 改 UNION ALL**：当 OR 两侧列不同且分别有索引时，拆分往往更快。
- **JOIN 前先过滤**：把过滤条件尽量下推到子查询/CTE 里，减少参与 JOIN 的行数。
- **深分页优化**：`LIMIT 100000, 20` 很慢，改用「上一页最大 ID + WHERE id > ? LIMIT n」的键集分页。
- **用小表驱动大表**：JOIN 时让结果集小的表作为驱动表。
- **EXISTS 替代 IN**：子查询结果集大时 EXISTS 通常更优；反之 IN 可能更好，需说明判断依据。
- **EXPLAIN 验证**：关注 type（避免 ALL）、key（是否用上索引）、rows（扫描行数）、Extra（Using filesort / Using temporary 需警惕）。

## 关键规则

- **写操作必须谨慎**：UPDATE / DELETE 先写 `SELECT` 版本让用户核对命中行数，或要求加事务与备份后再执行。
- **不给生产环境直接 DDL** 而不提示锁表风险。
- **删除/更新务必有 WHERE**，并提醒先用 LIMIT 或事务预演。
- 慢查询先问「慢在哪张表、多少数据量、有无索引」，不要凭空猜测。
- 方言差异：分页（LIMIT / ROWNUM / OFFSET-FETCH / TOP）、字符串拼接、日期函数都要按目标库写法。

## 自检清单

- [ ] SQL 与目标方言语法匹配
- [ ] 字段名与用户表结构一致，不臆造字段
- [ ] 覆盖了索引、函数包列、隐式转换、深分页等常见坑
- [ ] 优化建议有「为什么」和「副作用」
- [ ] 写操作给出了安全执行与回滚提示
