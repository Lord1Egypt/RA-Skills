# 示例：电商数据平台架构设计

本示例展示如何为电商场景设计完整的数据平台架构，包含架构选型、分层设计、技术规划和拓扑设计全流程。

---

## 场景背景

某电商平台需要建设企业级数据平台，支撑业务分析和实时决策。

**需求摘要**（来自requirement-analyst）：
- 日增10亿条埋点事件 + 100万订单
- 实时看板（延迟<5秒）+ 离线分析（T+1）
- 3年历史数据，约10PB总存储
- 用户画像、推荐系统、BI报表多场景

---

## 阶段1：架构选型

### 关键决策因素

| 因素 | 分析 |
|------|------|
| **数据类型** | 结构化（订单）+ 半结构化（埋点JSON） |
| **实时性** | 混合：实时看板 + 离线分析 |
| **数据量** | 大规模：10PB，日增TB级 |
| **使用场景** | 多样：BI、ML、实时决策 |
| **团队能力** | 中等，熟悉AWS |

### 架构决策

```yaml
# architecture/01-decisions/adr-001-architecture-choice.yaml
architecture_decision:
  adr_id: "ADR-001"
  title: "数据平台整体架构选型"
  status: "accepted"
  date: "2024-01-15"

  decision: "采用 Lambda架构 + 湖仓一体"

  rationale:
    - "埋点数据半结构化，需要数据湖存储原始日志"
    - "实时看板需要Flink流处理能力"
    - "离线分析需要Snowflake的查询性能"
    - "湖仓一体(Iceberg)提供统一元数据管理"

  architecture_diagram: |
    ┌─────────────────────────────────────────────────────────┐
    │  实时层 (Speed Layer)                                    │
    │  Kafka → Flink → Redis/ClickHouse → 实时看板            │
    └────────────────────┬────────────────────────────────────┘
                         │
    ┌────────────────────▼────────────────────────────────────┐
    │  批处理层 (Batch Layer)                                  │
    │  S3(Iceberg) → Spark → Snowflake → BI/报表              │
    └─────────────────────────────────────────────────────────┘

  components:
    streaming:
      - "Kafka: 事件总线"
      - "Flink: 实时处理"
      - "Redis: 实时指标缓存"
      - "ClickHouse: 实时OLAP"

    batch:
      - "S3: 数据湖存储"
      - "Iceberg: 湖仓表格式"
      - "Spark: 批处理"
      - "Snowflake: 数据仓库"

    orchestration:
      - "Airflow: 工作流调度"
      - "DBT: 数据转换"

  cost_estimate:
    monthly: "$15,000 - $20,000"
    justification: "满足所有业务场景，团队熟悉度高"
```

---

## 阶段2：分层设计

### 完整分层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                           ADS (应用层)                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │  实时看板    │ │  BI报表      │ │  用户画像    │ │  推荐特征  │ │
│  │  ClickHouse  │ │  Snowflake   │ │  HBase       │ │  Redis     │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│                           DWS (主题层)                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │  用户主题    │ │  交易主题    │ │  商品主题    │ │  流量主题  │ │
│  │  dws_user_*  │ │  dws_trade_* │ │  dws_prod_*  │ │  dws_traf_*│ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│                           DWD (明细层)                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │  事件明细    │ │  订单明细    │ │  用户行为    │ │  营销数据  │ │
│  │  dwd_event_* │ │  dwd_order_* │ │  dwd_action_*│ │  dwd_mkt_* │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│                           ODS (原始层)                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │  埋点日志    │ │  订单CDC     │ │  商品快照    │ │  外部数据  │ │
│  │  ods_events  │ │  ods_orders  │ │  ods_product │ │  ods_ext_* │ │
│  │  Kafka → S3  │ │  MySQL CDC   │ │  每日快照    │ │  API       │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 分层详细设计

