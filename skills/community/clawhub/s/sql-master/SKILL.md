---
name: sql-master
description: SQL 查询、数据获取智能体。覆盖 SQL 全链路能力：自然语言转生产级 SQL、慢查询诊断与执行计划分析、索引设计与优化、数仓建模、SQL 原理深度科普、查询结果可视化。支持 MySQL / PostgreSQL / Hive / Spark SQL / ClickHouse / BigQuery 多方言。触发场景：(1) 写 SQL / 生成查询，(2) SQL 慢/优化/调优，(3) 执行计划分析 EXPLAIN，(4) 索引设计，(5) 数仓建模 / 分层设计，(6) SQL 原理问题（事务/锁/MVCC/Join算法等），(7) 表结构设计 DDL，(8) SQL 报错诊断，(9) 任何"帮我写个查询"、"这个SQL为什么慢"、"怎么建索引"类请求，(10) 查询结果可视化 / 出图 / 图表 / 数据展示。
---

# SQL Master — SQL 查询、数据获取智能体

## ⚠️ 使用前必读

本 Skill 需要 Python 依赖。**首次使用前必须安装依赖**：

```bash
skillhub_install install_skill sql-master
```

工具会自动检测 Python3 环境、pip 可用性，并安装所有依赖。

### 依赖安装方式

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| **自动安装（推荐）** | `skillhub_install install_skill sql-master` | 一键安装，自动处理 |
| **手动安装** | `pip install -r requirements.txt` | 熟悉 Python 环境的用户 |

### 无依赖使用（受限模式）

如果无法安装依赖，本 Skill 提供以下**降级能力**：

✅ **可用功能**：
- SQL 语句生成（纯文本输出，无需执行）
- SQL 诊断与优化建议（基于文本分析）
- 索引设计建议（基于规则引擎）
- SQL 原理解释与科普
- 执行计划分析（用户提供 EXPLAIN 结果）

❌ **不可用功能**：
- 数据库连接与 SQL 执行
- 数据 Pipeline 处理
- 本地文件数据获取（CSV/Excel 等）
- 与 sql-dataviz / sql-report-generator 联动

---

## 🔗 Skill 协作关系

本 Skill 与 **sql-dataviz**、**sql-report-generator** 组成完整的数据分析流水线：

```
┌─────────────┐     ┌──────────────┐     ┌────────────────────────┐
│ sql-master  │ ──► │ sql-dataviz  │ ──► │ sql-report-generator   │
│  (数据层)   │     │  (可视化层)  │     │  (报告层)              │
└─────────────┘     └──────────────┘     └────────────────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
   SQL 查询           图表生成            HTML 报告
   数据获取           PNG/HTML            AI 洞察
   格式转换           Dashboard           数据表格
```

### 协作模式

| 模式 | 组合 | 适用场景 |
|------|------|---------|
| **单独使用** | sql-master | 仅需 SQL 查询/生成/优化 |
| **可视化** | sql-master + sql-dataviz | SQL 查询 → 图表输出 |
| **完整流程** | sql-master + sql-dataviz + sql-report-generator | 完整数据分析报告 |

### 🥇 最优使用方式：三 Skill 串联

```python
from scripts.unified_pipeline import UnifiedPipeline

result = (
    UnifiedPipeline("销售分析")
    .from_file("sales.csv")                                    # sql-master: 数据获取
    .query("SELECT region, SUM(sales) as total FROM data GROUP BY region")
    .interactive_chart("bar", x_col="region", y_col="total")   # sql-dataviz: 可视化
    .insights(value_cols=["total"])                            # AI 洞察
    .report(title="销售报告", output="report.html")            # sql-report-generator: 报告
)
```

### 决策指南

```
你需要什么？
├─ 仅 SQL 查询/优化 → sql-master 单独使用
├─ SQL + 图表 → sql-master + sql-dataviz
├─ 图表 + 报告（无 SQL）→ sql-dataviz + sql-report-generator
└─ 完整分析报告 → sql-master + sql-dataviz + sql-report-generator ✅ 推荐
```

---

## 新增功能：统一 Pipeline 编排（三 Skill 端到端）

### `scripts/unified_pipeline.py`

打通 sql-master → sql-dataviz → sql-report-generator 的端到端自动化：

```python
from scripts.unified_pipeline import UnifiedPipeline, analyze_file

# 完整 Pipeline
result = (
    UnifiedPipeline("销售分析")
    .from_file("sales.csv")                        # 数据源
    .query("SELECT region, SUM(sales) as total FROM data GROUP BY region")  # SQL
    .interactive_chart("bar", x_col="region", y_col="total", title="区域销售")  # 交互图
    .chart("line", x_col="region", y_col="total")              # 静态图 (PNG)
    .insights(value_cols=["total"])                            # AI 洞察
    .report(title="销售报告", output="report.html")           # 完整报告
)
print(result.log())

# 一键分析
result = analyze_file("sales.csv", output="report.html")
```

**支持的图表**：静态 PNG（60种）+ 交互式 HTML（12种）
**支持的洞察**：异常检测 / 趋势 / 相关性 / TOP N / 分布 / 季节性 / 对比
**支持的报告**：完整 HTML（图表 + 洞察 + 数据表格 + KPI 卡片）

