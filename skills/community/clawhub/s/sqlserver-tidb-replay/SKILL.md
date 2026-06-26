# SQL Server → TiDB SQL 回放工具

## 工具简介

参考 [Bowen-Tang/sql-replay](https://github.com/Bowen-Tang/sql-replay)（MySQL → TiDB 流量回放工具），实现 **SQL Server → TiDB** 的 SQL 回放能力。

**核心用途**：
- 数据库迁移前：验证 SQL 兼容性
- 迁移后：对比性能差异 + 生成语法转换建议
- 压测：模拟真实业务负载

**参考来源**：GitHub - Bowen-Tang/sql-replay: mysql slow query replay

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  ① 采集 (collect)                                          │
│  SQL Server 慢查询日志 → CSV（非标准 XE 格式）             │
│  ⚠️ 需要转换为标准 SQL 格式                                │
│  目标：sqlserver.sql_statement_completed 事件              │
└─────────────────────────────────────────────────────────────┘
                            ↓ CSV 文件
┌─────────────────────────────────────────────────────────────┐
│  ② CSV 转标准 SQL (csv_to_sql)                            │
│  解析原始日志 → 标准 SQL 语句                              │
│  功能：去除 XE 前缀符号、提取 SQL 文本、格式化             │
└─────────────────────────────────────────────────────────────┘
                            ↓ 标准 SQL CSV
┌─────────────────────────────────────────────────────────────┐
│  ③ 解析 (parse)                                            │
│  CSV → Python 解析 → JSON 中间格式                         │
│  功能：去重、过滤无效SQL、生成可回放JSON                    │
└─────────────────────────────────────────────────────────────┘
                            ↓ JSON 文件
┌─────────────────────────────────────────────────────────────┐
│  ④ 回放 (replay)                                           │
│  JSON → Python 回放脚本 → TiDB 并行执行                    │
│  功能：连接池、并发执行、按 conn_id 串行                   │
│  输出：results_{task_name}.json                            │
└─────────────────────────────────────────────────────────────┘
                            ↓ 结果 JSON
┌─────────────────────────────────────────────────────────────┐
│  ⑤ 分析 (analyze)                                          │
│  结果 JSON → 分析脚本                                       │
│  功能：                                                      │
│  - 识别语法不兼容问题                                       │
│  - 性能对比分析（TiDB vs SQL Server）                       │
│  - 自动生成语法转换建议（转换前/后/点）                     │
│  - HTML 报告（含语法转换对照表）                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 前置准备

### 环境要求
- Python 3.8+
- pymysql（连接 TiDB）
- pandas（解析 CSV）
- PowerShell 5.1+（采集用，Windows 环境）

### TiDB 连接信息
```bash
# 方式一：配置环境变量
export TIDB_HOST="your-tidb-host"
export TIDB_PORT="4000"
export TIDB_USER="root"
export TIDB_PASSWORD="your-password"
export TIDB_DATABASE="test_db"

# 方式二：命令行参数传入（优先级更高）
```

---

## 核心功能说明

### CSV 转标准 SQL（关键步骤）

SQL Server 慢查询日志导出的 CSV **不是标准的 XE 格式**，包含大量 XE 前缀符号和混合格式，需要先转换为标准 SQL 语句。

**原始 CSV 常见问题**：
- SQL 文本被截断或换行
- 包含 XE 事件前缀（如 `sql_statement_completed`、`sp_statement_completed`）
- 变量参数化符号（`@1`, `@2`, `N''` 等 Unicode 前缀）
- 多行合并问题

**转换脚本**：`csv_to_sql.py`  
自动处理：
- 去除 XE 事件前缀
- 合并被截断的 SQL（检测分号断句）
- 替换 SQL Server 特有参数格式
- 去除不可见字符

---

## 使用步骤

### ① 采集 SQL Server 慢日志

在 **Windows 服务器**上运行 PowerShell 脚本：

```powershell
# 方式一：Extended Events（推荐，结构清晰）
.\collect_xe.ps1 -SessionName "slow_query_capture" -ThresholdMs 1000 -OutputPath "C:\slow_logs\slow_20260412.csv"

# 方式二：从 SQL Server Management Studio 导出慢查询日志
# 右键 → 导出 → CSV（含 statement、duration、cpu 等字段）
```

**采集的字段**：
| 字段 | 说明 |
|------|------|
| statement | SQL 文本 |
| duration_us | 执行时间，微秒 |
| cpu_us | CPU 时间，微秒 |
| physical_reads | 物理读次数 |
| logical_reads | 逻辑读次数 |
| row_count | 返回行数 |
| start_time | 开始执行时间 |
| database_name | 所属数据库 |
| session_id | 连接 ID |

> **注意**：采集需要 `VIEW SERVER STATE` 权限。建议在测试环境运行。

---

### ② CSV 转标准 SQL 格式

```bash
python3 scripts/csv_to_sql.py \
  --input /path/to/raw_slow_query.csv \
  --output /path/to/standard_sql.csv \
  --normalize \
  --remove-prefix
```

**参数说明**：
| 参数 | 说明 |
|------|------|
| `--input` | 原始 CSV 路径 |
| `--output` | 标准 SQL CSV 输出路径 |
| `--normalize` | 规范化 SQL 格式（去除多余空白） |
| `--remove-prefix` | 去除 XE 事件前缀符号 |

**转换后字段**：
| 字段 | 说明 |
|------|------|
| sql_text | 标准 SQL 文本 |
| duration_ms | 执行时间（毫秒，标准化） |
| database_name | 数据库名 |
| session_id | 连接 ID |

---

### ③ 解析 CSV 为回放格式

```bash
python3 scripts/parse_csv.py \
  --input /path/to/standard_sql.csv \
  --output /path/to/slow_20260412.format.json \
  --filter-type select,insert,update,delete \
  --filter-duration-ms 1000 \
  --remove-admin \
  --lang cn
```

**解析输出 JSON 格式**：
```json
[
  {
    "conn_id": "52",
    "start_time": "2026-04-12T10:00:01.123",
    "sql": "SELECT c FROM sbtest1 WHERE id=250438",
    "sql_type": "select",
    "duration_us": 380,
    "database": "test_db"
  }
]
```

---

### ④ 回放至 TiDB

```bash
python3 scripts/replay_tidb.py \
  --input /path/to/slow_20260412.format.json \
  --host $TIDB_HOST \
  --port $TIDB_PORT \
  --user $TIDB_USER \
  --password $TIDB_PASSWORD \
  --database $TIDB_DATABASE \
  --speed 1.0 \
  --workers 4 \
  --output-dir ./replay_results \
  --task-name "test_migration"
```

**回放输出**：
```
replay_results/
├── test_migration_conn_52.json   # 每个 conn_id 一个文件
├── test_migration_conn_88.json
└── test_migration_summary.json   # 汇总信息
```

**汇总文件格式**：
```json
{
  "task_name": "test_migration",
  "total_sqls": 1523,
  "total_errors": 12,
  "avg_duration_us": 4523,
  "max_duration_us": 128500,
  "compatibility_rate": "99.21%"
}
```

---

### ⑤ 生成分析报告（含语法转换）

```bash
python3 scripts/analyze_results.py \
  --input-dir ./replay_results \
  --task-name "test_migration" \
  --output ./replay_report.html \
  --source-db "SQL Server 2022" \
  --target-db "TiDB v8.0"
```

**报告内容**：
- ✅ SQL 兼容性统计（错误类型分布）
- ✅ 性能对比分析（TiDB vs SQL Server）
- ✅ 慢 SQL Top 10
- ✅ **语法转换对照表**（转换前 / 转换后 / 转换点）
- ✅ 迁移风险评估

---

## 语法转换功能

### 自动识别的不兼容模式

| 类别 | SQL Server 写法 | TiDB 改写 | 转换说明 |
|------|----------------|-----------|---------|
| OUTPUT clause | `INSERT INTO t OUTPUT inserted.id VALUES(...)` | `INSERT INTO t VALUES(...); SELECT LAST_INSERT_ID();` | TiDB 不支持 OUTPUT clause，用 LAST_INSERT_ID() 替代 |
| NVARCHAR | `N'Unicode字符串'` | `CAST('字符串' AS CHAR)` | TiDB 字符集差异，需显式 CAST |
| OPENJSON | `SELECT * FROM OPENJSON(@json)` | `JSON_EXTRACT(@json, '$')` | TiDB 不支持 OPENJSON，用 JSON 函数替代 |
| Sequence | `NEXT VALUE FOR seq_name` | `NEXTVAL('seq_name')` | TiDB 序列语法不同 |
| OFFSET | `OFFSET 10 ROWS FETCH NEXT 5 ROWS` | `LIMIT 5 OFFSET 10` | TiDB LIMIT...OFFSET 顺序相反 |
| TOP | `SELECT TOP 10 * FROM t` | `SELECT * FROM t LIMIT 10` | TiDB 用 LIMIT 替代 TOP |
| INTO | `SELECT * INTO #temp FROM t` | `CREATE TEMPORARY TABLE t AS SELECT...` | TiDB 不支持 SELECT INTO 临时表 |
| MERGE | `MERGE INTO t USING...` | `INSERT...ON DUPLICATE KEY UPDATE` | TiDB 不支持 MERGE，用 IODU 替代 |

### 报告中的语法转换表示例

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  语法转换记录 #12                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│  源 SQL Server：                                                             │
│  INSERT INTO orders (name, amount)                                          │
│  OUTPUT inserted.order_id                                                  │
│  VALUES ('商品A', 100)                                                      │
├────────────────────────────────────────────────────────────────────────────┤
│  转换后 TiDB：                                                               │
│  INSERT INTO orders (name, amount)                                          │
│  VALUES ('商品A', 100);                                                     │
│  SELECT LAST_INSERT_ID() AS order_id;                                       │
├────────────────────────────────────────────────────────────────────────────┤
│  转换点：                                                                   │
│  1. OUTPUT inserted.order_id → SELECT LAST_INSERT_ID()                     │
│  2. 原因：TiDB 不支持 OUTPUT clause                                        │
│  3. 影响：需应用层调整获取自增 ID 的方式                                     │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 完整使用案例

### 场景：某银行核心系统 SQL Server → TiDB 迁移验证

**背景**：银行信贷系统从 SQL Server 2019 迁移至 TiDB，需要验证 2000+ 条核心 SQL 的兼容性。

**Step 1：生产库慢日志采集**

在 SQL Server 生产库上运行（阈值设为 500ms）：
```powershell
.\collect_xe.ps1 -SessionName "credit_slow" -ThresholdMs 500 -OutputPath "C:\logs\credit_slow_20260412.csv"
```
采集结果：约 3800 条慢查询，覆盖 3 天的业务高峰期。

**Step 2：CSV 转标准 SQL**
```bash
python3 scripts/csv_to_sql.py \
  --input credit_slow_20260412.csv \
  --output credit_slow_standard.csv \
  --normalize \
  --remove-prefix
```

**Step 3：解析并过滤**
```bash
python3 scripts/parse_csv.py \
  --input credit_slow_standard.csv \
  --output credit_slow.format.json \
  --filter-type select,insert,update,delete \
  --filter-duration-ms 500 \
  --remove-admin
```
解析后：2156 条有效 SQL。

**Step 4：回放至 TiDB 测试环境**
```bash
python3 scripts/replay_tidb.py \
  --input credit_slow.format.json \
  --host 192.168.1.100 \
  --port 4000 \
  --user root \
  --password "Xszyh@315315" \
  --database credit_db \
  --speed 2.0 \
  --workers 8 \
  --output-dir ./replay_results \
  --task-name "credit_migration"
```

**Step 5：生成报告**
```bash
python3 scripts/analyze_results.py \
  --input-dir ./replay_results \
  --task-name "credit_migration" \
  --output credit_migration_report.html \
  --source-db "SQL Server 2019" \
  --target-db "TiDB v8.0"
```

**报告结果示例**：
```
迁移兼容性评估报告
===============================
源库：SQL Server 2019
目标库：TiDB v8.0
采集时间：2026-04-12
总SQL数：2156
兼容性：98.6%（错误SQL 30条）

错误分布：
  - 语法不兼容：8条（主要是 OUTPUT clause）
  - 函数不存在：12条（DB2兼容函数）
  - 字符集问题：5条（NCHAR/NVARCHAR vs CHAR/VARCHAR）
  - 杂项错误：5条

语法转换记录：
  - #1: OUTPUT clause → SELECT LAST_INSERT_ID()（12条）
  - #2: N'' Unicode前缀 → CAST() 转换（8条）
  - #3: OFFSET...FETCH → LIMIT...OFFSET（15条）
  - #4: OPENJSON → JSON_EXTRACT（5条）

高风险SQL（需手动改写）：
  1. proc_audit_insert (行12) - OUTPUT clause
  2. proc_statement_get (行89) - OPENJSON 函数
  ...

性能对比（成功SQL）：
  - TiDB 平均响应：12.3ms
  - SQL Server 平均响应：45.2ms
  - TiDB 加速比：3.7x
```

---

## 常见问题

### Q: CSV 是慢查询日志，不是标准 XE 格式怎么办？
A：这是正常情况。SQL Server 慢查询日志导出时格式不统一，需用 `csv_to_sql.py` 进行标准化转换。该脚本会自动处理换行符、XE 前缀、变量参数等问题。

### Q: Extended Events 会话对生产库性能影响大吗？
A：XE 设计为低开销，建议阈值设高一些（≥500ms）避免量太大。如果 CPU 紧张，可使用 `histogram` 目标先看分布。

### Q: 回放时出现大量连接错误？
A：检查 TiDB 连接数限制（`max_connections`），同时调整 `--workers` 参数。SQL Server 和 TiDB 的连接池模型不同，建议从 4 开始逐步加压。

### Q: 语法转换是自动的吗？
A：分析报告会**自动识别**常见的语法不兼容模式，并给出转换建议。但最终改写需人工确认，特别是涉及业务逻辑的部分。

### Q: 性能对比怎么做的？
A：回放时会记录 TiDB 执行时间，汇总文件中会与原 SQL Server 的 `duration_us` 进行对比。注意：相同数据量下对比才有意义。

### Q: 能回放存储过程吗？
A：可以，但采集的是 `sp_statement_completed` 事件。需要确保 TiDB 端有对应的存储过程（存储过程不会被自动翻译，需手动迁移）。

---

## 输出文件说明

| 文件 | 说明 |
|------|------|
| `*_raw.csv` | 原始采集数据 |
| `*_standard.csv` | 标准 SQL CSV（已转换） |
| `*.format.json` | 解析后的回放中间格式 |
| `replay_results/*.json` | 回放执行结果 |
| `replay_report.html` | 最终兼容性报告（含语法转换对照表） |

---

## 与 MySQL→TiDB 回放工具的区别

| 维度 | Bowen-Tang/sql-replay | 本工具 |
|------|----------------------|--------|
| 源数据库 | MySQL slow log | SQL Server 慢查询日志 |
| 日志格式 | MySQL slow log text | Extended Events CSV（非标准） |
| CSV 标准化 | 不需要 | 需要（csv_to_sql.py） |
| 语法转换 | 无 | 自动识别并生成转换对照表 |
| 性能对比 | 基础 | 完整对比分析 |
| 回放目标 | TiDB | TiDB |

---

*Skill 版本：1.1.0 | 参考：sql-replay v0.3.4 | 适用：SQL Server 2008+ → TiDB 5.0+*
