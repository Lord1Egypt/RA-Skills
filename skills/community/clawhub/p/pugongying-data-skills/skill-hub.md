---
name: skill-hub
description: |
  数据开发Skill联动中枢 - 协调SQL智能开发助手、数据质量检查助手、
  数据建模助手、ETL Pipeline开发助手之间的协作。
  触发词：端到端开发、skill联动、完整工作流、自动化开发、data-workflow。
argument: { description: "联动需求描述（如：端到端建设电商数仓）", required: true }
agent: general-purpose
allowed-tools: [Agent, Read, Grep, Glob, Edit, Write, Bash]
---

# 数据开发Skill Hub

## 功能

协调多个数据开发Skill，实现端到端自动化开发工作流。

> 详细联动配置见: [skill-connections.yaml](skill-connections.yaml)

## 支持的联动模式

| 模式 | 说明 | 示例 |
|------|------|------|
| 简单串联 | A → B | SQL生成 → ETL生成 |
| 并行分流 | A → [B, C] | 模型设计 → 并行生成多个SQL |
| 完整工作流 | 多阶段流程 | 建模→SQL→ETL→质量→测试 |

## 联动矩阵

```
                    需求分析    架构设计    SQL智能    数据质量    数据建模    ETL Pipeline  测试工程
                    助手        助手       开发助手    检查助手     助手        开发助手      师
需求分析助手           -        ✓(需求→架构) ✓(需求→SQL) ✓(需求→规则) ✓(需求→模型) ✓(需求→ETL)  ✓(需求→测试)
架构设计助手       ✓(架构→需求)     -       ✓(架构→SQL) ✓(架构→规则) ✓(架构→模型) ✓(架构→ETL)  ✓(架构→测试)
SQL智能开发助手      ✓(SQL→需求)  ✓(SQL→架构)   -       ✓(SQL审查)  ✓(DDL生成)  ✓(SQL→ETL)   ✓(SQL→测试)
数据质量检查助手      ✓(质量→需求)  ✓(质量→架构) ✓(规则)      -       ✓(模型质量) ✓(ETL质量)   ✓(质量→测试)
数据建模助手        ✓(模型→需求) ✓(模型→架构) ✓(Schema)  ✓(质量)      -        ✓(模型→ETL)  ✓(模型→测试)
ETL Pipeline       ✓(ETL→需求)  ✓(ETL→架构) ✓(ETL SQL)  ✓(测试)    ✓(血缘)       -        ✓(ETL→测试)
开发助手
test-engineer    ✓(测试→需求)  ✓(测试→架构) ✓(测试→SQL)  ✓(测试→质量) ✓(测试→模型)  ✓(测试→ETL)      -
```

## 工作流模板

### 模板1: 端到端数仓建设

```yaml
workflow: end_to_end_warehouse
phases:
  - name: 需求分析
    skill: requirement-analyst
    input: 原始业务需求
    output: 结构化需求包

  - name: 架构设计
    skill: architecture-designer
    input: 需求包
    output: 架构规格

  - name: 数据建模
    skill: model-design
    input: 架构分层规格
    output: 维度模型设计

  - name: SQL开发
    skill: sql-gen
    input: 模型Schema
    output: DDL + ETL SQL

  - name: ETL开发
    skill: etl-template
    input: 拓扑设计 + SQL
    output: Pipeline代码

  - name: 质量配置
    skill: dq-rule-gen
    input: 目标表Schema
    output: 质量规则

  - name: 数据质量
    skill: dq-assistant
    input: 目标表Schema
    output: 质量规则

  - name: 测试验证
    skill: test-engineer
    input: 数据质量包 + Pipeline代码
    output: 测试套件
```

### 模板2: SQL优化→ETL生成

```yaml
workflow: sql_to_etl
phases:
  - name: SQL生成
    skill: sql-gen
    input: 业务需求
    output: SQL初稿

  - name: SQL审查
    skill: sql-review
    input: SQL初稿
    output: 优化后SQL

  - name: ETL生成
    skill: etl-template
    input: 优化SQL
    output: Pipeline代码
```

## 当前需求

$ARGUMENTS

---

