---
name: etl-assistant
description: |
  ETL Pipeline开发助手 - 端到端ETL开发工作流。包含代码生成、代码审查、数据测试三大核心功能。
  当用户需要开发数据同步Pipeline、构建ETL作业、设计数据集成流程、生成Airflow DAG时触发。
  触发词：ETL开发、Pipeline、数据同步、数据集成、增量同步、Airflow、数据管道、数据迁移。
---

# ETL Pipeline开发助手

端到端ETL Pipeline开发工作流：代码生成 → 代码审查 → 数据测试。从需求到可部署ETL Pipeline的完整解决方案。

## 架构概览

```
输入 → [阶段1: 代码生成] → [阶段2: 代码审查] → [阶段3: 数据测试] → 输出
            │                    │                    │
            ▼                    ▼                    ▼
       Agent:通用          Agent:探索           Agent:通用
```

| 阶段 | 命令 | Agent | 功能 |
|------|------|-------|------|
| 1 | /etl-template | general-purpose | 生成ETL代码模板（Python/Airflow/dbt） |
| 2 | /pipeline-review | Explore | ETL代码审查（性能/安全/可靠性） |
| 3 | /data-test | general-purpose | 生成测试代码（单元/集成/质量） |

**输出标准**: 生成 `etl_package.yaml` 便于下游 Skill 消费

## 参考资料导航

| 何时读取 | 文件 | 内容 | 场景 |
|---------|------|------|------|
| 设计Pipeline时 | [references/etl-standards.md](references/etl-standards.md) | 架构模式、命名规范、代码模板 | 需要遵循团队规范 |
| 选择技术栈时 | [references/etl-standards.md](references/etl-standards.md) | 技术选型指南、调度工具对比 | 不确定用Airflow还是其他 |
| 查看示例时 | [examples/](examples/) 目录 | 典型场景的完整示例 | 学习使用方法 |
| 配置监控时 | [references/etl-standards.md](references/etl-standards.md) | 监控埋点、日志规范 | 需要添加监控告警 |

## 项目初始化（推荐）

为团队建立标准化ETL开发工作流：

```bash
# 创建ETL开发项目骨架
bash .claude/skills/etl-assistant/scripts/init-project.sh ./etl-project "用户数据同步Pipeline"
```

自动生成目录结构：
```
etl-project/
├── PROJECT.md          # 项目中枢（Pipeline清单+进度+规范）
├── standards.md        # 团队ETL规范
├── pipelines/          # Pipeline代码
│   ├── generated/      # 生成的代码
│   ├── reviewed/       # 已审查的代码
│   └── production/     # 生产代码
├── dags/               # Airflow DAG
├── tests/              # 测试代码
│   ├── unit/           # 单元测试
│   ├── integration/    # 集成测试
│   └── data_quality/   # 数据质量测试
├── docs/               # 文档
└── scripts/            # 部署脚本
```

## 使用方法

### 方式1：分阶段使用（推荐）

```bash
# 阶段1：生成ETL代码（general-purpose Agent）
/etl-template 生成Python ETL脚本，源系统MySQL用户表，目标PostgreSQL数仓，增量同步

# 阶段2：审查ETL代码（Explore Agent）
/pipeline-review [ETL代码]

# 阶段3：生成测试代码（general-purpose Agent）
/data-test [ETL代码]
```

### 方式2：端到端工作流

```bash
# 启动完整ETL开发工作流
/etl-assistant 端到端开发：订单数据从MySQL同步到Snowflake，每日调度
```

## 核心功能

### 1. ETL代码生成器 (`/etl-template`)

**Agent**: general-purpose
**权限**: Read, Grep, Glob, Edit, Write, Bash

| 特性 | 说明 |
|------|------|
| **输入** | ETL需求描述（源/目标/转换逻辑） |
| **输出** | 完整可运行的代码模板 |
| **支持类型** | Python脚本、Airflow DAG、dbt模型 |
| **抽取策略** | 全量、增量（时间戳/CDC）、增量+全量混合 |
| **加载策略** | UPSERT、Append、Replace |

**示例**：
```bash
/etl-template 生成Airflow DAG，每日凌晨2点从MySQL抽取订单数据，
经过清洗转换后加载到BigQuery，使用增量同步策略，保留历史变更
```

### 2. Pipeline代码审查器 (`/pipeline-review`)

**Agent**: Explore
**权限**: Read, Grep, Glob

| 审查维度 | 检查内容 | 输出 |
|----------|----------|------|
| 🔴 性能问题 | 内存泄漏、重复查询、全表扫描 | 问题位置、风险说明、修复代码 |
| 🟡 可靠性 | 错误处理、幂等性、重试机制 | 风险评估、改进建议 |
| 🟠 数据质量 | 数据验证、类型转换、NULL处理 | 潜在风险点 |
| 🔴 安全性 | SQL注入、硬编码密码 | 安全漏洞警告 |
| 🟢 可维护性 | 日志、注释、代码结构 | 可读性评分 |

