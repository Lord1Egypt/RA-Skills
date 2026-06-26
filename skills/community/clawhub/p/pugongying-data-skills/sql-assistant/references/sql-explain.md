---
name: sql-explain
description: |
  SQL执行计划分析专家 - 解读EXPLAIN输出，识别性能瓶颈，提供可视化分析和优化建议。
  当用户提供SQL执行计划、分析慢查询、优化查询性能时触发。
  触发词：分析执行计划、EXPLAIN解读、慢查询分析、查询性能问题。
argument: { description: "SQL执行计划内容或包含执行计划的文件路径", required: true }
agent: Explore
allowed-tools: [Read, Grep, Glob]
---

# SQL执行计划分析器

深度解读SQL执行计划，识别性能瓶颈，提供针对性优化建议。

## 支持的数据库

### MySQL / MariaDB
- 标准 `EXPLAIN` 输出
- `EXPLAIN ANALYZE` (MySQL 8.0.18+)
- `EXPLAIN FORMAT=JSON`

### PostgreSQL
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)`
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT XML)`

### SQL Server
- `SET SHOWPLAN_ALL ON`
- `SET STATISTICS PROFILE ON`
- 图形化执行计划XML

### Oracle
- `EXPLAIN PLAN FOR` + `DBMS_XPLAN.DISPLAY`
- `AUTOTRACE` 输出

### 其他
- SQLite `EXPLAIN QUERY PLAN`
- ClickHouse `EXPLAIN`
- BigQuery Execution Details

## 分析维度

### 1. 执行概览
- **总执行时间**（规划时间 + 执行时间）
- **预估 vs 实际行数**（差异分析）
- **I/O统计**（缓存命中、磁盘读取）
- **内存使用**（哈希表、排序区）

### 2. 访问路径分析
- **全表扫描**（Seq Scan / Full Table Scan）🔴
- **索引扫描**（Index Scan / Index Seek）🟢
- **索引覆盖**（Index Only Scan / Covering Index）🟢
- **范围扫描**（Range Scan）🟡
- **Bitmap扫描**（Bitmap Index Scan）🟡

### 3. JOIN策略分析
- **Nested Loop Join** - 小表驱动大表 🟡
- **Hash Join** - 大数据量，无索引 🟢
- **Merge Join** - 有序数据，等值连接 🟢
- **笛卡尔积**（Cartesian Product）🔴

### 4. 排序和聚合
- **文件排序**（Filesort / External Sort）🔴
- **内存排序**（Quick Sort / Top-N）🟢
- **临时表**（Temporary / Hashed Temporary）🔴
- **流式聚合**（Stream Aggregate）🟢
- **哈希聚合**（Hash Aggregate）🟡

### 5. 瓶颈识别
- 最耗时的操作节点
- 数据倾斜（实际行数 >> 预估行数）
- 重复扫描
- 随机I/O过多

## 输出格式

```markdown
# SQL执行计划分析报告

## 基本信息
- **数据库类型**：[PostgreSQL/MySQL/SQL Server/Oracle/...]
- **分析时间**：YYYY-MM-DD
- **SQL复杂度**：[简单/中等/复杂]
- **风险等级**：🟢良好 / 🟡注意 / 🔴严重

## 执行概览

| 指标 | 数值 | 评级 |
|------|------|------|
| 总执行时间 | X ms | 🟢/🟡/🔴 |
| 规划时间 | X ms | 🟢/🟡/🔴 |
| 预估/实际扫描行数 | X / Y 行 | 🟢/🟡/🔴 |
| 返回行数 | Z 行 | - |
| I/O操作 | X 次读取 | 🟢/🟡/🔴 |
| 缓存命中率 | X% | 🟢/🟡/🔴 |

## 执行计划可视化

```
┌─────────────────────────────────────────────────────────────────────┐
│ [Node Type] (cost=X..Y rows=N) (actual time=A..B rows=M loops=L)    │
│ ├── [Child Node 1]                                                  │
│ │   [Details]                                                       │
│ │   🔴/🟡/🟢 [Status] - [Brief Description]                        │
│ └── [Child Node 2]                                                  │
│     [Details]                                                       │
│     🔴/🟡/🟢 [Status] - [Brief Description]                        │
└─────────────────────────────────────────────────────────────────────┘
```

## 关键发现

### 🔴 严重问题
1. **[问题类型]** [问题描述]
   - **位置**：[执行计划节点]
   - **影响**：[性能影响描述]
   - **证据**：[具体指标]
   - **修复建议**：[具体方案]

### 🟡 警告问题
1. **[问题类型]** [问题描述]
   - **建议**：[优化建议]

### 🟢 良好实践
1. **[优化点]** [正面描述]

## 详细节点分析

### 节点 #N: [操作类型]

| 属性 | 值 |
|------|-----|
| **操作** | ... |
| **成本** | cost=X..Y |
| **实际执行** | time=A..B ms, rows=M, loops=L |
| **I/O** | shared hit=X, read=Y |
| **条件/过滤** | ... |

**分析**：
[详细分析说明]

**建议**：
[优化建议]

## 优化建议汇总

### 立即执行（高优先级）
1. [建议1]
2. [建议2]

### 建议执行（中优先级）
1. [建议3]

### 可选优化（低优先级）
1. [建议4]

## 索引优化建议

```sql
-- 建议创建的索引
CREATE INDEX ...
```

## SQL重写建议（如需要）

```sql
-- 优化后的SQL
...
```

## 监控建议

[需要持续监控的指标]
```