```yaml
# architecture/02-layers/layer-design.yaml
layer_architecture:
  ods:
    description: "原始数据层 - 保持数据原貌"

    tables:
      - name: ods_kafka_events
        source: "埋点Kafka"
        format: "JSON"
        daily_volume: "10亿条/1TB"
        retention: "30天"
        storage: "S3 (Iceberg)"
        partition: dt

      - name: ods_mysql_orders_cdc
        source: "订单MySQL CDC"
        format: "Debezium JSON"
        daily_volume: "100万条/10GB"
        retention: "90天"
        storage: "S3 (Iceberg)"

      - name: ods_mysql_users_cdc
        source: "用户MySQL CDC"
        format: "Debezium JSON"
        daily_volume: "50万条/5GB"
        retention: "90天"
        storage: "S3 (Iceberg)"

      - name: ods_product_snapshot
        source: "商品表快照"
        format: "Parquet"
        schedule: "每日"
        retention: "30天"
        storage: "S3"

  dwd:
    description: "明细数据层 - 清洗标准化"

    tables:
      - name: dwd_user_event_di
        grain: "事件级别"
        source: ods_kafka_events
        cleaning:
          - "过滤机器人(IP黑名单)"
          - "字段标准化"
          - "ID-Mapping(设备→用户)"
          - "时间统一UTC"
        daily_volume: "9亿条/900GB"
        retention: "1年"
        storage: "S3 (Iceberg)"

      - name: dwd_trade_order_di
        grain: "订单级别"
        source: ods_mysql_orders_cdc
        cleaning:
          - "去重(order_id)"
          - "金额单位统一(分→元)"
          - "状态码标准化"
          - "时间戳验证"
        daily_volume: "100万条/5GB"
        retention: "3年"
        storage: "S3 (Iceberg)"

  dws:
    description: "主题宽表层 - 轻度汇总"

    tables:
      - name: dws_user_action_1d
        grain: "用户+日期"
        source: dwd_user_event_di
        metrics:
          - pv_cnt: "曝光次数"
          - click_cnt: "点击次数"
          - play_cnt: "播放次数"
          - play_duration: "播放时长"
          - like_cnt: "点赞数"
        daily_volume: "5000万条/2GB"
        retention: "2年"
        storage: "Snowflake"

      - name: dws_trade_summary_1d
        grain: "多维+日期"
        dimensions: [用户等级, 地区, 商品类目]
        source: dwd_trade_order_di
        metrics:
          - order_cnt: "订单数"
          - gmv: "成交金额"
          - paid_order_cnt: "支付订单数"
          - paid_gmv: "实付金额"
        daily_volume: "100万条/100MB"
        retention: "3年"
        storage: "Snowflake"

  ads:
    description: "应用数据层 - 场景专用"

    tables:
      - name: ads_realtime_dashboard
        purpose: "实时销售看板"
        refresh: "1分钟"
        source: "Flink实时聚合"
        storage: "ClickHouse"

      - name: ads_user_profile
        purpose: "用户画像服务"
        refresh: "每日"
        source: dws_user_action_1d
        features:
          - interest_tags: "兴趣标签(TF-IDF)"
          - activity_level: "活跃度分级"
          - lifecycle_stage: "生命周期阶段"
        storage: "HBase"

      - name: ads_user_retention
        purpose: "留存分析报表"
        refresh: "每日"
        source: dws_user_action_1d
        metrics: [new_user_cnt, retention_1d, retention_7d, retention_30d]
        storage: "Snowflake"

  data_flow:
    - path: "业务系统 → ODS"
      methods:
        - "埋点: Kafka实时采集"
        - "MySQL: Debezium CDC"
        - "商品: 每日Spark快照"

    - path: "ODS → DWD"
      method: "Spark批处理"
      schedule: "每小时"
      sla: "延迟<1小时"

    - path: "DWD → DWS"
      method: "Spark批处理 + DBT"
      schedule: "每日 02:00"
      sla: "4小时内完成"

    - path: "DWS → ADS"
      method: "Spark/DBT"
      schedule: "每日 04:00"

    - path: "实时流"
      method: "Kafka → Flink → ClickHouse/Redis"
      latency: "<5秒"
```

