# TOS (filesystem connector) notes

这份文档承接历史 `flink-template-tos` 中的“参数说明/踩坑说明”，供 `flink-sql/assets/tos.md` 的模板配套参考。

## 基本约定

- `path` 必须使用 `tos://<bucket>/<path>/` 形式
- 写入若希望尽快看到“完整可读文件”，通常需要：
  - 配置 rolling policy
  - 作业层开启 checkpoint（让 sink 更稳定地滚动/提交文件）

## rolling policy（写入文件滚动策略）

官方文档口径的核心参数：

- `sink.rolling-policy.file-size`: 文件大小达到阈值后滚动（默认 `128MB`）
- `sink.rolling-policy.rollover-interval`: 写入时间超过阈值后滚动（默认 `30min`）
- `sink.rolling-policy.check-interval`: 滚动条件检查间隔（默认 `1min`）

## 分区提交（可选）

当写入路径使用分区目录（如 `.../dt=2026-04-08/`）时，可考虑配置分区提交策略（例如生成 `_success`）：

- `sink.partition-commit.trigger`: `process-time` / `partition-time`
- `sink.partition-commit.delay`: 分区关闭延迟
- `partition.time-extractor.kind`: `default` / `custom`
- `partition.time-extractor.class`: 自定义抽取类（仅 `custom`）
- `partition.time-extractor.timestamp-pattern`: 分区字段组合时间戳 pattern
- `sink.partition-commit.policy.kind`: `success-file` / `custom`
- `sink.partition-commit.policy.class`: 自定义提交策略类（仅 `custom`）

## 参考

- 官方文档链接汇总：`references/connectors.md`

