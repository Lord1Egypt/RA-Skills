# CDN 与边缘平台

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| CDN | `QCE/CDN_LOG_DATA` | `domain` + `province` + `isp` | 域名 | Bandwidth, Traffic, HitTraffic, RequestTotal, HttpStatus2xx, HttpStatus4xx, HttpStatus5xx |
| ECDN 全站加速 | `QCE/DSA` | `domain` / `projectid` | 域名 | Bandwidth, FluxDownstream, RequestTotal, ProcessTime, BackOriginTotal, BackOriginFailRate, HttpStatus2xx, HttpStatus4xx, HttpStatus5xx |
| GAAP 全球应用加速 | `QCE/QAAP` | `channelId` | link-xxx | Connum, Inbandwidth, Outbandwidth, Inpacket, Outpacket, PacketLoss, Latency |
| EdgeOne | `QCE/EDGEONE_L7` | `domain` + `zoneid` | zone-xxx | HostBandwidth, HostTraffic, HostRequests, HostCacheHitRate, HostStatusCode4xxRate, HostStatusCode5xxRate, HostConnectOriginFailRate |
| ECM 边缘计算 | `QCE/ECM_BLOCK_STORAGE` | `UUID` / `diskId` | UUID/disk-xxx | DiskReadTraffic, DiskWriteTraffic, DiskReadIops, DiskWriteIops, DiskAwait, DiskUtil, DiskUsage |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| CDN 回源慢/错误 | CDN | Bandwidth, RequestTotal, HttpStatus4xx, HttpStatus5xx, HitTraffic |
| ECDN 回源失败 | ECDN | BackOriginFailRate, BackOriginTotal, RequestTotal, ProcessTime |
| GAAP 延迟/丢包 | GAAP | Latency, PacketLoss, Connum, Inbandwidth, Outbandwidth |
| EdgeOne 源站异常 | EdgeOne | HostConnectOriginFailRate, HostStatusCode5xxRate, HostBandwidth, HostRequests, HostCacheHitRate |
| 笼统/不明确 | CDN | Bandwidth, RequestTotal, HttpStatus4xx, HttpStatus5xx |

## 注意事项

- CDN/ECDN/GAAP/EdgeOne 拉取监控数据时 Region 统一选 `ap-guangzhou`
- CDN dimension key 是 `domain`，可加 `province` + `isp` 按省份运营商查询