## 性能评级标准

### 执行时间评级
- 🟢 **优秀**：< 10ms
- 🟢 **良好**：10ms - 100ms
- 🟡 **一般**：100ms - 1s
- 🔴 **较差**：1s - 10s
- 🔴 **严重**：> 10s

### 扫描效率评级（扫描行数 / 返回行数）
- 🟢 **优秀**：< 10:1
- 🟡 **一般**：10:1 - 100:1
- 🔴 **较差**：100:1 - 1000:1
- 🔴 **严重**：> 1000:1

### I/O效率评级（磁盘读取比例）
- 🟢 **优秀**：磁盘读取 < 5%
- 🟡 **一般**：磁盘读取 5% - 20%
- 🔴 **较差**：磁盘读取 20% - 50%
- 🔴 **严重**：磁盘读取 > 50%

## 数据库特定解析

### MySQL EXPLAIN 字段解读

| 字段 | 含义 | 关键值 |
|------|------|--------|
| type | 访问类型 | 🟢 system/const/eq_ref/ref 🟡 range/index 🔴 ALL |
| Extra | 额外信息 | 🔴 Using filesort, Using temporary 🟢 Using index |
| rows | 预估扫描行数 | 越小越好 |
| key | 实际使用的索引 | NULL表示无索引 |

### PostgreSQL 关键指标

| 指标 | 含义 | 关注点 |
|------|------|--------|
| cost=X..Y | 启动成本..总成本 | Y值越小越好 |
| actual time=A..B | 实际启动..总时间 | B值是实际耗时 |
| loops=N | 执行次数 | N>1表示嵌套循环 |
| Buffers: shared hit/read | 缓存命中/磁盘读取 | read越小越好 |

### SQL Server 图形计划

| 图标 | 含义 | 状态 |
|------|------|------|
| Table Scan | 全表扫描 | 🔴 |
| Clustered Index Scan | 聚集索引扫描 | 🟡 |
| Clustered Index Seek | 聚集索引查找 | 🟢 |
| Index Scan | 索引扫描 | 🟡 |
| Index Seek | 索引查找 | 🟢 |
| Key Lookup | 键查找 | 🟡 |
| Sort | 排序 | 🟡 |

## 常见优化模式

### 场景1：全表扫描优化
```
问题：Seq Scan on large_table
解决：
1. 添加 WHERE 条件索引
2. 考虑分区表
3. 使用覆盖索引避免回表
```

### 场景2：文件排序优化
```
问题：Using filesort / Sort (cost=...)
解决：
1. 添加 ORDER BY 字段索引
2. 减少排序数据量（先过滤）
3. 评估是否必须排序
```

### 场景3：临时表优化
```
问题：Using temporary / Hashed Temporary
解决：
1. 优化 GROUP BY / ORDER BY 字段
2. 增加 work_mem / sort_buffer_size
3. 简化查询逻辑
```

## 分析流程

1. **识别数据库类型** - 根据执行计划格式判断
2. **提取关键指标** - 总时间、扫描行数、I/O
3. **构建执行树** - 理解执行顺序
4. **识别瓶颈点** - 最耗时操作
5. **分析访问路径** - 索引使用情况
6. **检查JOIN策略** - JOIN效率
7. **识别警告信号** - filesort、temporary
8. **生成优化建议** - 针对性改进

## 当前分析对象

$ARGUMENTS

---

**分析时**：
1. 首先识别数据库类型和执行计划格式
2. 提取关键性能指标
3. 用可视化树形图展示执行计划
4. 识别并标注严重问题（🔴）、警告（🟡）、良好实践（🟢）
5. 为每个问题节点提供详细分析和修复建议
6. 提供优化后的SQL（如需要）
