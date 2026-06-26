# Paimon notes

这份文档承接历史 `flink-template-paimon` 中的“参数说明/最佳实践/常见问题”，供 `flink-sql/assets/paimon.md` 的模板配套参考。

## 合并引擎选择

| 场景 | 推荐 `merge-engine` | 推荐 `changelog-producer` |
|---|---|---|
| 只追加，不更新 | `deduplicate` 或不设置 | `none` |
| 根据主键更新 | `deduplicate` | `input` / `lookup` / `full-compaction` |
| 只更新部分列 | `partial-update` | `lookup` / `full-compaction` |
| 实时聚合统计 | `aggregation` | `lookup` / `full-compaction` |

## 分桶策略

- 主键表、部分列更新表、聚合表：通常建议设置 `bucket`
- Append 表：默认可不设置 `bucket`
- 历史约束：Append 表若设置 `bucket`，必须同时设置 `bucket-key`
- 经验建议：单个 bucket 存储量控制在约 `1-2GB`

常见参数：

- `bucket`: 分桶数量
- `bucket-key`: 分桶键

何时需要分桶：

- 数据量较大，需要并行读写
- 需要优化查询性能

## Changelog producer 选择

| 参数值 | 说明 | 场景 |
|---|---|---|
| `none` | 不产生 changelog | 只追加，不需要下游流读 |
| `input` | 根据上游输入生成 | 需要下游流读，但仅保留输入记录语义 |
| `lookup` | 查找模式 | 需要完整变更日志 |
| `full-compaction` | 全量压缩 | 需要完整变更日志 |

说明：`partial-update` 和 `aggregation` 在流读场景下，通常需要搭配 `lookup` 或 `full-compaction`。

## 分区策略

- 按天：`dt STRING`，格式常见 `yyyy-MM-dd`
- 按小时：`dt STRING, hh STRING`
- `metastore.partitioned-table = true`: 将分区信息同步到 LAS 元数据

注意：如果分区字段设计发生变化，通常需要清理旧表数据和旧元数据后重建。

## 常见参数优化

- 忽略删除事件：

```sql
'ignore-delete' = 'true'
```

- 非分区表行级过期：

```sql
'record-level.expire-time' = '30 d',
'record-level.time-field' = 'update_time',
```

- 分区过期：

```sql
'partition.expiration-strategy' = 'values-time',
'partition.expiration-time' = '7 d',
'partition.expiration-check-interval' = '1 d',
'partition.timestamp-formatter' = 'yyyyMMdd',
'partition.timestamp-pattern' = '$dt'
```

- 快照保留时间：

```sql
'snapshot.time-retained' = '3 d',
'snapshot.num-retained.max' = '1000',
```

- 异步文件合并：

```sql
'num-sorted-run.stop-trigger' = '2147483647',
'sort-spill-threshold' = '5',
'lookup-wait' = 'false',
```

- 上下游主键不一致时，可考虑在任务参数中关闭 upsert materialize：

```yaml
table.exec.sink.upsert-materialize: NONE
```

## 注意事项

- 必须按 `${catalog}.${db}.${table}` 三段式访问
- Append 表通常不需要主键
- 分区主键表的主键字段必须包含分区字段

## 已废弃的旧口径

以下旧参数口径不应继续在新模板中使用：

- `connector`
- `path`
- `warehouse`
- `auto-create`
- `write-mode`
- `file.format`
- `compression.format`

当前应优先使用的新参数体系：

- `bucket`
- `changelog-producer`
- `merge-engine`
- `metastore.partitioned-table`
- `fields.<field-name>.aggregate-function`
- `fields.<field-name>.sequence-group`
- `fields.<field-name>.nested-key`
- `fields.<field-name>.ignore-retract`

## 常见问题

- 验证 SQL 时出现 `org.apache.thrift.transport.TTransportException`
  - 原因：验证阶段可能暂时无法访问 LAS 元数据
  - 处理：上线时按需跳过上线前的深度检查

- 启动时报 `DatabaseNotExistException`
  - 原因：静态解析 SQL 时不会自动去 LAS 拉取已有数据库
  - 处理：在 SQL 中显式写 `CREATE DATABASE IF NOT EXISTS ...`

## 参考

- 官方文档链接汇总：`references/connectors.md`

