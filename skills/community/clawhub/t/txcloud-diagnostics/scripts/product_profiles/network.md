# 网络类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| CLB 公网负载均衡 | `QCE/LB_PUBLIC` | `loadBalancerId` | lb-xxx | ClientConnum, ClientNewConn, ClientIntraffic, ClientOuttraffic, TotalReq, RspAvg, Http2xx, Http4xx, Http5xx, HealthRsCount, UnhealthRsCount |
| CLB 内网负载均衡 | `QCE/LB_PRIVATE` | `loadBalancerId` | lb-xxx | 同公网 CLB |
| Anycast 弹性公网 IP | `QCE/CEIP_SUMMARY` | `eip` | IP地址 | VipInpkg, VipOutpkg, VipIntraffic, VipOuttraffic |
| NAT 网关 | `QCE/NAT_GATEWAY` | `natId` | nat-xxx | OutBandwidth, InBandwidth, Conns, ConnsUsage, OutPkg, InPkg, Egressbandwidthusage, IncreasedConnNum |
| VPN 网关 | `QCE/VPNGW` | `vpnGwId` | vpngw-xxx | VpnInbandwidth, VpnOutbandwidth, VpnInpkg, VpnOutpkg, VpnAccOuttraffic |
| 专线接入 (专用通道) | `QCE/DCX` | `directConnectConnId` | dcx-xxx | InBandwidth, OutBandwidth, InPkg, OutPkg, BandRate, Indroppkt, Outdroppkt |
| 云联网 CCN | `QCE/VBC` | `CcnId` + `SRegion` + `DRegion` | ccn-xxx | OutBandwidth, InBandwidth, OutBandwidthRate, InBandwidthRate, OutDropPkg, OutDropPkgRate |
| 对等连接 | `QCE/PCX` | `peeringConnectionId` | pcx-xxx | InBandwidth, OutBandwidth, InPkg, OutPkg, PkgDrop, OutbandRate, InbandRate |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 负载均衡访问慢 | CLB | ClientConnum, ClientNewConn, ClientIntraffic, ClientOuttraffic, TotalReq, RspAvg, Http5xx |
| 后端健康异常 | CLB | HealthRsCount, UnhealthRsCount, Http5xx, RspAvg |
| NAT 连接数满 | NAT | Conns, ConnsUsage, OutBandwidth, InBandwidth, OutPkg, InPkg, Egressbandwidthusage |
| VPN 流量异常 | VPN | VpnInbandwidth, VpnOutbandwidth, VpnInpkg, VpnOutpkg |
| 专线带宽/丢包 | 专线 | InBandwidth, OutBandwidth, BandRate, Indroppkt, Outdroppkt |
| 云联网流量/延迟 | CCN | OutBandwidth, InBandwidth, OutBandwidthRate, InBandwidthRate, OutDropPkg |
| 笼统/不明确 | CLB | ClientConnum, ClientIntraffic, ClientOuttraffic, Http5xx, RspAvg |

## CCN 多维度说明

CCN 是多维度产品，需要通过 `--extra-dims` 传入额外维度：
- **地域间指标**：`--extra-dims SRegion=<源region>,DRegion=<目标region>`
- **单地域指标**：`--extra-dims SRegion=<region>`

## 注意事项

- CLB 公网用 `QCE/LB_PUBLIC`，内网用 `QCE/LB_PRIVATE`（非 `QCE/LOADBALANCE`）
- CCN namespace 是 `QCE/VBC`，需 `CcnId` + `SRegion` + `DRegion` 三维度
- 专线 namespace 是 `QCE/DCX`，dimension key 是 `directConnectConnId`
