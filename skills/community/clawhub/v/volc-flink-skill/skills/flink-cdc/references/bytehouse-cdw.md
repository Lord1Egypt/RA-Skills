# ByteHouse CDW sink notes

## Platform constraints

- ByteHouse CDW pipeline sink currently supports Flink 1.16-volcano
- Pipeline parallelism is controlled by `pipeline.parallelism`; the Flink platform page parallelism does not take effect for this connector workflow

## Required options

- `host` 格式形如 tenant-xxxx-cn-beijing.bytehouse.ivolces.com。需要在ByteHouse控制台获取。
- `virtual-warehouse` ByteHouse 计算组
- `api-token` 账户的鉴权 token，需要在ByteHouse控制台获取。

## Common options

- `region` 固定填写 VOLCANO_PRIVATE 。
- `port` 固定填写 19000。
- `sink.mode` 默认不设置
- `sink.buffer-flush.interval` 默认 10s 。
- `sink.buffer-flush.max-rows` 默认 10000 条。
- `sink.max-retries` 默认不设置。
- `jdbc.max-retry-backoff` 默认不设置。
- `timestamp-offset` 东八区建议设置 -8h。
- `table.create.settings` 自动建表参数，按需设置。

## Timestamp offset note

对于 Flink `TIMESTAMP` / `TIMESTAMP_LTZ`，该 sink 会按 UTC 解析时间戳；常见东八区场景建议设置 `timestamp-offset: -8h`，用于修正本地时区语义。

## Auto create note

- Auto table creation is enabled by default
- For performance-sensitive large tables, prefer manual table design and tune table settings such as order by / cluster by
