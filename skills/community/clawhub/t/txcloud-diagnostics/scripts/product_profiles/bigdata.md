# 数据分析类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| Elasticsearch | `QCE/CES` | `uInstanceId` | es-xxx | Status, CpuUsageAvg, CpuUsageMax, MemUsageAvg, DiskUsageAvg, DiskUsageMax, JvmMemUsageAvg, IndexSpeed, IndexLatencyAvg, SearchCompletedSpeed, SearchLatencyAvg, BulkRejectedCompletedPercent, ShardNum |
| EMR (HDFS) | `QCE/TXMR_HDFS` | `id4hdfsoverview` + `host4hdfsoverview` | emr-xxx | HdfsStatUsageRatioCapacityusedrate, CapacityTotal, CapacityUsed, NumLiveDataNodes, NumDeadDataNodes, FilesTotal, CorruptBlocks |
| 流计算 Oceanus | `QCE/TSTREAM` | `tjob_id` | 作业ID | JobRecordsInPerSecond, JobRecordsOutPerSecond, JobCpuLoad, JobLatency, JobUptime, JobServiceDelay, JobLastcheckpointduration |

> DLC、TCHouse-C/P/D、CDW PostgreSQL 等需通过 `DescribeBaseMetrics` API 动态获取指标

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| ES 集群健康/写入慢 | ES | Status, CpuUsageAvg, DiskUsageAvg, JvmMemUsageAvg, IndexLatencyAvg, BulkRejectedCompletedPercent |
| ES 查询慢 | ES | SearchLatencyAvg, SearchCompletedSpeed, CpuUsageAvg, JvmMemUsageAvg |
| EMR 存储问题 | EMR | HdfsStatUsageRatioCapacityusedrate, CapacityUsed, NumLiveDataNodes, NumDeadDataNodes, CorruptBlocks |
| Oceanus 作业异常 | Oceanus | JobCpuLoad, JobLatency, JobUptime, JobServiceDelay, JobRecordsInPerSecond, JobRecordsOutPerSecond |
| 笼统/不明确 | ES | Status, CpuUsageAvg, DiskUsageAvg, JvmMemUsageAvg, SearchLatencyAvg, IndexLatencyAvg |

## 注意事项

- ES dimension key 是 `uInstanceId`（不是 `InstanceId`）
- EMR dimension key 格式特殊（如 `id4hdfsoverview`）
