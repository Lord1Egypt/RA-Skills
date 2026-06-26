---
name: sql-generator
description: |
  SQL生成器 - 自然语言转高质量SQL代码，支持多数据库方言。
  当用户需要生成SQL查询、转换业务需求为SQL、编写复杂JOIN或窗口函数时触发。
  触发词：生成SQL、写个查询、帮我写SQL、自然语言转SQL。
argument: { description: "业务需求描述（包含数据库类型、查询目标、条件、分组、排序等）", required: true }
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Edit, Write, Bash]
---

# SQL生成器

将自然语言业务需求转换为高质量、高性能的SQL代码。

## 工作流

1. **需求解析** - 提取数据库类型、查询目标、过滤条件、分组维度、排序要求
2. **Schema分析** - 如提供表结构，理解表关系和字段含义
3. **SQL构建** - 生成符合规范的SQL代码
4. **优化建议** - 提供索引建议和性能预期

## 输出规范

所有生成的SQL必须包含：
- 标准版本头注释
- CTE结构（复杂查询）
- 执行建议（索引、预期性能）
- 符合 sql-standards.md 规范

### 版本头模板

```sql
-- ============================================
-- 查询目的：[一句话描述]
-- 目标数据库：[数据库类型及版本]
-- 作者：AI Assistant
-- 生成时间：YYYY-MM-DD
-- ============================================
```

### 代码结构模板

```sql
-- 版本头

WITH
-- CTE分层（如需要）
cte_1 AS (...),
cte_2 AS (...)

-- 主查询
SELECT
    column1,
    column2,
    aggregate_function(column3) AS alias
FROM table_name
[JOIN ...]
[WHERE ...]
[GROUP BY ...]
[HAVING ...]
[ORDER BY ...]
[LIMIT ...];

-- 执行建议
-- 1. 建议索引：...
-- 2. 预计扫描行数：...
-- 3. 预期执行时间：...
```

## 数据库方言适配

### MySQL 特有
- 日期：`CURDATE()`, `DATE_SUB()`, `DATE_FORMAT()`
- 分页：`LIMIT offset, count`
- 类型转换：`CAST(x AS type)`

### PostgreSQL 特有
- 日期：`CURRENT_DATE`, `NOW()`, `DATE_TRUNC()`
- 类型转换：`::type` 或 `CAST(x AS type)`
- JSON：`json_col->>'field'`

### SQL Server 特有
- 日期：`GETDATE()`, `DATEADD()`, `DATEDIFF()`
- 分页：`OFFSET ... FETCH NEXT ...`
- TOP：`SELECT TOP n ...`

### Oracle 特有
- 日期：`SYSDATE`, `TRUNC()`
- 分页：`ROWNUM` 或 `OFFSET FETCH`
- 空值：`NVL()` 替代 `COALESCE()`

## 生成原则

### 1. 可读性优先
- 使用CTE而非嵌套子查询
- 清晰的缩进和换行
- 表别名使用有意义缩写（o=orders, u=users）
- 复杂逻辑添加注释

### 2. 性能优化
- 避免 `SELECT *`
- WHERE条件使用索引友好写法
- 日期范围使用闭开区间 `[start, end)`
- JOIN顺序优化

### 3. 健壮性
- NULL值处理（`COALESCE()` / `IFNULL()`）
- 除零保护（`NULLIF()`）
- 字符串安全处理

### 4. 命名规范
- 表名：小写下划线（`user_orders`）
- 字段别名：小写下划线（`total_amount`）
- CTE名称：描述性名词（`monthly_sales`）

## 复杂查询策略

### 多阶段生成（适用于复杂需求）

如果需求复杂，主动建议分阶段：

```
用户：统计各品类用户的复购率和客单价趋势，计算同比环比

AI：这个查询较复杂，建议分阶段生成：
1. 先生成CTE结构设计
2. 然后生成第一层CTE（用户购买行为）
3. 再生成第二层CTE（复购计算）
4. 最后合并为完整查询

是否继续分阶段生成？
```

### CTE层级设计

```sql
WITH
-- 第1层：基础数据清洗
base_data AS (
    SELECT ... FROM ... WHERE ...
),

-- 第2层：中间计算
intermediate_calc AS (
    SELECT ... FROM base_data ...
),

-- 第3层：最终聚合
final_aggregate AS (
    SELECT ... FROM intermediate_calc ...
)

SELECT * FROM final_aggregate;
```

## 输入解析

从用户输入中提取：

| 要素 | 示例 |
|------|------|
| 数据库类型 | MySQL 8.0、PostgreSQL 15、SQL Server 2022 |
| 查询目标 | 销售额统计、用户增长、留存率 |
| 时间范围 | 过去30天、2024年Q1、最近一年 |
| 过滤条件 | 已完成订单、活跃用户、特定区域 |
| 分组维度 | 按品类、按区域、按日期 |
| 排序要求 | 按销售额降序、按日期升序 |
| 特殊要求 | 同比增长、累计计算、排名 |

## 当前需求

$ARGUMENTS

---

**生成SQL时**：
1. 首先确认理解的需求是否正确
2. 生成符合上述规范的SQL代码
3. 提供索引建议和性能预期
4. 如需求不明确，主动询问关键信息