## 新增功能：数据库连接执行层 + 数据 Pipeline

### 1. 数据库连接（scripts/database_connector.py）

支持 SQLite / MySQL / PostgreSQL / SQL Server / ClickHouse / Oracle

```python
from scripts.database_connector import connect_sqlite, connect_mysql, connect_postgresql

# SQLite（本地文件）
conn = connect_sqlite("data/sales.db")
result = conn.execute("SELECT region, SUM(amount) FROM sales GROUP BY region")
print(result.df)           # DataFrame 访问
print(result.to_dict())   # dict 访问
result.to_csv("output.csv")  # 导出 CSV
result.to_json("output.json") # 导出 JSON

# MySQL
conn = connect_mysql(host="localhost", port=3306, username="root", password="xxx", database="mydb")
result = conn.execute("SELECT * FROM orders WHERE date >= '2024-01-01'")
print(result.summary())   # 可读摘要

# PostgreSQL
conn = connect_postgresql(host="localhost", database="mydb", username="postgres", password="xxx")
tables = conn.get_tables()  # 获取所有表名
schema = conn.get_schema("orders")  # 获取表结构
conn.close()
```

### 2. 本地文件数据获取（scripts/file_connector.py）

支持 CSV / Excel / JSON / Parquet / SQLite 等所有主流格式，自动 SQL 查询 + 格式转换

```python
from scripts.file_connector import load_file, load_directory

# 加载本地文件
fc = load_file("data/sales.csv")        # 单个文件
fc = load_directory("data/reports/")     # 目录下所有文件
fc = load_file("data/*.csv")            # 通配符匹配

print(fc.shape)           # (10000, 12)
print(fc.columns)         # ['date', 'region', 'amount', ...]
print(fc.df.head())       # DataFrame

# 用途一：SQL 查询（自动建 SQLite 内存表）
result = fc.query("SELECT region, SUM(amount) as total FROM data GROUP BY region ORDER BY total DESC")

# 用途二：格式转换
fc.to_csv("output/sales_report.csv")
fc.to_excel("output/sales_report.xlsx")
fc.to_json("output/sales_report.json")
fc.to_parquet("output/sales_report.parquet")
fc.to_sqlite("output/sales.db", table_name="sales")

# 用途三：传给 sql-dataviz 画图
b64 = fc.to_dataviz("line", x_col="month", y_col="sales", title="月度销售趋势")
```

### 3. SQL Pipeline 流水线（scripts/pipeline.py）

三大用途一气呵成：数据获取 → SQL 查询 → 格式转换 → 可视化 → HTML 报告

```python
from scripts.pipeline import SQLPipeline

# 方式一：从文件开始
p = (
    SQLPipeline()
    .from_file("data/sales.csv")
    .query("SELECT region, SUM(amount) as total FROM data GROUP BY region")
    .to_csv("output/regional_sales.csv")
    .to_excel("output/regional_sales.xlsx")
)

# 方式二：从数据库开始
p = SQLPipeline().from_db(dialect="sqlite", database="data.db")
p.query("SELECT * FROM sales WHERE amount > 1000")
p.query("SELECT region, COUNT(*) FROM data GROUP BY region")

# 方式三：从 DataFrame 开始
import pandas as pd
df = pd.read_csv("data.csv")
p = SQLPipeline().from_dataframe(df)

# 管道操作
p.query("SELECT region, SUM(amount) as total FROM data GROUP BY region")
p.transform(lambda df: df[df["total"] > 1000])  # 过滤
p.to_dataviz("bar", x_col="region", y_col="total", title="区域销售排行")
p.to_report(title="销售分析报告", output="output/report.html")
p.log()   # 打印执行日志
```

**Pipeline 完整流程示例：**
```python
(
    SQLPipeline()
    .from_file("sales_2024.csv")                        # 加载数据
    .query("SELECT * FROM data WHERE region = '华东'")  # SQL 筛选
    .to_csv("output/east_sales.csv")                   # 导出 CSV
    .to_json("output/east_sales.json")                 # 导出 JSON
    .to_dataviz("line", x_col="month", y_col="sales") # 生成折线图
    .to_dataviz("pie", x_col="product", y_col="amount") # 生成饼图
    .to_report(title="华东区域销售报告", output="output/report.html")  # HTML 报告
)
```

## 核心原则

**生产级标准**：所有输出的 SQL 必须满足：
- 注释完整（业务背景 + 性能预期 + 适用数据量级）
- 明确标注数据库版本和方言
- 主动提示 NULL 处理、空集合、边界条件
- 给出多方案时说明各自 trade-off

**分层回答**：同一问题，先给结论，再给原理，最后给深入扩展。自动识别用户水平（初学者/开发者/DBA），调整解释深度。

**可复现**：生成的 SQL 必须附带最小可复现测试数据（DDL + INSERT），确保用户能直接验证。

---

## 功能模块导航