**执行策略**：
1. 解析需求，识别需要哪些Skill
2. 确定执行顺序和依赖关系
3. 依次调用各Skill，传递上下文
4. 整合输出，形成完整项目包

**示例**：
```
需求: "端到端建设电商订单数仓"
识别: 需要 modeling → sql-gen → etl-template → dq-rule-gen
执行: 按顺序调用，传递Schema和上下文
输出: 模型+SQL+ETL+质量规则完整包
```

## 详细联动指南

### 联动1: 需求分析 → 架构设计

当用户从业务需求开始完整数据平台建设时：

```bash
# 用户输入
/requirement-analyst 分析电商销售分析需求 → /architecture-designer 基于需求设计数据平台架构

# 系统自动
1. requirement-analyst 解析需求，输出requirement_package.yaml
   - 提取业务实体、指标、维度
   - 识别数据量和实时性要求
2. 将requirement_package传递给architecture-designer
3. architecture-designer 根据需求选择合适的架构模式
   - Lambda架构（实时+批量）
   - 湖仓一体（Iceberg/S3 + Snowflake）
4. 输出architecture_package.yaml，包含分层设计和拓扑规划
```

**上下文传递**:
```yaml
# requirement_package.yaml → architecture_package.yaml
input:
  functional.entities → layer_architecture.dwd.tables
  functional.metrics → layer_architecture.dws.metrics
  non_functional.freshness → architecture.pattern(实时性判断)
  non_functional.retention → lifecycle_policies
```

---

### 联动2: 架构设计 → 数据建模

当架构确定后，基于分层设计进行维度建模：

```bash
# 用户输入
/architecture-designer 完成分层设计 → /model-design 基于DWS层设计维度模型

# 系统自动
1. architecture-designer 输出分层架构
   - DWD层：清洗后的明细表
   - DWS层：轻度汇总主题表
2. 提取DWS层主题域传递给model-designer
3. model-designer 设计星型/雪花模型
   - 事实表：与DWS层粒度一致
   - 维度表：支持SCD策略
4. 输出dbt模型代码
```

**上下文传递**:
```yaml
# architecture_package.yaml → model_spec.yaml
input:
  layers.dws.tables → fact_tables (事实表设计)
  layers.dwd.tables.source → dimension_tables (维度属性)
  tech_stack.storage.data_warehouse → dbt适配器选择
```

---

### 联动3: 架构设计 → ETL开发

当架构确定后，基于拓扑设计生成Pipeline：

```bash
# 用户输入
/architecture-designer 完成拓扑设计 → /etl-template 基于拓扑生成Pipeline代码

# 系统自动
1. architecture-designer 输出Pipeline拓扑
   - DAG分组：ingestion/processing/serving
   - 依赖关系：任务间依赖
   - 调度策略：时间/事件驱动
2. 提取拓扑结构传递给etl-template
3. etl-template 生成对应代码
   - 批量：Airflow DAG + Spark/Pandas
   - 流式：Flink作业（如需要）
4. 输出可部署的Pipeline代码
```

**上下文传递**:
```yaml
# architecture_package.yaml → etl_spec.yaml
input:
  topology.dag_groups → airflow DAG结构
  topology.dependencies → task依赖关系
  topology.scheduling → DAG调度配置
  tech_stack → 执行引擎选择(Spark/Flink/Python)
```

---

### 联动5: SQL生成 → ETL模板

当用户需要基于SQL逻辑生成Pipeline时：

```bash
# 用户输入
/sql-gen 生成订单表抽取SQL → /etl-template 使用上述SQL生成Pipeline

# 系统自动
1. sql-gen 分析需求，生成优化SQL
2. 提取SQL中的表名、字段、条件
3. 将提取的Schema传递给etl-template
4. etl-template 生成匹配该SQL的Pipeline代码
```

### 联动6: 数据建模 → SQL生成

当用户从模型设计到DDL生成：

```bash
# 用户输入
/model-design 设计电商维度模型 → /sql-gen 生成建表DDL

# 系统自动
1. model-design 输出维度模型设计
2. 提取模型中的表结构、字段类型、关系
3. 传递给sql-gen生成CREATE TABLE语句
4. 可继续传递给etl-template生成加载逻辑
```

