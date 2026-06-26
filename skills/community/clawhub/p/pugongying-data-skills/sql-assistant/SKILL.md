---
name: sql-assistant
description: |
  SQL智能开发助手 - 端到端SQL开发工作流。包含SQL生成、代码审查、执行计划分析三大核心功能。
  当用户需要生成SQL查询、审查SQL代码质量、分析执行计划性能时触发。
  触发词：生成SQL、SQL审查、执行计划分析、优化SQL、查询性能问题。
---

# SQL智能开发助手

从自然语言需求到高性能SQL的完整工作流。三个阶段：生成 → 审查 → 分析优化。

## 架构概览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SQL智能开发助手架构                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   用户需求 ───────┬──────────────────────────────────────────►     │
│                   │                                                │
│   ┌───────────────▼────────────────┐                              │
│   │  阶段1: SQL生成 (sql-generator) │                              │
│   │  - 自然语言转SQL                │                              │
│   │  - 多数据库方言支持              │                              │
│   └───────────────┬────────────────┘                              │
│                   │                                                │
│   ┌───────────────▼────────────────┐                              │
│   │  阶段2: SQL审查 (sql-reviewer)  │                              │
│   │  - 性能/安全/可读性审查         │                              │
│   │  - 静态代码分析                 │                              │
│   └───────────────┬────────────────┘                              │
│                   │                                                │
│   ┌───────────────▼────────────────┐                              │
│   │  阶段3: 执行计划分析 (sql-explain)│                            │
│   │  - EXPLAIN解读                 │                              │
│   │  - 瓶颈识别与优化               │                              │
│   └────────────────────────────────┘                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 参考资料导航

| 需要时读取 | 文件 | 内容 |
|-----------|------|------|
| SQL编写规范 | [references/sql-standards.md](references/sql-standards.md) | 命名规范、方言差异、优化checklist、反模式 |
| 使用示例 | `examples/` 目录 | 典型场景的输入输出示例 |

## 快速开始

### 方式1：分阶段使用（推荐）

```bash
# 阶段1：生成SQL
/sql-gen 查询过去30天各品类销售数据，按销售额降序

# 阶段2：审查生成的SQL
/sql-review [生成的SQL代码]

# 阶段3：分析执行计划（在生产环境执行后）
/sql-explain [EXPLAIN输出结果]
```

### 方式2：端到端工作流

```bash
# 启动完整SQL开发工作流
/sql-assistant 端到端开发：查询最近30天活跃用户
```

## 核心功能详解

### 功能1：SQL生成器 (/sql-gen)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 自然语言转SQL
- 复杂多表JOIN生成
- 窗口函数编写
- 特定数据库方言适配

**输入格式**：
```
/sql-gen [业务需求描述] [可选：数据库类型]
```

**示例**：
```
/sql-gen 使用MySQL语法，查询过去7天每天的新增用户数，
         要求显示日期、新增用户数、环比增长百分比
```

**输出规范**：
- 带版本头注释（查询目的、数据库类型、生成时间）
- 使用CTE而非嵌套子查询
- 包含执行建议和索引提示
- 遵循 references/sql-standards.md 中的命名规范

---

### 功能2：SQL审查器 (/sql-review)

**Agent类型**：Explore
**工具权限**：Read, Grep, Glob

**使用场景**：
- 代码Review前检查
- 生产SQL性能预审
- 团队规范合规检查
- 学习SQL最佳实践

**输入格式**：
```
/sql-review [SQL代码或文件路径]
```

**审查维度**：
1. **性能问题** 🔴 - 索引失效、全表扫描、大偏移分页等
2. **代码可读性** 🟡 - 缩进、命名、注释、复杂度
3. **健壮性** 🟠 - NULL处理、除零风险、边界条件
4. **安全性** 🔴 - SQL注入、权限问题、敏感数据暴露
5. **方言兼容性** 🟢 - 语法通用性、可移植性

**输出规范**：
- 评分概览表（各维度1-10分）
- 分级问题清单（🔴严重/🟡警告/🟢建议）
- 修复代码示例
- 优化后完整SQL

---

### 功能3：执行计划分析器 (/sql-explain)

**Agent类型**：Explore
**工具权限**：Read, Grep, Glob

**使用场景**：
- 慢查询诊断
- 执行计划解读
- 索引效果验证
- 性能瓶颈定位

**输入格式**：
```
/sql-explain [EXPLAIN输出文本或文件路径]
```

**支持的数据库**：
- PostgreSQL (EXPLAIN, EXPLAIN ANALYZE, JSON格式)
- MySQL / MariaDB (EXPLAIN, EXPLAIN FORMAT=JSON)
- SQL Server (SHOWPLAN_ALL, 图形化计划)
- Oracle (DBMS_XPLAN)
- SQLite, ClickHouse, BigQuery

**输出规范**：
- 执行概览指标（时间、扫描行数、I/O、缓存命中率）
- 可视化执行树（文本图形）
- 关键发现（严重/警告/良好）
- 详细节点分析
- 索引优化建议
- SQL重写建议

