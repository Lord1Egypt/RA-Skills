# 视频服务与安全类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| 云直播 LIVE | `QCE/LIVE` | `appid` + `domain`/`streamid` | 域名/流ID | Bandwidth, Flux, Request, VideoBitrate, VideoFps, AudioBitrate |
| WAF | `QCE/WAF` | `domain` + `edition` + `instance` | waf_xxx | Access, Qps, Attack, Cc, Bot, InBandwidth, OutBandwidth, 4xx, 5xx |
| 云防火墙 CFW | `QCE/CFW` | 多维度(`edge_ip`/`natid`/`ewid`等) | 各类实例ID | InPeakBandwidth, OutPeakBandwidth, Natwanintraffic, Natwanouttraffic, Natconntrack, Vpcconntrack, BlockListHit |

> 云点播 VOD、DDoS 防护等需通过 `DescribeBaseMetrics` API 动态获取指标

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 直播带宽/卡顿 | LIVE | Bandwidth, Flux, Request, VideoBitrate, VideoFps |
| WAF 被攻击 | WAF | Attack, Cc, Bot, Access, Qps, InBandwidth, OutBandwidth |
| WAF 误拦截 | WAF | Access, 4xx, 5xx, Attack, RatioAttack |
| 防火墙带宽 | CFW | InPeakBandwidth, OutPeakBandwidth, Natwanintraffic, Natwanouttraffic, Natconntrack |
| 笼统/不明确 | WAF | Access, Qps, Attack, Cc, 4xx, 5xx |

## 注意事项

- 云直播 dimension key 按场景：上行质量用 `appid` + `streamid`，统计数据用 `appid` + `domain`
- WAF 拉取监控数据时 Region 统一选 `ap-guangzhou`
- CFW 维度较复杂：互联网边界用 `edge_ip`/`edge_region`，NAT 用 `natid`，VPC 间用 `ewid`