### 联动7: ETL模板 → 数据质量

当用户为Pipeline添加质量监控：

```bash
# 用户输入
/etl-template 生成订单同步Pipeline → /dq-rule-gen 为目标表生成质量规则

# 系统自动
1. etl-template 生成ETL代码
2. 提取目标表Schema和字段信息
3. 传递给dq-rule-gen生成对应质量规则
4. 可继续生成Great Expectations测试代码
```

### 联动8: 数据质量 → 测试工程

当质量规则确定后，生成对应的测试用例：

```bash
# 用户输入
/dq-rule-gen 生成质量规则 → /unit-test 基于规则生成单元测试

# 系统自动
1. dq-rule-gen 生成质量规则配置
2. 提取规则类型和字段信息
3. 传递给test-engineer生成pytest测试用例
4. 生成schema验证、数据质量断言、边界测试
```

### 联动9: ETL模板 → 测试工程

当Pipeline开发完成后，进行集成测试：

```bash
# 用户输入
/etl-template 生成Pipeline → /integration-test 验证数据流一致性

# 系统自动
1. etl-template 生成Pipeline代码
2. 提取Pipeline拓扑和转换逻辑
3. 传递给test-engineer生成集成测试
4. 生成跨层级对账测试、血缘一致性验证
```

### 联动10: SQL开发 → 测试工程

当SQL开发完成后，进行性能和正确性测试：

```bash
# 用户输入
/sql-gen 生成分析查询 → /performance-test 验证查询性能

# 系统自动
1. sql-gen 生成SQL查询
2. 提取查询复杂度和表信息
3. 传递给test-engineer生成性能测试
4. 生成P50/P95/P99基准测试、并发压力测试
```

### 联动8: 端到端工作流

完整的数据开发流程（6阶段）：

```bash
# 用户输入
/skill-hub 端到端建设电商数仓：包含用户、订单、商品数据，支持销售分析

# 系统自动执行完整工作流
Phase 0: 需求分析 (requirement-analyst)
  - /requirement-parser: 解析业务需求，提取实体、指标、维度
  - /requirement-clarify: 识别需求缺口，确认业务规则
  - /requirement-transform: 生成技术规格
  - 输出: requirement_package.yaml

Phase 1: 架构设计 (architecture-designer)
  - /arch-select: 选择Lambda+湖仓一体架构
  - /layer-design: 设计ODS/DWD/DWS/ADS四层分层
  - /tech-planning: 选择Snowflake+Spark技术栈
  - /topology-design: 设计Pipeline拓扑
  - 输出: architecture_package.yaml

Phase 2: 数据建模 (modeling-assistant)
  - /model-design: 基于DWS层设计星型模型
  - /dbt-model: 生成dbt模型代码
  - /lineage-doc: 生成血缘关系图

Phase 3: SQL开发 (sql-assistant)
  - /sql-gen: 生成各表抽取SQL
  - /sql-review: 审查SQL性能
  - 输出优化后的ETL SQL

Phase 4: ETL Pipeline (etl-assistant)
  - /etl-template: 基于拓扑设计生成Pipeline
  - /pipeline-review: 审查代码质量
  - /data-test: 生成测试套件

Phase 5: 数据质量 (dq-assistant)
  - /dq-rule-gen: 生成质量规则
  - /schema-doc: 生成数据字典

Phase 6: 测试验证 (test-engineer)
  - /unit-test: 生成单元测试
  - /integration-test: 生成集成测试
  - /performance-test: 生成性能测试

Phase 7: 项目整合
  - 输出完整项目结构
  - 包含所有代码和文档
  - 提供部署指南
```

## 上下文传递协议

### requirement-analyst 输出格式

