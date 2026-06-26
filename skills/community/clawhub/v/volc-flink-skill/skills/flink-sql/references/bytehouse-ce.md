# ByteHouse CE notes

这份文档承接历史 `flink-template-bytehouse-ce` 中的“参数说明/误区说明”，供 `flink-sql/assets/bytehouse-ce.md` 的模板配套参考。

## 依赖准备

使用 Flink SQL 方式，需要安装与 Flink 版本匹配的 ByteHouse CE SQL connector jar。

历史说明中的 Maven 信息：

- `groupId`: `com.bytedance.bytehouse`
- `artifactId`: `flink-sql-connector-bytehouse-ce`
- `version`: `${flink-sql-connector-bytehouse-ce.version}`

## 常用参数说明（按文档归纳）

关键点：`table-name` 指每个分片上的本地表（不是分布式表名）。

- `connector`: `bytehouse-ce`（文档也提到可用 `clickhouse`）
- `database`: 目标数据库名
- `table-name`: 本地表名（local table）
- `username` / `password`: 认证信息
- `sink.buffer-flush.interval`: flush 间隔（示例 `10 second`）
- `sink.buffer-flush.max-rows`: flush 行数阈值（示例 `5000`）
- `clickhouse.cluster`: 集群名称
- `clickhouse.shard-discovery.kind`: 分片发现类型（历史提到：`SYSTEM_CLUSTERS` / `CE_GATEWAY` / `CE_API_CLUSTERS`）
- `clickhouse.shard-discovery.service.host` / `.port`: 分片发现服务 host/port
- `clickhouse.shard-discovery.address-mapping`: 分片地址映射（可达性转换）
- `bytehouse.ce.gateway.host` / `.port`: 企业版网关 host/port（按 shard discovery 方式使用）
- `sharding-strategy`: 写入分片策略（历史提到：`NONE` / `RANDOM` / `ROUND_ROBIN` / `HASH`）

## 常见误区

- 不要写成 `connector = bytehouse`
- 不要用 `url = jdbc:bytehouse://...` 直连 JDBC URL 模板替代 connector 参数集
- 不要臆造 `scan.partition.*`、`scan.fetch-size` 作为必选项
- 不要把 `table-name` 当分布式表

## 参考

- 官方文档链接汇总：`references/connectors.md`

