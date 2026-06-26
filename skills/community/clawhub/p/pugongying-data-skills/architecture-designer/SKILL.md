---
name: architecture-designer
description: |
  数据架构设计助手 - 端到端数据架构设计工作流。基于业务需求设计整体数据系统架构，
  包含数据架构选型、分层设计、技术栈规划、Pipeline拓扑设计四大核心功能。
  当用户需要设计数据平台架构、选择技术栈、规划数据分层时触发。
  触发词：架构设计、技术选型、数据分层、平台架构、系统架构、架构规划。
---

# 数据架构设计助手

从业务需求到可落地技术架构的完整设计工作流。四个阶段：架构选型 → 分层设计 → 技术规划 → 拓扑设计。

## 架构概览

```
输入 → [阶段1: 架构选型] → [阶段2: 分层设计] → [阶段3: 技术规划] → [阶段4: 拓扑设计] → 输出
            │                      │                      │                      │
            ▼                      ▼                      ▼                      ▼
       Agent:通用              Agent:通用              Agent:探索            Agent:通用
```

| 阶段 | 命令 | Agent | 功能 |
|------|------|-------|------|
| 1 | /arch-select | general-purpose | 选择整体数据架构 |
| 2 | /layer-design | general-purpose | 设计ODS/DWD/DWS/ADS分层 |
| 3 | /tech-planning | Explore | 选择技术组件与成本估算 |
| 4 | /topology-design | general-purpose | 设计Pipeline依赖拓扑 |

**输入**: requirement_package.yaml (来自需求分析)  
**输出**: architecture_package.yaml (驱动下游建模与开发)

## 参考资料导航

| 何时读取 | 文件 | 内容 | 场景 |
|---------|------|------|------|
| 架构选型时 | [references/architecture-standards.md](references/architecture-standards.md) | 架构模式对比 | 不确定用Lambda还是Kappa架构 |
| 分层设计时 | [references/architecture-standards.md](references/architecture-standards.md) | ODS/DWD/DWS/ADS规范 | 需要设计数据分层 |
| 技术选型时 | [references/architecture-standards.md](references/architecture-standards.md) | 技术选型矩阵、成本模型 | 选择Snowflake vs BigQuery |
| 成本估算时 | [references/architecture-standards.md](references/architecture-standards.md) | 成本评估模型 | 需要向管理层汇报预算 |
| 查看示例时 | [examples/](examples/) 目录 | 电商/实时分析等场景 | 参考完整设计案例 |

---

## 示例快速索引

