# 存储类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| CBS 云硬盘 | `QCE/BLOCK_STORAGE` | `diskId` | disk-xxx | DiskReadTraffic, DiskWriteTraffic, DiskReadIops, DiskWriteIops, DiskAwait, DiskSvctm, DiskUtil |
| COS 对象存储 | `QCE/COS` | `bucket` | bucket名-appid | StdStorage, TotalRequestsPs, InternetTraffic, 2xxResponse, 4xxResponse, 5xxResponse, TotalRequestLatency, RequestsSuccessRate |
| CFS 文件存储 | `QCE/CFS` | `FileSystemId` | cfs-xxx | Storage, StorageUsage, DataReadIoBytes, DataWriteIoBytes, DataReadIoLatency, DataWriteIoLatency, DataReadIoCount, DataWriteIoCount, ClientCount |
| 云 HDFS | `QCE/CHDFS` | `appid` + `filesystemid` | 文件系统ID | ApiCapacityUsed, ApiCapacityPercentUsed, ApiReadBandwidth, ApiReadRequestCount, ApiWriteRequestCount |
| GooseFSx | `QCE/GOOSEFSX` | `appid` + `clusterid` | 实例ID | GpfsFsBytesRead, GpfsFsBytesWritten, GpfsFsFreeProportion, GpfsFsReadOps, GpfsFsWriteOps |
| 日志服务 CLS | `QCE/CLS` | `uin` + `TopicId` | 日志主题ID | TrafficWrite, TrafficIndex, TotalTrafficRead, TotalStorage, Request |
| 数据万象 CI | `QCE/CI` | `appid` + `bucket` | bucket名 | ImageRequests, MediaTasks, MediaSuccessTasks, ImagesAuditingTasks, VideoAuditingTasks |
| 存储网关 CSG | `QCE/CSGFS` | `appid` + `csgid` | 网关实例ID | Cpupercentused, Rampercentused, Csgreadbytes, Csgwritebytes, CsgStatus, MetaPercentUsed |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 磁盘 IO 慢 | CBS | DiskReadIops, DiskWriteIops, DiskAwait, DiskUtil, DiskSvctm, DiskReadTraffic, DiskWriteTraffic |
| 存储桶访问慢 | COS | TotalRequestsPs, TotalRequestLatency, 4xxResponse, 5xxResponse, InternetTraffic |
| 存储桶错误多 | COS | 4xxResponse, 5xxResponse, RequestsSuccessRate, TotalRequestsPs |
| 文件系统性能 | CFS | DataReadIoBytes, DataWriteIoBytes, DataReadIoLatency, DataWriteIoLatency, StorageUsage |
| 日志写入慢/丢失 | CLS | TrafficWrite, TrafficIndex, TotalTrafficRead, Request, TotalStorage |
| 笼统/不明确 | CBS | DiskReadIops, DiskWriteIops, DiskAwait, DiskUtil |
| 笼统/不明确 | COS | StdStorage, TotalRequestsPs, InternetTraffic, 4xxResponse, 5xxResponse |

## 注意事项

- COS/CI 拉取监控数据时 Region 统一选 `ap-guangzhou`
- CBS dimension key 是小写 `diskId`
- COS dimension key 是 `bucket`（桶名称），不是实例 ID