---

## 标准输出格式

每个SQL开发任务输出标准化的 `sql_package.yaml`，便于下游 Skill 消费：

```yaml
sql_package:
  version: "1.0"
  metadata:
    generated_by: "sql-assistant"
    generated_at: "2024-01-15T10:00:00Z"
    sql_dialect: "MySQL|PostgreSQL|SQL Server|..."
    query_purpose: "业务用途描述"

  content:
    query_description: "查询的详细说明"
    sql_code: "SELECT ..."
    sql_hash: "sha256_hash"
    tables_involved: ["table_a", "table_b"]
    ddl_files:          # 如有建表语句
      - path: "ddl/create_table_a.sql"
        table: "table_a"

  optimization:
    indexes_suggested:
      - table: "table_a"
        columns: ["user_id", "created_at"]
        type: "composite"
    execution_notes: "执行建议和注意事项"

  performance:
    estimated_rows: 100000
    complexity: "O(n log n)"

  downstream_specs:
    - target: "etl-assistant"
      input_file: "sql_package.yaml"
      mapping:
        - "sql_code → extract_sql"
        - "tables_involved → source_tables"
```

---

## 前置强制检查

执行 `/sql-gen` 前，必须完成以下检查：

```markdown
【强制】SQL 生成前置检查清单：
- [ ] **数据库类型已确认**（MySQL/PostgreSQL/SQL Server/Oracle/其他）
  - 如果用户未指定 → 必须主动询问
  - 如果用户指定不明确 → 要求明确版本（如 MySQL 8.0 vs 5.7）
- [ ] **表结构信息已知**（有DDL或样本数据）或已在对话中提供
- [ ] **查询目的明确**（OLTP查询 vs OLAP分析）

如果任何项未确认，必须先询问用户，禁止假设默认值。
```

---

## 与下游 Skill 的联动

SQL 开发完成后，自动触发下游 Skill：

```bash
## SQL 输出后的下一步

# 步骤1: 转化为 ETL Pipeline（推荐）
/etl-assistant 基于以下 SQL 生成 ETL Pipeline：
- SQL 文件: outputs/sql_package.yaml
- 抽取逻辑: sql_code 中的 SELECT 部分
- 源表: tables_involved 列表
- 目标: [用户指定目标表]
- 调度: [用户指定调度频率]

# 步骤2: 数据质量检查
/dq-assistant 为以下查询结果建立质量监控：
- 目标表: [查询结果表]
- 检查项: 结果行数监控、数据新鲜度、异常值检测

# 步骤3: 性能测试
/test-engineer 为以下 SQL 生成性能测试：
- SQL Hash: [sql_package.metadata.sql_hash]
- 测试场景: 大数据量查询、并发查询
- 基准: 执行时间 < [用户指定阈值]
```

---

## 示例快速索引