```yaml
# 标准化需求包 (requirement_package.yaml)
requirement_package:
  version: "1.0"
  metadata:
    project_name: "项目名称"
    confirmed: true

  business:
    domain: "业务域"
    goal: "业务目标"

  functional:
    entities: [...]      # 传递给 model-design
    metrics: [...]       # 传递给 sql-gen
    dimensions: [...]    # 传递给 model-design

  specifications:
    model_spec: {...}    # 传递给 model-design
    etl_spec: {...}      # 传递给 etl-template
    dq_spec: {...}       # 传递给 dq-rule-gen

  downstream_tasks:      # skill-hub 执行顺序
    - skill: "architecture-designer"  # 新增
    - skill: "model-design"
    - skill: "sql-gen"
    - skill: "etl-template"
    - skill: "dq-rule-gen"
```

### architecture-designer 输出格式

```yaml
# 架构设计包 (architecture_package.yaml)
architecture_package:
  version: "1.0"
  source: "requirement-analyst"

  architecture:
    pattern: "Lambda + 湖仓一体"
    decisions: [...]  # ADR列表

  layers:
    ods: {...}        # 传递给 etl-template (抽取目标)
    dwd: {...}        # 传递给 model-design (模型输入)
    dws: {...}        # 传递给 model-design (事实表粒度)
    ads: {...}        # 传递给 dq-assistant (质量检查点)

  tech_stack:
    storage: {...}    # 传递给 sql-gen (方言选择)
    compute: {...}    # 传递给 etl-template (执行引擎)
    orchestration: {...}  # 传递给 etl-template (调度器)

  topology:
    dag_groups: [...]     # 传递给 etl-template (DAG结构)
    dependencies: [...]   # 传递给 etl-template (task依赖)
    scheduling: {...}     # 传递给 etl-template (调度配置)

  downstream_specs:
    model_spec:   # 传递给 modeling-assistant
      file: "specs/model_spec.yaml"
    etl_spec:     # 传递给 etl-assistant
      file: "specs/etl_spec.yaml"
    infra_spec:   # 传递给部署工具
      file: "specs/infra_spec.yaml"
    cost_estimate:
      file: "specs/cost_estimate.yaml"
```

### 端到端数据流

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        完整Skill联动数据流                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  原始需求                                                                │
│     │                                                                   │
│     ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  requirement-analyst                                            │   │
│  │  输出: requirement_package.yaml                                  │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │  [functional.entities]                       │
│                           │  [non_functional.freshness]                  │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  architecture-designer                                          │   │
│  │  输入: requirement_package.yaml                                  │   │
│  │  输出: architecture_package.yaml                                 │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │  [layers.dws]                                │
│                           │  [tech_stack.storage]                        │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  modeling-assistant                                             │   │
│  │  输入: architecture_package.layers.dws                           │   │
│  │  输出: dbt模型 + 血缘文档                                        │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │  [fact_tables, dimensions]                   │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  sql-assistant                                                  │   │
│  │  输入: 模型Schema + architecture.tech_stack                      │   │
│  │  输出: DDL + ETL SQL                                             │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │  [sql_snippet]                               │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  etl-assistant                                                  │   │
│  │  输入: SQL + architecture.topology + architecture.tech_stack    │   │
│  │  输出: Pipeline代码 + Airflow DAG                                │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │  [target_schema, columns]                    │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  dq-assistant                                                   │   │
│  │  输入: 目标表Schema + architecture.layers.ads                    │   │
│  │  输出: 质量规则 + 数据字典                                       │   │
│  └────────────────────────┬────────────────────────────────────────┘   │
│                           │  [quality_rules, table_schemas]              │
│                           ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  test-engineer                                                  │   │
│  │  输入: 质量规则 + 表Schema + Pipeline代码                         │   │
│  │  输出: 单元测试 + 集成测试 + 性能测试                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  完整项目交付 (模型 + SQL + ETL + 质量 + 测试 + 文档)                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 共享数据结构

```yaml
skill_context:
  # 由上游Skill生成，传递给下游Skill

  schema_info:          # 表结构信息
    table_name: "orders"
    columns:
      - name: "order_id"
        type: "BIGINT"
        constraints: ["PRIMARY KEY"]
      - name: "user_id"
        type: "BIGINT"
        constraints: ["NOT NULL"]

  sql_snippet: |        # SQL代码片段
    SELECT order_id, user_id, total_amount
    FROM orders
    WHERE updated_at > '{last_extract_time}'

  etl_config:           # ETL配置
    extract_strategy: "incremental"
    incremental_column: "updated_at"
    load_strategy: "upsert"
    unique_key: "order_id"

  quality_rules:        # 质量规则
    - column: "order_id"
      rule: "not_null"
      severity: "error"
    - column: "total_amount"
      rule: "positive"
      severity: "error"
```

