# 数据库类

## 产品参数 — 关系型

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| CDB MySQL | `QCE/CDB` | `InstanceId` | cdb-xxx | CpuUseRate, MemoryUseRate, VolumeRate, Qps, Tps, SlowQueries, ThreadsConnected, ConnectionUseRate, BytesReceived, BytesSent, InnodbCacheHitRate, SecondsBehindMaster |
| TDSQL-C MySQL | `QCE/CYNOSDB_MYSQL` | `InstanceId` | cynosdbmysql-ins-xxx | Cpuuserate, Memoryuserate, Storageuserate, Qps, Tps, SlowQueries, Threadsconnected, Connectionuserate, BytesReceived, BytesSent, InnodbCacheHitRate, Replicationdelay |
| MariaDB | `QCE/MARIADB` | `InstanceId` + `NodeId` | tdsql-xxx | CpuUsageRate, MemHitRate, DataDiskUsedRate, DataDiskAvailable, ClientConnTotal, ConnUsageRate, RequestTotal, SelectTotal, LongQueryCount, SlaveDelay |
| SQL Server | `QCE/SQLSERVER` | `resourceId` | mssql-xxx | Cpu, UsageMemory, Storage, FreeStorage, Iops, Connections, SlowQueries, Requests, Transactions, BufferCacheHitRatio, BlockedProcesses, NumberOfDeadlocks |
| PostgreSQL | `QCE/POSTGRES` | `resourceId` | postgres-xxx | Cpu, MemoryRate, StorageRate, Qps, Tps, Connections, ConnUtilization, SlowQueryCnt, Deadlocks, SqlRuntimeAvg, XactCommit, XactRollback |
| TDSQL-C PG | `QCE/CYNOSDB_POSTGRES` | `InstanceId` | tdcpg-ins-xxx | CpuUsageRate, Memoryusagerate, StorageUsage, ReadWriteCalls, DbConnections, CacheHitRate, SqlRuntimeAvg |
| DCDB (旧版) | `QCE/DCDB` | `uuid` + `shardId` | tdsqlshard-xxx | CpuUsageRate, DataDiskUsedRate, MemHitRate, ConnActive, RequestTotal, LongQuery, SlaveDelay |
| TDSQL-H LibraDB | `QCE/TDSQL_A` | `appid` + `instanceid` + `shard` | 实例ID | CpuUseRate, MemoryRate, DiskRate, DiskUsage, Connections, SelectCount, InsertCount, BytesReceived, BytesSent |
| TBase | `QCE/TBASE` | `appId` + `clusterName` | tdpg-xxx | MaxCnConnectionRate, MaxDnConnectionRate |

## 产品参数 — NoSQL

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| Redis | `QCE/REDIS_MEM` | `instanceid` | crs-xxx | CpuUtil, MemUtil, MemUsed, Connections, ConnectionsUtil, Commands, CmdSlow, LatencyAvg, LatencyP99, InFlow, OutFlow, CmdHitsRatio, Keys, Evicted |
| MongoDB | `QCE/CMONGO` | `target` | cmgo-xxx | Qps, ClusterConn, Connper, ClusterDiskUsage, AvgAllRequestDelay, ClusterNetin, ClusterNetout, MonogdMaxCpuUsage, MongodMaxMemUsage |
| Memcached | `QCE/MEMCACHED` | `appid` + `instanceid` | 实例ID | Qps, Get, Set, Delete, Error, Latency, Usedsize, Allocsize |
| CTSDB | `QCE/XSTOR` | `account_id` + `instance_id` | ctsdbi-xxx | InsComputeCpuAvgUtil, InsDataMemAvgUtil, StorageUtil, StorageUsedBytes, TotalRequestsCnt, WritePointsCnt, LatencyReadAvgMs, LatencyWriteAvgMs |
| TcaplusDB | `QCE/TCAPLUS` | `TableInstanceId` + `ClusterId` | tcaplus-xxx | Readqps, Writeqps, Readlatency, Writelatency, Avgerror, Volume, ProxyCpuUtil, DataDiskUtil |
| KeeWiDB | `QCE/KEEWIDB` | `instanceid` | keewidb-xxx | KeeCommands, LatencyAvg, LatencyP99, Connections, KeeDataUtil, KeeDiskUtil, KeeCpuUtil, KeeKeyspaceHitUtil, KeeCmdSlow, InFlow, OutFlow |
| 向量数据库 | `QCE/VECDB` | `instance_id` / `cluster` + `node` | vdb-xxx | ClusterNodesTotalCommands, ClusterNodesAvgCpuUtil, ClusterNodesAvgMemUtil, ClusterNodesAvgDiskUsageUtil, ClusterNodesAvgCommandsTime, ClusterNodesCommandsExceptUtil |