| 需求场景 | 推荐命令 | 详情位置 |
|----------|----------|----------|
| 生成简单查询 | `/sql-gen [描述]` | [功能1](#功能1sql生成器-sql-gen) |
| 审查现有 SQL | `/sql-review [SQL]` | [功能2](#功能2sql审查器-sql-reviewer) |
| 优化慢查询 | `/sql-explain [计划]` | [功能3](#功能3执行计划分析器-sql-explain) |
| 批量生成报表 | `/sql-assistant 并行开发...` | [多Agent协作](#多agent协作流程) |
| 转化为ETL | 先生成 SQL → 调用 `/etl-assistant` | [下游联动](#与下游-skill-的联动) |

---

## 项目初始化（可选）

为团队建立标准化SQL开发工作流：

```bash
# 创建SQL开发项目骨架
bash .claude/skills/sql-assistant/scripts/init-project.sh ./sql-project "业务报表SQL库"
```

自动生成：
```
sql-project/
├── PROJECT.md          # 项目中枢（SQL清单+进度+规范）
├── standards.md        # 团队SQL规范（从references复制）
├── queries/            # SQL文件目录
│   ├── generated/      # AI生成的SQL
│   ├── reviewed/       # 已审查的SQL
│   └── production/     # 生产环境SQL
├── explain/            # 执行计划存档
│   └── YYYY-MM/        # 按月归档
└── README.md           # 项目说明
```

---

## 多Agent协作流程

复杂SQL开发任务可拆分为多Agent并行：

```
协调Agent (主会话)
    │
    ├─► sql-generator Agent #1 ──► 生成查询A
    ├─► sql-generator Agent #2 ──► 生成查询B
    │
    ▼ (收集结果)
    │
    ├─► sql-reviewer Agent #1 ──► 审查查询A
    ├─► sql-reviewer Agent #2 ──► 审查查询B
    │
    ▼ (汇总审查意见)
    │
    └─► 输出最终SQL合集
```

启动多Agent并行：
```
/sql-assistant 并行开发：需要3个销售报表查询
    1. 日销售趋势（按日期聚合）
    2. 品类销售排行（按品类聚合）
    3. 区域销售分布（按区域聚合）
要求使用PostgreSQL语法，统一命名规范
```

---

## 阶段流转与反馈循环

```
┌─────────────────────────────────────────────────────────────┐
│                        完整开发循环                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   需求 ──► [生成] ──► SQL初稿                               │
│            │        │                                       │
│            │        ▼                                       │
│            │       [审查] ──► 问题清单                       │
│            │        │                                       │
│            │        ▼ (如有严重问题)                         │
│            │       [修正] ──► 返回修改                       │
│            │        │                                       │
│            │        ▼ (审查通过)                             │
│            │       [测试] ──► 执行计划                        │
│            │        │                                       │
│            │        ▼ (性能不达标)                           │
│            └─────── [优化] ──► 索引/重写                     │
│                     │                                       │
│                     ▼ (性能达标)                             │
│                    [上线] ──► 生产部署                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 版本管理

SQL迭代版本规范：

```
查询文件名：{业务模块}_{查询描述}_v{版本号}.sql

示例：
- report_sales_daily_v1.0.0.sql
- report_sales_daily_v1.0.1.sql  # 优化索引
- report_sales_daily_v1.1.0.sql  # 增加字段
- report_sales_daily_v2.0.0.sql  # 重写逻辑
```

版本号规则：
- **PATCH (0.0.1)**：性能优化、格式调整、注释更新
- **MINOR (0.1.0)**：增加字段、调整过滤条件
- **MAJOR (1.0.0)**：重写逻辑、表结构变更、业务规则调整

---

## 最佳实践

### 1. 提示词工程

**高效需求描述公式**：
```
[数据库类型] + [业务动作] + [数据范围] + [分组维度] + [排序要求] + [特殊约束]

示例：
"使用PostgreSQL，统计2024年Q1各区域各品类的销售额和订单量，
 只包含已完成订单，按区域和销售额降序排列，需要计算同比"
```

### 2. 复杂查询拆分

复杂需求分步骤生成：
```
# 第一步：生成CTE结构
/sql-gen 先设计CTE结构：计算用户LTV需要哪些中间表

# 第二步：生成第一层CTE
/sql-gen 基于以上结构，生成第一层CTE：用户首次购买记录

# 第三步：生成完整查询
/sql-gen 合并所有CTE，生成完整LTV计算查询
```

### 3. 执行计划分析时机

- **开发阶段**：用 `/sql-explain` 分析预发布环境执行计划
- **上线前**：对比优化前后的执行计划差异
- **生产问题**：慢查询日志 → `/sql-explain` 诊断 → 优化 → 验证

---

## 故障排除

### Skill未触发
1. 检查skill文件是否在正确的skills目录
2. 确认Frontmatter格式正确（YAML语法）
3. 重启Claude Code

### SQL生成不符合预期
1. 提供更详细的表结构信息
2. 明确指定数据库类型和版本
3. 分步骤生成复杂查询

### 执行计划分析不完整
1. 使用 `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` 获取完整信息
2. 确保提供的是实际执行计划（ANALYZE），而非预估计划
3. 大数据量时执行计划可能不同，提供生产环境的计划

---

## 示例场景

### 场景1：从零构建报表系统

```bash
# 1. 生成核心查询
/sql-gen 统计近30天每日销售额、订单量、客单价，使用MySQL

# 2. 审查优化
/sql-review [上一步生成的SQL]

# 3. 执行计划验证（在测试库执行后）
/sql-explain
[粘贴EXPLAIN结果]

# 4. 根据分析结果优化索引
/sql-gen 为以上查询设计最优索引
```

### 场景2：慢查询优化

```bash
# 1. 分析现有慢查询
/sql-explain
[粘贴生产环境慢查询的执行计划]

# 2. 根据分析结果生成优化方案
/sql-gen 优化以下查询，解决全表扫描问题：[原SQL]

# 3. 对比审查
/sql-review 对比分析：[原SQL] vs [优化后的SQL]
```

### 场景3：团队规范落地

```bash
# 1. 审查团队现有SQL
/sql-review src/queries/*.sql

# 2. 生成规范文档
/sql-assistant 基于审查结果，生成团队SQL规范文档

# 3. 批量规范化
/sql-assistant 批量规范化目录下所有SQL文件，统一命名和格式
```

---

## 路线图

### v1.0.0 (当前)
- ✅ SQL生成器 (sql-generator)
- ✅ SQL审查器 (sql-reviewer)
- ✅ 执行计划分析器 (sql-explain)
- ✅ 多数据库支持 (PostgreSQL/MySQL/SQL Server/Oracle)

### v1.1.0 (计划)
- 🔄 Schema自动发现（从数据库读取表结构）
- 🔄 查询性能基线（记录历史执行计划对比）
- 🔄 SQL格式化工具（统一代码风格）

### v2.0.0 (计划)
- 📝 自然语言查询优化建议
- 📝 自动索引推荐引擎
- 📝 与dbt/Metabase等工具集成

---

**提示**：本Skill与《AI编程与数据开发工程师融合实战手册》§04 AI辅助SQL开发实战章节配套使用。