**示例**：
```bash
/pipeline-review [粘贴Python ETL脚本]
```

### 3. 数据测试生成器 (`/data-test`)

**Agent**: general-purpose
**权限**: Read, Grep, Glob, Edit, Write, Bash

| 测试类型 | 说明 | 框架 |
|----------|------|------|
| **单元测试** | 转换函数、业务逻辑 | pytest |
| **集成测试** | 数据源连接、Pipeline端到端 | pytest + mock |
| **数据质量测试** | 完整性、准确性、一致性 | Great Expectations |
| **DAG测试** | Airflow DAG结构、依赖关系 | Airflow测试框架 |

**示例**：
```bash
/data-test 为订单ETL Pipeline生成完整测试套件，
包含单元测试、数据质量测试和Airflow DAG测试
```

---

## 标准输出格式

每个ETL开发任务输出标准化的 `etl_package.yaml`：

```yaml
etl_package:
  version: "1.0"
  metadata:
    generated_by: "etl-assistant"
    generated_at: "2024-01-15T10:00:00Z"
    source_system: "MySQL"
    target_system: "Snowflake"
    pipeline_name: "order_sync"
    
  pipeline:
    type: "Python|Airflow DAG|dbt"
    extract:
      strategy: "incremental|full|cdc"
      source_tables: ["orders", "order_items"]
      watermark_column: "updated_at"
    transform:
      logic: ["join", "aggregate", "clean"]
      dependencies: ["dim_user", "dim_product"]
    load:
      target_tables: ["fct_orders"]
      mode: "upsert|append|replace"
      schedule: "0 2 * * *"
      
  code_artifacts:
    main_script: "pipelines/order_sync.py"
    dag_file: "dags/order_sync_dag.py"
    test_files: ["tests/test_order_sync.py"]
    
  quality_gates:
    row_count_check: true
    schema_check: true
    data_freshness_check: true
```

## 与下游 Skill 的联动

ETL Pipeline 开发完成后，自动触发下游 Skill：

```bash
## ETL 输出后的下一步

# 步骤1: 数据质量检查（推荐）
/dq-assistant 基于以下 ETL 配置建立质量监控：
- 源表: orders, order_items
- 目标表: fct_orders
- 检查项: 行数对比、schema一致性、数据新鲜度

# 步骤2: 数据测试（必需）
/test-engineer 为以下 Pipeline 生成端到端测试：
- Pipeline: order_sync
- 测试类型: 集成测试、回归测试
- 验证点: 数据完整性、业务逻辑正确性
```

## 配合使用流程

```
需求理解 (10分钟)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段1: ETL代码生成 (/etl-template)                          │
│  ├─ 输入：ETL需求描述                                         │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：Python/Airflow/dbt代码模板                          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段2: 代码审查 (/pipeline-review)                          │
│  ├─ 输入：ETL代码                                            │
│  ├─ 处理：Explore Agent (只读分析)                           │
│  └─ 输出：审查报告 + 优化后代码                               │
└─────────────────────────────────────────────────────────────┘
    │
    ├─ 🔴 严重问题 ──► 返回修改 ──► 重新审查
    │
    ▼ (审查通过)
┌─────────────────────────────────────────────────────────────┐
│  阶段3: 数据测试 (/data-test)                                │
│  ├─ 输入：ETL代码                                            │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：完整测试套件                                        │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
部署上线
```

## 多Agent协作

复杂ETL开发可拆分为多Agent并行：

```
协调Agent (主会话)
    │
    ├─► etl-template Agent #1 ──► 生成抽取代码
    ├─► etl-template Agent #2 ──► 生成转换代码
    ├─► etl-template Agent #3 ──► 生成加载代码
    │
    ▼ (收集结果)
    │
    ├─► pipeline-review Agent #1 ──► 审查抽取逻辑
    ├─► pipeline-review Agent #2 ──► 审查转换逻辑
    ├─► pipeline-review Agent #3 ──► 审查加载逻辑
    │
    ▼ (汇总审查意见)
    │
    └─► data-test Agent ──► 生成测试代码
```

## 技术栈支持

### 数据源
- **关系型**: MySQL, PostgreSQL, SQL Server, Oracle
- **大数据**: Hive, Impala, Presto
- **云数仓**: BigQuery, Snowflake, Redshift, Databricks
- **文件**: CSV, JSON, Parquet, Avro
- **API**: REST, GraphQL
- **消息队列**: Kafka, RabbitMQ

### 转换引擎
- **Python**: pandas, polars, pyarrow
- **大数据**: Spark, Flink
- **SQL**: dbt, 存储过程