### 参数映射规则

| 源Skill | 目标Skill | 映射参数 |
|---------|-----------|----------|
| requirement-analyst | architecture-designer | requirement_package→input |
| requirement-analyst | model-design | specifications.model_spec→input |
| requirement-analyst | sql-gen | functional.metrics→query_requirements |
| requirement-analyst | etl-template | specifications.etl_spec→pipeline_config |
| requirement-analyst | dq-rule-gen | specifications.dq_spec→quality_config |
| architecture-designer | model-design | layer_architecture.dws→model_input |
| architecture-designer | sql-gen | tech_stack.storage→sql_dialect |
| architecture-designer | etl-template | topology→pipeline_topology |
| architecture-designer | etl-template | tech_stack→infrastructure |
| sql-gen | etl-template | sql→extract_sql, table→source_table |
| model-design | sql-gen | fact_tables→tables, dimensions→joins |
| etl-template | dq-rule-gen | target_table→table_name, columns→columns |
| model-design | etl-template | schema→target_schema, grain→etl_config |
| dq-rule-gen | test-engineer | quality_rules→test_assertions |
| etl-template | test-engineer | pipeline→integration_test_scenarios |
| sql-gen | test-engineer | sql_query→performance_test_target |
| model-design | test-engineer | schema→unit_test_fixtures |

## 使用示例

### 示例1: 简单联动

```bash
用户: 帮我生成订单数据同步Pipeline

系统:
┌─────────────────────────────────────────────────────────┐
│ Step 1: SQL智能开发助手                                  │
│ /sql-gen 生成订单表抽取SQL                               │
│ 输出: 优化的抽取SQL                                      │
├─────────────────────────────────────────────────────────┤
│ [自动传递上下文]                                         │
│ SQL → 表结构提取 → Schema信息                            │
├─────────────────────────────────────────────────────────┤
│ Step 2: ETL Pipeline开发助手                             │
│ /etl-template 基于Schema生成Pipeline                     │
│ 输出: Python ETL + Airflow DAG                          │
└─────────────────────────────────────────────────────────┘

最终输出: SQL + ETL代码包
```

### 示例2: 端到端联动（完整6阶段）

```bash
用户: 端到端建设电商销售分析数仓

系统执行完整6阶段工作流:

Phase 0 (需求分析助手):
  - 解析业务需求
  - 提取实体(订单/用户/商品)、指标(GMV/订单量/客单价)、维度(日期/地区/类目)
  - 确认业务规则(用户等级SCD Type 2)
  - 输出: requirement_package.yaml

Phase 1 (架构设计助手):
  - 选择Lambda+湖仓一体架构
  - 设计ODS/DWD/DWS/ADS四层分层
  - 规划技术栈(S3 Iceberg + Snowflake + Spark)
  - 设计Pipeline拓扑
  - 输出: architecture_package.yaml + ADR文档

Phase 2 (建模助手):
  - 基于DWS层设计星型模型
  - 输出: dim_users(SCD2), dim_products(SCD2), fct_order_items
  - 生成dbt模型代码
  - 生成血缘关系图

Phase 3 (SQL助手):
  - 生成维度表DDL
  - 生成事实表抽取SQL(增量/CDC)
  - 审查SQL性能
  - 输出: SQL脚本集合

Phase 4 (ETL助手):
  - 基于拓扑设计生成5个Pipeline
  - 生成Airflow DAG
  - 生成测试套件
  - 输出: ETL代码 + DAG文件

Phase 5 (质量助手):
  - 为所有表生成质量规则
  - 配置Great Expectations测试
  - 生成数据字典
  - 输出: DQ配置 + 文档

Phase 6 (测试工程师):
  - 生成单元测试 (schema/数据质量/业务逻辑)
  - 生成集成测试 (Pipeline/对账/SCD2)
  - 生成性能测试 (查询基准/ETL时长)
  - 输出: pytest测试套件 + 性能报告

Phase 7 (项目整合):
  - 整合所有代码和配置
  - 生成PROJECT.md项目中枢
  - 输出README和部署指南
  - 提供成本估算报告
```

