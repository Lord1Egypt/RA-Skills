# 示例：实时分析平台架构设计

本示例展示纯实时场景下的架构设计，适合监控告警、实时决策等业务。

---

## 场景背景

某金融科技公司需要建设实时风控和交易监控平台。

**需求摘要**：
- 每秒10万笔交易，峰值30万TPS
- 风控决策延迟<100ms
- 实时监控大屏延迟<1秒
- 99.99%可用性要求

---

## 架构选型

### 决策：Kappa架构

由于需求是**纯实时**，选择 Kappa架构 简化系统复杂度。

```
┌─────────────────────────────────────────────────────────┐
│                    应用层                                │
│   风控决策    实时监控    告警通知    运营后台           │
└────────┬───────────┬──────────┬──────────┬─────────────┘
         │           │          │          │
┌────────┴───────────┴──────────┴──────────┴─────────────┐
│              服务层 (Flink SQL + 状态存储)              │
│   规则引擎    聚合计算    异常检测    指标计算          │
└────────┬───────────────────────────────┬───────────────┘
         │                               │
┌────────▼─────────┐        ┌───────────▼──────────────┐
│   流处理层        │        │      状态存储           │
│   Flink Cluster   │◄──────►│   RocksDB State Backend │
└────────┬─────────┘        └───────────────────────────┘
         │
┌────────▼──────────────────────────────────────────────┐
│              消息队列 (Kafka - 持久化日志)              │
│   Topic: transactions (100分区, 保留7天)               │
└─────────────────────────────────────────────────────────┘
```

---

## 分层设计

由于纯实时场景，采用简化分层：

```yaml
layer_architecture:
  streaming_raw:
    description: "实时原始流"
    topic: kafka_transactions
    format: Avro
    schema_registry: Confluent Schema Registry

  streaming_processed:
    description: "实时处理流"
    jobs:
      - name: fraud_detection
        function: "CEP复杂事件处理"
        latency: "<100ms"

      - name: real_time_aggregation
        function: "窗口聚合(1min/5min)"
        state_backend: RocksDB

  serving:
    description: "实时服务层"
    stores:
      - name: redis_metrics
        use: "实时指标缓存"
        ttl: 1hour

      - name: hbase_profiles
        use: "用户风控画像"

      - name: clickhouse_analytics
        use: "实时OLAP查询"
```

---

## 技术规划

```yaml
tech_stack:
  messaging:
    kafka:
      version: "3.5"
      cluster: 6 brokers (m5.2xlarge)
      partitions: 100
      replication: 3
      retention: "7天"

  processing:
    flink:
      deployment: "EKS"
      version: "1.18"
      taskmanagers: 50
      slots_per_tm: 4
      checkpointing:
        interval: "30s"
        backend: "RocksDB"
        storage: "S3"

  state_storage:
    rocksdb:
      incremental_checkpoint: true
      local_recovery: true

  serving:
    redis:
      mode: "cluster"
      nodes: 6 (cache.r6g.xlarge)

    hbase:
      deployment: "EMR"
      masters: 2
      regionservers: 6

    clickhouse:
      cluster: 3 shards × 2 replicas

  schema_management:
    confluent_schema_registry:
      format: Avro
      compatibility: BACKWARD
```

---

## 拓扑设计

```yaml
stream_topology:
  jobs:
    - name: transaction_enrichment
      parallelism: 20
      input: kafka_transactions
      output: kafka_enriched
      latency_sla: "<50ms"

    - name: fraud_detection
      parallelism: 30
      input: kafka_enriched
      state: "用户行为模式(24h窗口)"
      output: kafka_alerts
      latency_sla: "<100ms"

    - name: real_time_metrics
      parallelism: 10
      input: kafka_enriched
      windows: [1min, 5min, 15min]
      output: redis_metrics

  failure_handling:
    checkpointing:
      interval: 30s
      timeout: 10min
      min_pause: 5s

    restart_strategy:
      type: fixed_delay
      attempts: 10
      delay: 10s

    alert:
      - condition: "checkpoint失败"
        severity: critical
      - condition: "延迟>SLA"
        severity: warning
```

---

## 关键设计点

| 设计点 | 决策 | 理由 |
|--------|------|------|
| **架构** | Kappa | 纯实时，简化维护 |
| **消息队列** | Kafka 100分区 | 支持30万TPS |
| **状态存储** | RocksDB | 高性能本地状态 |
| **Checkpont** | 30秒间隔 | 平衡性能和恢复时间 |
| **Schema** | Avro + Registry | 强类型，向后兼容 |

---

## 成本估算

| 组件 | 配置 | 月成本 |
|------|------|--------|
| Kafka | 6×m5.2xlarge | $4,000 |
| Flink | 50 pods (4vCPU) | $8,000 |
| Redis | 6节点集群 | $2,000 |
| HBase | 8节点 EMR | $3,000 |
| ClickHouse | 6节点 | $3,000 |
| **总计** | | **$20,000/月** |

这个设计满足了金融级实时要求：
- **低延迟**: Flink + RocksDB 本地状态，<100ms决策
- **高吞吐**: Kafka 100分区，支持30万TPS
- **高可用**: 3副本 + checkpoint，99.99%可用性