---

## 阶段3：技术规划

### 完整技术栈

```yaml
# architecture/03-tech-stack/tech-stack.yaml
tech_stack:
  cloud: AWS ap-northeast-1

  data_ingestion:
    event_streaming:
      service: "MSK (Kafka)"
      config:
        instance: kafka.m5.2xlarge
        brokers: 6
        partitions: 200
        retention: "7天"

    cdc:
      service: "Debezium + MSK Connect"
      sources: [mysql_orders, mysql_users, mysql_products]

  storage:
    data_lake:
      service: "S3"
      structure:
        raw: "s3://company-raw-data/{source}/{table}/dt={date}/"
        processed: "s3://company-processed/{layer}/{table}/dt={date}/"
      lifecycle:
        - "30天转IA"
        - "90天转Glacier"

    table_format:
      service: "Apache Iceberg"
      features:
        - "ACID事务"
        - "Schema演进"
        - "时间旅行"
        - "分区演进"

    data_warehouse:
      service: "Snowflake"
      config:
        edition: "Enterprise"
        warehouses:
          - name: ETL_WH
            size: Large
            auto_suspend: 300
          - name: ANALYTICS_WH
            size: XLarge
            auto_suspend: 600

    real_time_store:
      olap: "ClickHouse"
        cluster: 3节点
        instance: r6g.2xlarge
      cache: "ElastiCache Redis"
        node: cache.r6g.xlarge
        cluster_mode: enabled

  compute:
    batch_processing:
      service: "EMR"
      version: "6.10"
      applications: [Spark, Hive, Iceberg, JupyterHub]
      hardware:
        master: 1 × m5.xlarge
        core: 3-20 × r5.2xlarge (自动扩缩)

    stream_processing:
      service: "Flink on EKS"
      config:
        taskmanagers: 20
        slots_per_tm: 4
        checkpointing: "S3"

    transformation:
      service: "dbt"
      version: "1.7"
      execution: "Snowflake"

  orchestration:
    workflow: "MWAA (Airflow)"
    environment: mw1.large
    dags:
      - ods_to_dwd_hourly
      - dwd_to_dws_daily
      - dws_to_ads_daily
      - data_quality_checks

  governance:
    catalog: "Glue Data Catalog"
    lineage: "OpenLineage"
    quality: "Great Expectations"
    monitoring: "Datadog + CloudWatch"

  cost_estimate:
    monthly_breakdown:
      kafka_msk: "$2,500"
      s3_storage: "$3,000"
      snowflake: "$5,000"
      emr: "$2,500"
      eks_flink: "$2,000"
      clickhouse: "$1,500"
      redis: "$800"
      mwaa: "$1,000"
      others: "$1,200"
      total: "$19,500/月"

    optimization:
      - "EMR使用Spot实例节省40%"
      - "Snowflake warehouse按需启停"
      - "S3生命周期策略"
```

---

## 阶段4：拓扑设计

### Pipeline分组与依赖