## 产品参数 — 数据库 SaaS

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| DBbrain | `QCE/DBBRAIN` | `instanceid` + `instance_name` | 实例ID | SlowSql, DeadLock, CpuUsageFatal, SpaceUsageFatal, ReplDelay, HighActiveSession, WaitRowLock, TrxNotCommit |
| DTS | `QCE/DTS` | `replicationjobid` / `migratejob_id` / `Subscribeid` | 任务ID | DtsReplicationLag, DtsReplicationLagData, ReplicationCaptureRps, ReplicationLoadRps, MigrateLag, MigrateLagData |

## 指标决策表（通用关系型）

| 问题现象 | 推荐指标 |
|----------|---------|
| 慢查询/响应慢 | SlowQueries, Qps, Tps, CpuUseRate, MemoryUseRate, ThreadsConnected |
| 连接数满/无法连接 | ThreadsConnected, ConnectionUseRate, CpuUseRate, MaxConnections |
| CPU 高 | CpuUseRate, Qps, Tps, SlowQueries, ThreadsConnected |
| 存储满/磁盘告警 | VolumeRate, DataDiskUsedRate, StorageRate |
| 主从延迟 | SecondsBehindMaster, SlaveDelay, Replicationdelay |
| 笼统/不明确 | CpuUseRate, MemoryUseRate, Qps, SlowQueries, ThreadsConnected, VolumeRate |

## 指标决策表（Redis 专用）

| 问题现象 | 推荐指标 |
|----------|---------|
| 延迟高 | LatencyAvg, LatencyP99, Commands, CpuUtil, MemUtil |
| 内存满/驱逐 | MemUtil, MemUsed, Evicted, Keys, CpuUtil |
| 连接数满 | Connections, ConnectionsUtil, Commands, CpuUtil |
| 命中率低 | CmdHitsRatio, Commands, MemUtil |
| 慢查询 | CmdSlow, LatencyAvg, Commands, CpuUtil |
| 笼统/不明确 | CpuUtil, MemUtil, Commands, LatencyAvg, Connections, CmdSlow |

## 指标决策表（MongoDB 专用）

| 问题现象 | 推荐指标 |
|----------|---------|
| 延迟高 | AvgAllRequestDelay, Qps, ClusterConn, MonogdMaxCpuUsage |
| 磁盘满 | ClusterDiskUsage, MonogdMaxCpuUsage, MongodMaxMemUsage |
| 笼统/不明确 | Qps, ClusterConn, ClusterDiskUsage, AvgAllRequestDelay, MonogdMaxCpuUsage |

## 注意事项

- **Redis** dimension key 小写 `instanceid`（不是 `InstanceId`）
- **PostgreSQL/SQLServer** dimension key 是 `resourceId`
- **MongoDB** dimension key 是 `target`，值格式因层级而异
- **MariaDB** namespace `QCE/MARIADB`（非 `QCE/TDSQL`）
- **DCDB** namespace `QCE/DCDB`，dimension key 用 `uuid`（非 `InstanceId`）
- **TDSQL-C MySQL** 旧版 `QCE/CYNOSDB_MYSQL`，新版分布式 `QCE/TDMYSQL`，prefetch.py 自动处理
