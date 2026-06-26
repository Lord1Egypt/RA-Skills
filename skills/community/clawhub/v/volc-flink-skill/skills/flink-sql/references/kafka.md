# Kafka connector notes

这份文档承接历史 `flink-template-kafka` 中的“参数说明/最佳实践/注意事项”，供 `flink-sql/assets/kafka.md` 的模板配套参考。

## 常用参数说明

- `topic`: Kafka topic 名称
- `properties.bootstrap.servers`: Kafka broker 地址
- `properties.group.id`: 消费组 ID
- `scan.startup.mode`: 启动模式（见下文表格）
- `format`: `json` / `csv` / `avro` / `debezium-json` 等（以平台支持为准）
- JSON 容错：
  - `json.fail-on-missing-field`: 缺失字段是否失败
  - `json.ignore-parse-errors`: 解析错误是否忽略

## Sink 吞吐优化参数（常用三件套）

当写入吞吐不足时，通常优先调整：

- `properties.batch.size`: 单个 batch 最大字节数（示例：`524288` = 512KB）
- `properties.linger.ms`: batch 聚合等待时间（示例：`500`ms）
- `properties.buffer.memory`: 生产者缓冲区内存（示例：`134217728` = 128MB）

## 读取优化

- `scan.parallelism`: 单独设置 source 并发，通常与 Kafka 分区数一致
- `scan.topic-partition-discovery.interval`: 定期发现新分区（示例：`120s`），默认不启用

## 启动模式选择

| 启动模式 | 说明 | 适用场景 |
|---|---|---|
| `earliest-offset` | 从最早位点开始读取 | 首次启动，需要消费历史数据 |
| `latest-offset` | 从最新位点开始读取 | 首次启动，只消费新数据 |
| `group-offsets` | 从消费组位点读取（默认） | 有 checkpoint 恢复/稳定消费组位点 |
| `timestamp` | 从指定时间点读取 | 需要从特定时间点恢复 |
| `specific-offsets` | 从指定分区位点读取 | 需要精确控制消费位点 |

## Offset 管理建议

- 推荐：依赖 Flink checkpoint
  - 开启 checkpoint 后，source 在完成 checkpoint 时提交位点，保证状态与位点一致
- 未开 checkpoint：依赖 Kafka consumer 自动提交（风险更高）
  - `properties.enable.auto.commit = true`
  - `properties.auto.commit.interval.ms = 5000`

## 注意事项

- Kafka 版本：不再支持 `kafka-0.10` / `kafka-0.11` 连接器版本（按历史说明）
- BMQ：若用 Kafka connector 消费 BMQ，建议在 BMQ 侧提前创建 consumer group，否则可能无法正常提交 offset
- Flink 1.16/1.17 SSL：Kafka client 3.x 默认启用 hostname 校验，必要时可设 `properties.ssl.endpoint.identification.algorithm = ''` 跳过校验以规避 `SSLHandshakeException`

## 参考

- 官方文档链接汇总：`references/connectors.md`

