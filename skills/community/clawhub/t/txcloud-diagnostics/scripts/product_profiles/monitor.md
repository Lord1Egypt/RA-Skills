# 可观测类 诊断

覆盖产品：CLS（日志服务）、APM（应用性能监控）、RUM（前端性能监控）、Prometheus

## 产品参数

| 产品 | Namespace | Dimension Key | 实例 ID 格式 |
|------|-----------|--------------|-------------|
| CLS 日志服务 | `QCE/CLS` | `TopicId` | topic-xxx |
| APM | `QCE/APM` | `serviceId` | apm-xxx |
| RUM | `QCE/RUM` | `projectId` | 项目 ID |
| Prometheus | `QCE/PROMETHEUS` | `instanceid` | prom-xxx |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 日志写入慢/丢失 | CLS | `TrafficWrite,SpeedWrite,RequestCountWrite,ErrorCountWrite` |
| 日志存储告警 | CLS | `StorageSize,IndexFlow,TrafficWrite` |
| APM 延迟高 | APM | 通过 DescribeBaseMetrics 确认可用指标 |
| 笼统/不明确 | CLS | `TrafficWrite,SpeedWrite,StorageSize,ErrorCountWrite` |

## 注意事项

- CLS 的 dimension key 是 `TopicId`（大写 T）
- Prometheus 的 dimension key 是小写 `instanceid`