| 需求场景 | 推荐命令 | 上游输入 | 详情位置 |
|----------|----------|----------|----------|
| 新建数据平台 | `/arch-select [需求]` | requirement_package.yaml | [功能1](#功能1架构选型助手-arch-select) |
| 设计数仓分层 | `/layer-design [实体列表]` | architecture_decision | [功能2](#功能2分层设计助手-layer-design) |
| 选择技术栈 | `/tech-planning [架构]` | layer_architecture | [功能3](#功能3技术规划助手-tech-planning) |
| 设计Pipeline | `/topology-design [数据流]` | tech_stack_spec | [功能4](#功能4拓扑设计助手-topology-design) |
| 端到端完整设计 | `/architecture-designer [需求]` | requirement_package.yaml | [方式2](#方式2端到端工作流) |
| 驱动数据建模 | 调用 `/modeling-assistant` | architecture_package.yaml | [下游联动](#与下游-skill-的联动) |

## 上游输入

本 Skill 消费来自需求分析的标准包：

| 来源 Skill | 输入文件 | 关键字段 | 使用方式 |
|-----------|----------|----------|----------|
| requirement-analyst | requirement_package.yaml | business.domain | 确定数据平台范围 |
| requirement-analyst | requirement_package.yaml | functional.entities | 设计ODS/DWD表 |
| requirement-analyst | requirement_package.yaml | functional.metrics | 设计DWS/ADS层 |
| requirement-analyst | requirement_package.yaml | non_functional.freshness | 选择实时/批量架构 |
| requirement-analyst | requirement_package.yaml | non_functional.retention | 设计生命周期策略 |
| requirement-analyst | requirement_package.yaml | technical.preferred_stack | 技术选型参考 |

### 自动读取上游包

```bash
# 方式1: 显式引用需求包
/arch-select 基于 requirement_package.yaml 选择架构

# 方式2: 自动发现
/arch-select --auto  # 自动读取 outputs/requirement_package.yaml
```

---

## 标准输出格式

每个架构设计任务输出标准化的 `architecture_package.yaml`：

```yaml
architecture_package:
  version: "1.0"
  metadata:
    generated_by: "architecture-designer"
    generated_at: "2024-01-15T10:00:00Z"
    source_package: "requirement_package.yaml"
    project_name: "电商数据平台"

  architecture:
    pattern: "Lambda + 湖仓一体"
    decisions:          # ADR 列表
      - adr_id: "ADR-001"
        title: "数据平台整体架构选型"
        status: "accepted"

  layers:
    ods:
      tables: [...]
      retention: "30天"
    dwd:
      tables: [...]
      retention: "1年"
    dws:
      tables: [...]
      retention: "2年"
    ads:
      tables: [...]

  tech_stack:
    storage:
      data_lake: "S3 + Iceberg"
      data_warehouse: "Snowflake"
    compute:
      batch: "EMR + Spark"
      streaming: "Flink"
    orchestration: "Airflow"

  topology:
    dag_groups: [...]
    dependencies: [...]
    scheduling: {...}
    failure_handling: {...}

  downstream_specs:
    - target: "modeling-assistant"
      input_file: "architecture_package.yaml"
      mapping:
        - "layers.dws.tables → fact_tables"
        - "layers.dwd.tables → dimension_sources"
        - "tech_stack.storage → dbt_adapter"

    - target: "etl-assistant"
      input_file: "architecture_package.yaml"
      mapping:
        - "topology.dag_groups → airflow_dag_structure"
        - "tech_stack.compute → execution_engine"

    - target: "sql-assistant"
      input_file: "architecture_package.yaml"
      mapping:
        - "tech_stack.storage → sql_dialect"
```

---

## 与下游 Skill 的联动

架构设计完成后，自动触发下游 Skill：

```bash
## 架构设计后的下一步

# 步骤1: 数据建模（推荐）
/modeling-assistant 基于以下架构设计维度模型：
- 输入文件: outputs/architecture_package.yaml
- 分层设计: layers.dwd/dws 表定义
- 技术栈: tech_stack.storage (Snowflake/Iceberg)
- SCD策略: 根据 entities 确定

# 步骤2: ETL开发
/etl-assistant 基于以下架构生成Pipeline：
- 输入文件: outputs/architecture_package.yaml
- DAG结构: topology.dag_groups
- 计算引擎: tech_stack.compute
- 调度策略: topology.scheduling

# 步骤3: SQL开发
/sql-assistant 生成各层转换SQL：
- 输入文件: outputs/architecture_package.yaml
- 方言: tech_stack.storage 指定的数仓类型
- 分层: layers 定义的表结构
```

---

## 项目初始化（推荐）

为团队建立标准化架构设计工作流：

```bash
# 创建架构设计项目骨架
bash .claude/skills/architecture-designer/scripts/init-project.sh ./data-platform "企业级数据平台"
```

自动生成目录结构：
```
data-platform/
├── PROJECT.md              # 项目中枢（架构决策记录+进度）
├── architecture/           # 架构设计文档
│   ├── 01-decisions/       # 架构决策记录(ADR)
│   ├── 02-layers/          # 分层设计
│   ├── 03-tech-stack/      # 技术栈规划
│   └── 04-topology/        # Pipeline拓扑
├── requirements/           # 输入需求（来自requirement-analyst）
│   └── requirement_package.yaml
├── specs/                  # 输出规格
│   ├── architecture_spec.yaml
│   ├── infra_spec.yaml
│   └── cost_estimate.yaml
├── docs/                   # 架构文档
│   ├── overview.md         # 架构总览
│   ├── data-flow.md        # 数据流图
│   └── ops-guide.md        # 运维指南
└── diagrams/               # 架构图
    ├── system-context.png
    ├── container-diagram.png
    └── deployment-diagram.png
```

## 快速开始

### 方式1：分阶段使用（推荐）

```bash
# 阶段1: 架构选型
/arch-select 基于电商销售分析需求选择数据架构

# 阶段2: 分层设计
/layer-design 设计ODS/DWD/DWS/ADS分层

# 阶段3: 技术规划
/tech-planning 选择合适的存储和计算引擎

# 阶段4: 拓扑设计
/topology-design 设计Pipeline依赖拓扑
```

### 方式2：端到端工作流

```bash
# 启动完整架构设计工作流
/architecture-designer 端到端设计：基于电商需求设计完整数据平台架构
```

## 核心功能详解

### 功能1：架构选型助手 (/arch-select)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 新建数据平台，需要选择整体架构方向
- 现有系统架构升级/迁移
- 多云/混合云架构设计

**架构选型决策树**：

```
需求输入
    │
    ├── 数据类型？
    │   ├── 结构化为主 → 数据仓库
    │   ├── 半/非结构化 → 数据湖
    │   └── 混合 → 湖仓一体
    │
    ├── 实时性要求？
    │   ├── 批量(T+1) → 批量架构
    │   ├── 准实时(分钟) → Lambda架构
    │   └── 实时(秒级) → Kappa/流架构
    │
    ├── 部署方式？
    │   ├── 云服务 → 云原生架构
    │   ├── 混合云 → 混合架构
    │   └── 本地 → 自建架构
    │
    └── 输出：架构决策报告
```

**输出示例**：

```yaml
# architecture/01-decisions/adr-001-architecture-choice.yaml
architecture_decision:
  adr_id: "ADR-001"
  title: "数据平台整体架构选型"
  status: "accepted"
  date: "2024-01-15"
  context:
    requirements:
      - "日增10亿条埋点数据"
      - "实时看板延迟<5秒"
      - "离线分析T+1"
      - "3年历史数据"
    constraints:
      - "团队熟悉AWS"
      - "预算限制"

  decision: "采用Lambda架构 + 湖仓一体"

  rationale:
    - "埋点数据半结构化，需要数据湖存储原始数据"
    - "实时看板需要流处理能力"
    - "离线分析需要数仓查询性能"
    - "团队AWS经验降低学习成本"

  options_considered:
    - option: "传统数据仓库"
      pros: ["查询性能好", "生态成熟"]
      cons: ["无法处理非结构化数据", "扩展成本高"]
      verdict: "rejected"

    - option: "纯数据湖"
      pros: ["存储成本低", "灵活性高"]
      cons: ["查询性能差", "数据治理难"]
      verdict: "rejected"

    - option: "Lambda + 湖仓一体"
      pros: ["兼顾实时批量", "存储灵活", "查询性能好"]
      cons: ["架构复杂", "维护成本高"]
      verdict: "accepted"

  consequences:
    positive:
      - "支持所有数据类型"
      - "实时离线一体"
    negative:
      - "需要维护两套处理逻辑"
      - "团队需要学习成本"

  related_decisions:
    - "ADR-002: 流处理引擎选型"
    - "ADR-003: 湖仓一体方案选型"
```

---

### 功能2：分层设计助手 (/layer-design)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 设计数据仓库分层架构
- 规划数据流转路径
- 制定数据生命周期策略

**标准分层模型**：

```
┌─────────────────────────────────────────────────────────────┐
│                         ADS (应用数据层)                      │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│    │  BI报表  │  │ 算法特征 │  │ 即席查询 │  │ 数据API │      │
│    └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │
├───────┬─┴──────────┬─┴──────────┬─┴──────────┬─┴───────────┤
│       │           DWS (主题宽表层)                            │
│    ┌──┴──┐     ┌──┴──┐     ┌──┴──┐     ┌──┴──┐            │
│    │用户主题│    │商品主题│    │交易主题│    │流量主题│            │
│    └─────┘     └─────┘     └─────┘     └─────┘            │
├─────────────────────────────────────────────────────────────┤
│                         DWD (明细数据层)                      │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│    │用户行为 │  │交易明细 │  │商品信息 │  │营销数据 │      │
│    └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │
├───────┬─┴──────────┬─┴──────────┬─┴──────────┬─┴───────────┤
│       │           ODS (原始数据层)                            │
│    ┌──┴──┐     ┌──┴──┐     ┌──┴──┐     ┌──┴──┐            │
│    │埋点日志│    │业务快照│    │外部数据│    │爬虫数据│            │
│    └─────┘     └─────┘     └─────┘     └─────┘            │
└─────────────────────────────────────────────────────────────┘
```

**分层设计输出示例**：

```yaml
# architecture/02-layers/layer-design.yaml
layer_architecture:
  version: "1.0"
  project: "电商数据平台"

  layers:
    - name: "ODS"
      full_name: "Operational Data Store"
      description: "原始数据层，保持数据原貌"

      tables:
        - name: "ods_log_event"
          source: "Kafka埋点"
          format: "JSON"
          retention: "30天"
          partition_by: "dt"
          storage: "S3 (Iceberg)"

        - name: "ods_mysql_orders"
          source: "MySQL订单表"
          sync_type: "CDC"
          retention: "90天"
          storage: "S3 (Iceberg)"

        - name: "ods_mysql_users"
          source: "MySQL用户表"
          sync_type: "CDC"
          retention: "90天"
          storage: "S3 (Iceberg)"

      governance:
        - "数据血缘追溯"
        - "Schema变更自动同步"
        - "数据质量基础检查"

    - name: "DWD"
      full_name: "Data Warehouse Detail"
      description: "明细数据层，清洗标准化"

      tables:
        - name: "dwd_user_event_di"
          grain: "事件级别"
          source: "ods_log_event"
          cleaning_rules:
            - "过滤机器人流量"
            - "字段标准化"
            - "ID-Mapping"
          retention: "1年"
          storage: "S3 (Iceberg)"

        - name: "dwd_trade_order_di"
          grain: "订单级别"
          source: "ods_mysql_orders"
          cleaning_rules:
            - "去重"
            - "金额单位统一"
            - "状态码转换"
          retention: "3年"
          storage: "S3 (Iceberg)"

    - name: "DWS"
      full_name: "Data Warehouse Service"
      description: "主题宽表层，轻度汇总"

      tables:
        - name: "dws_user_action_1d"
          grain: "用户+天"
          aggregation: "每日用户行为汇总"
          source: "dwd_user_event_di"
          metrics:
            - "pv_cnt"
            - "click_cnt"
            - "play_cnt"
            - "active_duration"
          retention: "2年"
          storage: "Snowflake"

        - name: "dws_trade_order_1d"
          grain: "订单+天"
          aggregation: "每日交易汇总"
          source: "dwd_trade_order_di"
          metrics:
            - "order_cnt"
            - "gmv"
            - "paid_order_cnt"
          retention: "3年"
          storage: "Snowflake"

    - name: "ADS"
      full_name: "Application Data Store"
      description: "应用数据层，面向场景"

      tables:
        - name: "ads_user_retention_1d"
          purpose: "留存分析"
          source: "dws_user_action_1d"
          metrics:
            - "new_user_cnt"
            - "retention_1d"
            - "retention_7d"
            - "retention_30d"
          consumers: ["BI报表", "运营后台"]
          storage: "Snowflake"

        - name: "ads_sales_dashboard_1d"
          purpose: "销售实时看板"
          source: "dws_trade_order_1d"
          refresh_mode: "准实时(1min)"
          consumers: ["实时看板"]
          storage: "ClickHouse"

  data_flow:
    - from: "业务系统"
      to: "ODS"
      method: "CDC/日志采集"

    - from: "ODS"
      to: "DWD"
      method: "Spark批处理"
      schedule: "每小时"

    - from: "DWD"
      to: "DWS"
      method: "Spark批处理"
      schedule: "每日"

    - from: "DWS"
      to: "ADS"
      method: "Spark/ETL"
      schedule: "每日/实时"

  lifecycle_policies:
    hot_data:    # 7天内，SSD存储
      layers: ["ADS", "DWS"]
      retention: "7天"

    warm_data:   # 7-90天，标准存储
      layers: ["DWD"]
      retention: "90天"

    cold_data:   # 90天+，归档存储
      layers: ["ODS", "DWD"]
      retention: "3年"
      archive_to: "Glacier"
```

---

### 功能3：技术规划助手 (/tech-planning)

**Agent类型**：Explore
**工具权限**：Read, Grep, Glob

**使用场景**：
- 为架构选择合适的具体技术组件
- 评估不同技术方案的成本
- 规划基础设施资源

**技术选型矩阵**：

| 类别 | 选项 | 适用场景 | 成本 | 学习曲线 |
|------|------|---------|------|---------|
| **数仓** | Snowflake | 云原生，弹性扩展 | $$$ | 低 |
| | BigQuery | 与GCP深度集成 | $$$ | 低 |
| | Redshift | AWS生态 | $$ | 中 |
| | Databricks | 湖仓一体 | $$$$ | 高 |
| **数据湖** | S3 + Iceberg | 开放格式 | $ | 中 |
| | Delta Lake | Databricks生态 | $$ | 中 |
| | Hudi | 增量处理 | $ | 高 |
| **流处理** | Flink | 复杂流处理 | $$ | 高 |
| | Spark Streaming | 批流统一 | $$ | 中 |
| | Kafka Streams | 轻量级 | $ | 中 |
| **调度** | Airflow | 复杂DAG | 免费 | 中 |
| | Dagster | 数据感知 | 免费 | 中 |
| | Prefect | 现代工作流 | 免费 | 低 |

**技术规划输出示例**：

```yaml
# architecture/03-tech-stack/tech-stack.yaml
tech_stack:
  version: "1.0"
  architecture_pattern: "Lambda + 湖仓一体"

  infrastructure:
    cloud_provider: "AWS"
    region: "ap-northeast-1"
    vpc:
      cidr: "10.0.0.0/16"
      subnets:
        - type: "public"
          azs: ["a", "b", "c"]
        - type: "private"
          azs: ["a", "b", "c"]

  storage:
    data_lake:
      service: "S3"
      bucket: "company-data-lake"
      format: "Iceberg"
      zones:
        - name: "raw"
          path: "s3://company-data-lake/raw/"
          lifecycle: "30天转Glacier"
        - name: "processed"
          path: "s3://company-data-lake/processed/"
          lifecycle: "90天转Glacier"

    data_warehouse:
      service: "Snowflake"
      edition: "Enterprise"
      warehouses:
        - name: "ETL_WH"
          size: "Large"
          auto_suspend: "5min"
          use: "数据加载"
        - name: "ANALYTICS_WH"
          size: "XLarge"
          auto_suspend: "10min"
          use: "BI查询"

    real_time_store:
      cache: "Redis"
      node_type: "cache.r6g.xlarge"
      use: "实时指标缓存"

      olap: "ClickHouse"
      instance_type: "r6g.2xlarge"
      use: "实时分析查询"

  compute:
    batch_processing:
      service: "EMR"
      version: "6.10"
      applications: ["Spark", "Hive", "Iceberg"]
      master: "m5.xlarge"
      core: "r5.2xlarge (3-10节点)"

    stream_processing:
      service: "Flink"
      deployment: "EKS"
      resources:
        taskmanagers: "10 pods"
        slots_per_tm: "4"

    transformation:
      service: "dbt"
      version: "1.7"
      execution: "Snowflake"

  messaging:
    event_streaming:
      service: "Kafka (MSK)"
      version: "3.5"
      instance_type: "kafka.m5.large"
      brokers: "3"
      topics:
        - name: "user-events"
          partitions: "100"
          retention: "7天"

  orchestration:
    workflow_scheduler:
      service: "Airflow (MWAA)"
      version: "2.7"
      environment_class: "mw1.large"

  data_governance:
    catalog: "Glue Data Catalog"
    lineage: "OpenLineage"
    quality: "Great Expectations"
    monitoring: "Datadog"

  cost_estimate:
    monthly:
      storage:
        s3: "$500"
        snowflake: "$2,000"
        redis: "$300"
      compute:
        emr: "$1,500"
        flink: "$1,200"
        msk: "$800"
      others: "$1,000"
      total: "$7,300/月"

    optimization_suggestions:
      - "使用Spot实例可节省EMR成本40%"
      - "Snowflake warehouse按需启停"
      - "S3生命周期策略优化存储成本"
```

---

### 功能4：拓扑设计助手 (/topology-design)

**Agent类型**：general-purpose
**工具权限**：Read, Grep, Glob, Edit, Write, Bash

**使用场景**：
- 设计Pipeline之间的依赖关系
- 规划调度策略
- 设计失败恢复机制

**拓扑设计输出示例**：

```yaml
# architecture/04-topology/pipeline-topology.yaml
pipeline_topology:
  version: "1.0"

  dag_groups:
    - name: "ingestion"
      description: "数据采集"
      pipelines:
        - name: "kafka_to_ods"
          type: "streaming"
          schedule: "continuous"
          sla: "延迟<1分钟"

        - name: "mysql_cdc_to_ods"
          type: "streaming"
          schedule: "continuous"
          sla: "延迟<5分钟"

    - name: "processing"
      description: "数据处理"
      pipelines:
        - name: "ods_to_dwd"
          type: "batch"
          schedule: "每小时"
          depends_on: ["ingestion"]

        - name: "dwd_to_dws"
          type: "batch"
          schedule: "每日 02:00"
          depends_on: ["ods_to_dwd"]

    - name: "serving"
      description: "数据服务"
      pipelines:
        - name: "dws_to_ads"
          type: "batch"
          schedule: "每日 04:00"
          depends_on: ["dwd_to_dws"]

  dependencies:
    - upstream: "mysql_cdc_to_ods"
      downstream: "ods_to_dwd"
      type: "data_dependency"
      check: "ods表数据新鲜度"

    - upstream: "ods_to_dwd"
      downstream: "dwd_to_dws"
      type: "execution_dependency"

  scheduling:
    strategy: "时间驱动 + 数据依赖"
    timezone: "Asia/Shanghai"
    catchup: false
    max_active_runs: 1

  failure_handling:
    retry_policy:
      retries: 3
      retry_delay: "5min"
      retry_exponential_backoff: true

    alert_rules:
      - condition: "失败"
        severity: "critical"
        notify: ["oncall", "slack"]

      - condition: "SLA延迟>30分钟"
        severity: "warning"
        notify: ["slack"]

    recovery:
      - scenario: "单Pipeline失败"
        action: "自动重试 → 告警"

      - scenario: "多Pipeline失败"
        action: "暂停调度 → 人工介入"

      - scenario: "数据质量检查失败"
        action: "阻断下游 → 通知负责人"

  monitoring:
    metrics:
      - "Pipeline执行时长"
      - "数据处理记录数"
      - "SLA达成率"
      - "失败率"

    dashboards:
      - name: "Pipeline健康度"
        url: "https://datadog/dashboard/pipeline"

      - name: "SLA达成率"
        url: "https://datadog/dashboard/sla"
```

---

## 配合使用流程

```
结构化需求 (来自requirement-analyst)
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段1: 架构选型 (/arch-select)                               │
│  ├─ 输入：需求包 + 约束条件                                   │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：架构决策记录 (ADR)                                  │
│       - 数据架构类型                                          │
│       - 处理模式（批/流）                                     │
│       - 部署方式                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段2: 分层设计 (/layer-design)                              │
│  ├─ 输入：架构决策 + 业务实体                                 │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：分层架构设计                                        │
│       - ODS/DWD/DWS/ADS分层                                   │
│       - 数据流转路径                                          │
│       - 生命周期策略                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段3: 技术规划 (/tech-planning)                             │
│  ├─ 输入：分层架构 + 性能要求                                 │
│  ├─ 处理：Explore Agent (方案对比)                          │
│  └─ 输出：技术栈规格                                          │
│       - 存储选型                                              │
│       - 计算选型                                              │
│       - 成本估算                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段4: 拓扑设计 (/topology-design)                           │
│  ├─ 输入：技术栈 + 数据流                                     │
│  ├─ 处理：general-purpose Agent                              │
│  └─ 输出：Pipeline拓扑                                        │
│       - DAG设计                                               │
│       - 调度策略                                              │
│       - 失败恢复                                              │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
              架构设计包 (architecture_package.yaml)
                     │
                     ▼
              驱动下游建模与开发
```

---

## 与需求分析 Skill 的关系

```
requirement-analyst (需求层)
    │ 输出: requirement_package.yaml
    ▼
architecture-designer (架构层)
    │ 输入: 业务需求 + 数据实体 + 指标要求
    │ 输出: architecture_package.yaml
    ▼
modeling-assistant (模型层)
    │ 输入: 架构分层 + 存储选型
    │ 输出: 维度模型 + dbt模型
    ▼
etl-assistant (开发层)
    │ 输入: 拓扑设计 + 技术栈
    │ 输出: Pipeline代码
    ▼
dq-assistant (质量层)
    │ 输入: 全层数据流
    └─ 输出: 质量规则
```

### 上下文传递

```yaml
# architecture_package.yaml 标准格式
architecture_package:
  version: "1.0"
  source: "requirement-analyst"

  architecture:
    pattern: "Lambda + 湖仓一体"
    decisions: [...]  # ADR列表

  layers:
    ods: {...}
    dwd: {...}
    dws: {...}
    ads: {...}

  tech_stack:
    storage: {...}
    compute: {...}
    orchestration: {...}

  topology:
    dag_groups: [...]
    dependencies: [...]
    scheduling: {...}

  downstream_specs:
    model_spec:  # 传递给modeling-assistant
      file: "specs/model_spec.yaml"
    etl_spec:    # 传递给etl-assistant
      file: "specs/etl_spec.yaml"
    infra_spec:  # 传递给部署工具
      file: "specs/infra_spec.yaml"
```

---

## 最佳实践

### 1. 架构决策记录(ADR)

每个重大架构决策都应记录：
- 决策背景(Context)
- 考虑过的选项(Options)
- 决策结果(Decision)
- 影响分析(Consequences)

### 2. 分层设计原则

- **ODS**: 原始数据，不做清洗，保留时间视成本而定
- **DWD**: 明细数据，清洗标准化，统一口径
- **DWS**: 轻度汇总，面向主题，服务多场景
- **ADS**: 应用数据，高度聚合，面向具体场景

### 3. 技术选型原则

- 团队熟悉度 > 技术先进性
- 云原生优先，降低运维成本
- 开放标准优先，避免 vendor lock-in
- 成本效益分析，预留扩展空间

---

## 故障排除

### 架构选型争议
1. 明确约束条件（预算、团队、时间）
2. 制作对比矩阵打分
3. 小规模POC验证

### 技术方案不可行
1. 检查需求是否理解正确
2. 寻找替代技术方案
3. 调整架构分层策略

### 成本超出预算
1. 优化存储策略（冷热分离）
2. 使用Spot/Preemptible实例
3. 调整SLA要求

---

## 示例场景

详见 [examples/](examples/) 目录：

| 示例 | 场景 | 流程 |
|------|------|------|
| [example-ecommerce-platform.md](examples/example-ecommerce-platform.md) | 电商数据平台架构 | 选型 → 分层 → 技术 → 拓扑 |
| [example-realtime-analytics.md](examples/example-realtime-analytics.md) | 实时分析平台架构 | 选型 → 分层 → 技术 → 拓扑 |

---

## 路线图

### v1.0.0 (当前)
- ✅ 架构选型助手 (arch-select)
- ✅ 分层设计助手 (layer-design)
- ✅ 技术规划助手 (tech-planning)
- ✅ 拓扑设计助手 (topology-design)
- ✅ ADR模板与规范

### v1.1.0 (计划)
- 🔄 成本优化建议
- 🔄 性能基准测试模板
- 🔄 多云架构支持

### v2.0.0 (计划)
- 📝 AI驱动架构优化
- 📝 架构演进路径规划
- 📝 自动基础设施即代码生成

---

**提示**：本Skill与《AI编程与数据开发工程师融合实战手册》§03 数据架构设计章节配套使用。