| 场景 | 参考文件 |
|------|---------|
| 自然语言 → SQL 生成 | [references/sql-generation.md](references/sql-generation.md) |
| 慢查询诊断 & 执行计划分析 | [references/query-optimization.md](references/query-optimization.md) |
| 索引设计策略 | [references/index-design.md](references/index-design.md) |
| 数仓建模 & 分层架构 | [references/data-warehouse.md](references/data-warehouse.md) |
| Hive 数据倾斜深度（引擎原理/量化模型/极端场景） | [references/hive-skew-advanced.md](references/hive-skew-advanced.md) |
| SQL 原理深度（事务/锁/MVCC/Join） | [references/sql-internals.md](references/sql-internals.md) |
| 多方言差异速查 | [references/dialect-guide.md](references/dialect-guide.md) |
| DDL 设计规范 | [references/ddl-design.md](references/ddl-design.md) |
| SQL 安全规范（注入防护/参数化查询） | [references/sql-security.md](references/sql-security.md) |
| CLI 实操速查（sqlite3/psql/mysql 连接与导入导出） | [references/cli-quickref.md](references/cli-quickref.md) |
| 查询结果可视化（图表选型/Python 代码/设计原则） | [references/visualization-guide.md](references/visualization-guide.md) |

---

## 工作流程

### 1. 意图识别
收到请求后，先判断属于哪个场景：
- **生成类**：用户描述业务需求，需要输出 SQL
- **优化类**：用户提供现有 SQL 或 EXPLAIN，需要诊断和改写
- **设计类**：表结构、索引、数仓架构设计
- **科普类**：原理解释、概念问答
- **诊断类**：报错信息分析
- **可视化类**：将查询结果转化为图表 → 加载 [references/visualization-guide.md](references/visualization-guide.md)

### 2. 上下文收集
生成或优化 SQL 前，主动确认（如未提供）：
- 数据库类型和版本
- 关键表的 schema（列名、类型、索引）
- 数据量级（行数、数据大小）
- 查询频率和性能目标（P99 < Xms？）

### 3. 输出规范

**SQL 输出模板**：
```sql
-- ============================================================
-- 业务说明：[描述这段 SQL 解决什么业务问题]
-- 数据库：MySQL 8.0 / PostgreSQL 15 / ...
-- 性能预期：[预计执行时间，适用数据量级]
-- 注意事项：[NULL 处理、边界条件、已知限制]
-- ============================================================

SELECT ...
FROM ...
WHERE ...
```

**优化报告模板**：
```
## 问题诊断
[执行计划中发现的问题，按严重程度排序]

## 优化方案
### 方案 A（推荐）
[改写后的 SQL + 原因]

### 方案 B（备选）
[另一种思路 + 适用场景]

## 预期收益
[优化前 vs 优化后的性能对比估算]

## 可复现测试
[最小 DDL + 数据 + 验证步骤]
```

### 4. 加载参考文件
根据意图识别结果，读取对应的 references/ 文件获取详细指导。

---

## 快速参考

### 常见性能陷阱（立即识别）
- `SELECT *` → 明确列名，避免回表
- `WHERE` 列上有函数 → 索引失效
- `OR` 连接不同列 → 考虑 UNION ALL
- `!=` / `NOT IN` → 无法走索引
- 隐式类型转换 → 索引失效
- `LIMIT` 大偏移量 → 延迟关联优化
- `COUNT(*)` vs `COUNT(col)` → NULL 语义差异

### Join 算法选择直觉
- 小表 JOIN 大表 → Nested Loop（小表驱动）
- 两个大表等值 JOIN → Hash Join
- 有序数据等值 JOIN → Merge Join
- 数据倾斜 → 广播小表 / 加盐打散

### 索引设计口诀
**最左前缀、区分度高、覆盖查询、避免冗余**

---

## 强制规范（MUST DO / MUST NOT）

借鉴 sql-pro 的约束清单，以下规则在任何情况下都必须遵守：

### ✅ MUST DO
- 优化前**必须先分析执行计划**（EXPLAIN / EXPLAIN ANALYZE）
- 优先使用**集合操作**，避免逐行处理（游标/循环）
- **尽早过滤**：WHERE 条件尽量前置，减少中间结果集
- 存在性检查用 `EXISTS`，不用 `COUNT(*) > 0`
- **显式处理 NULL**：IS NULL / IS NOT NULL / COALESCE / NULLIF
- 为高频查询创建**覆盖索引**
- 涉及安全场景时，必须使用**参数化查询**，详见 [references/sql-security.md](references/sql-security.md)
- 跨数据库迁移时，必须标注**方言差异**，详见 [references/dialect-guide.md](references/dialect-guide.md)

### ❌ MUST NOT
- 不在 WHERE / JOIN 条件列上使用函数（导致索引失效）
- 不用 `SELECT *`（回表开销 + 隐式依赖）
- 不用字符串拼接构造 SQL（SQL 注入风险）
- 不在大表上做无索引的全表扫描
- 不用 `OFFSET` 大偏移量分页（改用游标/keyset 分页）
- 不忽略隐式类型转换（导致索引失效 + 数据截断）
- 不在生产环境直接运行未经 EXPLAIN 验证的复杂查询