### 调度工具
- **Apache Airflow**
- **Prefect**
- **Dagster**
- ** cron / systemd**

## 最佳实践

### 提示词工程

**高效需求描述公式**：
```
[源系统] + [目标系统] + [同步实体] + [抽取策略] + [调度频率] + [特殊需求]

示例：
"从MySQL订单表增量同步到BigQuery，使用updated_at时间戳识别变更，
每日凌晨2点执行，需要处理删除标记的软删除记录"
```

### Pipeline设计原则

1. **幂等性**: 任何Pipeline都可以安全重跑
2. **断点续传**: 支持从失败点恢复
3. **数据验证**: 每个阶段都有输入/输出验证
4. **监控埋点**: 关键指标输出到监控系统
5. **错误隔离**: 单条记录失败不影响整体

## 故障排除

### Skill未触发
1. 检查skill文件路径：`~/.claude/skills/` 或项目 `.claude/skills/`
2. 确认Frontmatter格式正确（YAML语法，---包裹）
3. 重启Claude Code

### 代码生成不符合预期
1. 提供更详细的表结构信息
2. 明确指定技术栈版本
3. 分步骤生成复杂Pipeline

### 审查结果不完整
1. 确保提供完整的代码文件
2. 说明特定的审查关注点
3. 分阶段审查大型Pipeline

## 示例场景

详见 `examples/` 目录：

| 示例 | 场景 | 流程 |
|------|------|------|
| [example-ecommerce-etl.md](examples/example-ecommerce-etl.md) | 电商订单数据同步 | 生成 → 审查 → 测试 |

## 完整数据开发工作流

```
┌─────────────────────────────────────────────────────────────────────┐
│                   完整数据开发工作流                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   数据采集/ETL                                                      │
│       │                                                             │
│       ▼                                                             │
│   ┌────────────────────────────────────────────────────┐           │
│   │  ETL Pipeline开发助手                               │           │
│   │  - 生成ETL Pipeline代码                            │           │
│   │  - 审查Pipeline质量                                │           │
│   │  - 生成数据测试                                    │           │
│   └────────────────────┬───────────────────────────────┘           │
│                        │                                            │
│                        ▼                                            │
│   数据存储                                            │           │
│       │                                              │           │
│       ▼                                              ▼           │
│   ┌────────────────────────────────────────────────────┐           │
│   │  SQL智能开发助手                                    │           │
│   │  - 生成ETL/ELT SQL                                 │           │
│   │  - 审查数据清洗逻辑                                │           │
│   │  - 优化Pipeline性能                                │           │
│   └────────────────────┬───────────────────────────────┘           │
│                        │                                            │
│                        ▼                                            │
│   数据质量                                            │           │
│       │                                              │           │
│       ▼                                              ▼           │
│   ┌────────────────────────────────────────────────────┐           │
│   │  数据质量检查助手                                   │           │
│   │  - 建立质量监控规则                                │           │
│   │  - 定期检查数据质量                                │           │
│   │  - 生成数据字典文档                                │           │
│   └────────────────────┬───────────────────────────────┘           │
│                        │                                            │
│                        ▼                                            │
│   数据建模                                            │           │
│       │                                              │           │
│       ▼                                              ▼           │
│   ┌────────────────────────────────────────────────────┐           │
│   │  数据建模助手                                       │           │
│   │  - 维度模型设计                                    │           │
│   │  - dbt模型开发                                     │           │
│   │  - 数据血缘分析                                    │           │
│   └────────────────────────────────────────────────────┘           │
│                                                                     │
│   数据服务（BI/报表/机器学习）                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 四大模块对比

| 特性 | SQL智能开发助手 | 数据质量检查助手 | 数据建模助手 | ETL Pipeline开发助手 |
|------|----------------|-----------------|-------------|---------------------|
| **核心目标** | 高效开发高质量SQL | 保障数据质量 | 建立数据模型 | 开发ETL Pipeline |
| **工作流程** | 生成→审查→优化 | 规则→检查→文档 | 设计→开发→血缘 | 生成→审查→测试 |
| **主要Agent** | general + Explore | general + Explore | general + Explore | general + Explore |
| **输出物** | SQL代码 | 质量报告 | dbt模型 | ETL代码+测试 |
| **适用场景** | 查询开发 | 数据监控 | 数仓建设 | Pipeline开发 |

---

**提示**：本Skill套件与《AI编程与数据开发工程师融合实战手册》配套使用。
- SQL智能开发助手 → §04 AI辅助SQL开发实战
- 数据质量检查助手 → §06 数据Pipeline与仓库建模
- 数据建模助手 → §06 数据Pipeline与仓库建模
- ETL Pipeline开发助手 → §05 数据Pipeline自动化