```yaml
# architecture/04-topology/pipeline-topology.yaml
pipeline_topology:
  dag_groups:
    - name: ingestion
      description: "数据采集"
      type: streaming
      pipelines:
        - name: kafka_to_ods_raw
          schedule: continuous
          sla: "延迟<1分钟"

        - name: mysql_cdc_orders
          schedule: continuous
          sla: "延迟<5分钟"

        - name: mysql_cdc_users
          schedule: continuous
          sla: "延迟<5分钟"

    - name: processing_hourly
      description: "小时级处理"
      type: batch
      schedule: "每小时"
      pipelines:
        - name: ods_events_to_dwd
          depends_on: [kafka_to_ods_raw]
          check: "ods_kafka_events有新分区"

    - name: processing_daily
      description: "日级处理"
      type: batch
      schedule: "02:00"
      pipelines:
        - name: dwd_to_dws_user
          depends_on: [ods_events_to_dwd, mysql_cdc_users]

        - name: dwd_to_dws_trade
          depends_on: [mysql_cdc_orders]

        - name: dws_to_ads_profile
          depends_on: [dwd_to_dws_user]

        - name: dws_to_ads_retention
          depends_on: [dwd_to_dws_user]

        - name: dws_to_ads_sales
          depends_on: [dwd_to_dws_trade]

    - name: quality_checks
      description: "数据质量"
      type: batch
      schedule: "03:00"
      pipelines:
        - name: dwd_quality_check
        - name: dws_quality_check
        - name: ads_quality_check

  scheduling:
    timezone: "Asia/Shanghai"
    catchup: false
    max_active_runs: 1
    concurrency: 10

  failure_handling:
    retry_policy:
      default:
        retries: 3
        retry_delay: "5min"
        retry_exponential_backoff: true

    alert_rules:
      - name: pipeline_failure
        condition: "任务失败且重试耗尽"
        severity: critical
        notify: [pagerduty, slack]

      - name: sla_breach
        condition: "SLA延迟>30分钟"
        severity: warning
        notify: [slack]

      - name: data_quality_fail
        condition: "质量检查失败"
        severity: critical
        notify: [slack, email]
        action: "阻断下游"

  monitoring:
    metrics:
      - pipeline_execution_time
      - records_processed
      - sla_compliance_rate
      - error_rate
      - resource_utilization

    dashboards:
      - name: "Pipeline健康度"
        tool: Datadog
      - name: "SLA达成率"
        tool: Datadog
      - name: "Snowflake监控"
        tool: Snowflake
```

---

## 架构包输出

```yaml
# specs/architecture_package.yaml
architecture_package:
  version: "1.0"
  project: "电商数据平台"

  architecture:
    pattern: "Lambda + 湖仓一体"
    decisions:
      - adr-001-architecture-choice
      - adr-002-lake-format-iceberg
      - adr-003-streaming-flink

  layers:
    ods: { tables: 4, daily_volume: "1TB", storage: "S3" }
    dwd: { tables: 6, daily_volume: "1TB", storage: "S3 Iceberg" }
    dws: { tables: 8, daily_volume: "5GB", storage: "Snowflake" }
    ads: { tables: 12, storage: "Snowflake/ClickHouse/HBase" }

  tech_stack:
    cloud: AWS
    streaming: [MSK, Flink]
    batch: [EMR, Spark, dbt]
    storage: [S3, Iceberg, Snowflake, ClickHouse, HBase, Redis]
    orchestration: [MWAA Airflow]

  cost:
    monthly: "$19,500"
    annual: "$234,000"

  downstream_specs:
    modeling_spec:
      content: |
        基于DWS层设计维度模型：
        - 用户维度: SCD Type 2
        - 商品维度: SCD Type 2
        - 事实表: 订单项粒度

    etl_spec:
      content: |
        Pipeline实现要求：
        - ODS→DWD: Spark批处理，小时级
        - DWD→DWS: Spark + dbt，日级
        - 实时流: Flink → ClickHouse
```

---

## 设计总结

| 维度 | 设计决策 |
|------|---------|
| **架构模式** | Lambda + 湖仓一体 |
| **数据分层** | ODS/DWD/DWS/ADS 四层 |
| **存储策略** | S3(Iceberg) + Snowflake + ClickHouse |
| **计算引擎** | Spark(批) + Flink(流) |
| **调度** | Airflow |
| **月成本** | ~$20K |

这个架构设计满足了电商平台的多样化需求：
- **实时性**: Flink + ClickHouse 支持<5秒延迟
- **成本**: S3生命周期 + Spot实例优化成本
- **扩展性**: 云原生架构，弹性扩缩容
- **维护性**: 托管服务降低运维负担