### 示例3: 交付检查清单

```bash
用户: 生成交付检查清单

系统检查项目完整性:

┌─────────────────────────────────────────────────────────┐
│ Step 1: 检查项目结构                                    │
│ ✓ requirements/ 需求文档                                │
│ ✓ architecture/ 架构设计                                │
│ ✓ models/ 数据模型                                      │
│ ✓ sql/ SQL开发                                          │
│ ✓ etl/ ETL开发                                          │
│ ✓ dq/ 数据质量                                          │
│ ✓ docs/ 项目文档                                        │
│ ✓ outputs/ 标准包文件                                   │
├─────────────────────────────────────────────────────────┤
│ Step 2: 检查标准包文件                                  │
│ ✓ requirement_package.yaml                              │
│ ✓ architecture_package.yaml                             │
│ ✓ modeling_package.yaml                                 │
│ ✓ sql_package.yaml                                      │
│ ✓ etl_package.yaml                                      │
│ ✓ dq_package.yaml                                       │
├─────────────────────────────────────────────────────────┤
│ Step 3: 检查文档完整性                                  │
│ ✓ PROJECT.md 项目中枢                                   │
│ ✓ docs/deployment-guide.md 部署指南                     │
│ ✓ docs/user-manual.md 用户手册                          │
├─────────────────────────────────────────────────────────┤
│ Step 4: 生成交付报告                                    │
│ 输出: delivery-report.md                                │
│ - 检查项总数: 15                                        │
│ - 通过: 15                                              │
│ - 失败: 0                                               │
│ - 状态: ✅ 可以交付                                      │
└─────────────────────────────────────────────────────────┘
```

## 完整数据开发工作流

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        完整数据开发工作流                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 0: 需求分析 (requirement-parser + clarify + transform)   │   │
│  │  ├─ 需求解析                                                     │   │
│  │  ├─ 需求澄清                                                     │   │
│  │  └─ 需求转化                                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │  [requirement_package.yaml]                                        │
│     ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 1: 架构设计 (arch-select + layer-design + tech-planning) │   │
│  │  ├─ 架构选型                                                     │   │
│  │  ├─ 分层设计                                                     │   │
│  │  ├─ 技术规划                                                     │   │
│  │  └─ 拓扑设计                                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │  [architecture_package.yaml]                                       │
│     ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 2: 数据建模 (model-design + dbt-model + lineage-doc)     │   │
│  │  ├─ 维度模型设计                                                 │   │
│  │  ├─ dbt模型开发                                                  │   │
│  │  └─ 血缘分析                                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │                                                                   │
│     ▼ [传递Schema]                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 3: SQL开发 (sql-gen + sql-review + sql-explain)          │   │
│  │  ├─ SQL生成                                                      │   │
│  │  ├─ SQL审查                                                      │   │
│  │  └─ 执行计划分析                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │                                                                   │
│     ▼ [传递SQL]                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 4: ETL Pipeline (etl-template + pipeline-review + data-test)│  │
│  │  ├─ Pipeline代码生成                                             │   │
│  │  ├─ 代码审查                                                     │   │
│  │  └─ 测试代码生成                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │                                                                   │
│     ▼ [传递目标Schema]                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 5: 数据质量 (dq-rule-gen + dq-check + schema-doc)        │   │
│  │  ├─ 质量规则生成                                                 │   │
│  │  ├─ 质量检查                                                     │   │
│  │  └─ 数据字典生成                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │                                                                   │
│     ▼ [传递质量规则和表Schema]                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 6: 测试验证 (unit-test + integration-test + performance-test)│  │
│  │  ├─ 单元测试生成                                                 │   │
│  │  ├─ 集成测试生成                                                 │   │
│  │  └─ 性能测试生成                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│     │                                                                   │
│     ▼                                                                   │
│  完整项目输出 (模型+SQL+ETL+质量+测试+文档)                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```
