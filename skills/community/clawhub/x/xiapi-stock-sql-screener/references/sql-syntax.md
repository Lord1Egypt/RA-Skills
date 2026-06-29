# SQL 语法说明

本文档详细说明大虾皮 SQL 股票筛选器支持的 SQL 语法。

## 基本结构

SQL 查询的基本结构为：

```
<WHERE 条件> [ORDER BY <排序字段>] [LIMIT <数量限制>]
```

**注意**：不支持 SELECT 和 FROM 语句，只支持 WHERE 条件、ORDER BY 和 LIMIT。

## WHERE 条件

### 比较运算符

| 运算符 | 说明 | 示例 |
| ------ | ---- | ---- |
| `=` | 等于 | `date='2026-06-17'` |
| `!=` 或 `<>` | 不等于 | `isVCP!=1` 或 `isVCP<>1` |
| `>` | 大于 | `rps_score>70` |
| `<` | 小于 | `cs<15` |
| `>=` | 大于等于 | `sctr>=60` |
| `<=` | 小于等于 | `zdf<=5` |

### 区间运算符

| 运算符 | 说明 | 示例 |
| ------ | ---- | ---- |
| `in [...]` | 区间范围（闭区间） | `cs in [0, 15]` 表示 cs >= 0 AND cs <= 15 |
| `in (...)` | IN 枚举 | `stockId in ('000001', '600031')` |

**区间运算符说明**：

- `in [min, max]`：表示字段值在 min 和 max 之间（闭区间）
- 等价于：`field >= min AND field <= max`
- 示例：`cs in [0, 15]` 等价于 `cs>=0 AND cs<=15`

### 字段间比较

支持字段与字段之间的比较：

```sql
rps_score>sctr
```

表示 RPS 强度大于 SCTR 技术排名。

### 逻辑运算符

| 运算符 | 说明 | 示例 |
| ------ | ---- | ---- |
| `AND` | 逻辑与 | `rps_score>70 AND sctr>60` |
| `OR` | 逻辑或 | `isVCP=1 OR isSOS=1` |

**逻辑运算符优先级**：

- `AND` 优先级高于 `OR`
- 示例：`rps_score>70 OR sctr>60 AND cs>0` 等价于 `rps_score>70 OR (sctr>60 AND cs>0)`

### 括号嵌套

支持使用括号改变逻辑优先级：

```sql
(rps_score>70 OR sctr>60) AND cs>0
```

表示：RPS>70 或 SCTR>60，且 CS>0。

## ORDER BY 排序

支持多字段排序：

```sql
ORDER BY field1 ASC, field2 DESC
```

| 关键字 | 说明 |
| ------ | ---- |
| `ASC` | 升序（默认） |
| `DESC` | 降序 |

**示例**：

```sql
ORDER BY rps_score DESC, sctr DESC
```

表示：按 RPS 降序排序，RPS 相同的按 SCTR 降序排序。

## LIMIT 数量限制

限制返回的股票数量：

```sql
LIMIT 10
```

表示：最多返回 10 条记录。

**注意**：

- LIMIT 必须为正整数
- 默认不限制数量（返回所有符合条件的股票）

## 完整示例

### 单条件查询

```sql
date='2026-06-17' AND rps_score>70 LIMIT 20
```

查询 2026-06-17 日期，RPS>70 的股票，最多返回 20 条。

### 多条件组合

```sql
date='2026-06-17' AND rps_score>70 AND sctr>60 AND cs>0 ORDER BY rps_score DESC LIMIT 10
```

查询 RPS>70、SCTR>60、CS>0 的股票，按 RPS 降序排序，最多返回 10 条。

### 区间范围查询

```sql
date='2026-06-17' AND cs in [0, 15] AND rps_score>70 LIMIT 15
```

查询 CS 在 0-15 之间、RPS>70 的股票，最多返回 15 条。

### 逻辑组合查询

```sql
date='2026-06-17' AND (isVCP=1 OR isSOS=1) AND rps_score>70 ORDER BY sctr DESC LIMIT 20
```

查询 VCP 或 SOS 形态、RPS>70 的股票，按 SCTR 降序排序，最多返回 20 条。

### 字段间比较查询

```sql
date='2026-06-17' AND rps_score>sctr AND cs>0 LIMIT 10
```

查询 RPS 大于 SCTR、CS>0 的股票，最多返回 10 条。

## 语法限制

### 必须包含 date 条件

所有查询必须包含 `date='YYYY-MM-DD'` 条件。

**错误示例**：

```sql
rps_score>70 LIMIT 10
```

**正确示例**：

```sql
date='2026-06-17' AND rps_score>70 LIMIT 10
```

### 日期限制

只支持查询最近 10 天内的股票数据。

**错误示例**：

```sql
date='2026-01-01' AND rps_score>70
```

**正确示例**：

```sql
date='2026-06-17' AND rps_score>70
```

### 不支持的语法

以下 SQL 语法不支持：

- `SELECT` 语句
- `FROM` 语句
- `GROUP BY` 语句
- `HAVING` 语句
- `JOIN` 语句
- 子查询
- 聚合函数（SUM、AVG、COUNT 等）
- 字符串函数（CONCAT、SUBSTRING 等）
- 数学函数（ABS、ROUND 等）

## 字符串值

字符串值必须用单引号或双引号包围：

```sql
date='2026-06-17'
stockId='000001'
name='平安银行'
```

## 数值值

数值值不需要引号：

```sql
rps_score>70
cs<15
isVCP=1
```

## 常见错误

### 1. 缺少 date 条件

**错误**：

```sql
rps_score>70 LIMIT 10
```

**修复**：添加 date 条件

```sql
date='2026-06-17' AND rps_score>70 LIMIT 10
```

### 2. 日期格式错误

**错误**：

```sql
date='2026/06/17'
```

**修复**：使用 YYYY-MM-DD 格式

```sql
date='2026-06-17'
```

### 3. 字符串值缺少引号

**错误**：

```sql
stockId=000001
```

**修复**：添加引号

```sql
stockId='000001'
```

### 4. 区间运算符格式错误

**错误**：

```sql
cs in (0, 15)
```

**修复**：使用方括号表示区间

```sql
cs in [0, 15]
```

### 5. 逻辑运算符大小写错误

**错误**：

```sql
rps_score>70 and sctr>60
```

**修复**：使用大写

```sql
rps_score>70 AND sctr>60
```

## 最佳实践

### 1. 始终包含 date 条件

确保查询结果准确，避免查询过期数据。

### 2. 使用合理的 LIMIT

避免返回过多数据，影响性能和可读性。

### 3. 使用 ORDER BY 排序

按关键指标排序，便于识别最强标的。

### 4. 使用括号明确逻辑

复杂逻辑条件使用括号，避免优先级混淆。

### 5. 使用区间运算符简化条件

`cs in [0, 15]` 比 `cs>=0 AND cs<=15` 更简洁。

## 参考文档

- [字段列表](field-list.md)：查看所有支持的查询字段
- [常用查询示例](query-examples.md)：查看更多查询示例