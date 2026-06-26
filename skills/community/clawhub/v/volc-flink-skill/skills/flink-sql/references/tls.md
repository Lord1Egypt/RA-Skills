# TLS (Log Service) via Kafka protocol notes

这份文档承接历史 `flink-template-tls` 中的“参数说明/约束/易错点”，供 `flink-sql/assets/tls.md` 的模板配套参考。

## 前置条件与约束

- TLS 控制台已开通 Kafka 协议消费/写入能力
- TLS 与 Flink 需在同一个 Region，建议使用私网地址访问
- 历史建议：Flink 版本使用 `Flink-1.16-volcano` 及以上

## 关键规则（最容易写错）

- 消费 topic: 必须是 `out-<tls-topic-id>`
- 写入 topic: 必须是 `<tls-topic-id>`（不要加 `out-`）
- 端口：消费通常 `9093`；写入通常 `9094`
- 鉴权：`SASL_SSL` + `PLAIN` + JAAS
  - JAAS `username`: `<tls-project-id>`
  - JAAS `password`: `<ak>#<sk>`
- 写入必须关闭幂等：`properties.enable.idempotence = false`

## Source 常用参数

- `properties.bootstrap.servers`: `tls-<region>.ivolces.com:9093`
- `properties.group.id`: TLS 消费组 ID
- `scan.startup.mode`: `latest-offset` / `group-offsets` / `timestamp` / `specific-offsets`
  - `timestamp` 需配 `scan.startup.timestamp-millis`
  - `specific-offsets` 需配 `scan.startup.specific-offsets`
- `format`: value 反序列化格式（常见 `json/csv/raw`，以平台支持为准）

## Sink 吞吐与成本（按需启用）

历史建议值与说明（需要结合吞吐/延迟权衡）：

- `properties.compression.type`: 推荐 `lz4`
- `properties.batch.size`:
  - 启用压缩：`262144`
  - 不启用压缩：`2621440`
- `properties.linger.ms`: 推荐 `100`
- `properties.max.request.size`:
  - 启用压缩：`1046576`
  - 不启用压缩：`10465760`
- `properties.buffer.memory`: 建议 `>= batch.size * 分区数 * 2`
- `sink.partitioner`:
  - `fixed`（默认）：每个 Flink 分区对应一个 TLS 分区
  - `round-robin`：轮询分配到各分区

## 参考

- 官方文档链接汇总：`references/connectors.md`

