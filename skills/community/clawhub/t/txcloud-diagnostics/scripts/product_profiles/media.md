# 音视频类 诊断

覆盖产品：Live（直播）、VOD（点播）、TRTC（实时音视频）、GME（游戏多媒体引擎）、MPS（媒体处理）

## 产品参数

| 产品 | Namespace | Dimension Key | 实例 ID 格式 |
|------|-----------|--------------|-------------|
| 直播 Live | `QCE/LVB` | `domain` | 域名 |
| 直播 CDN | `QCE/XMCDN` | `domain` | 域名 |
| 点播 VOD | `QCE/VOD` | `domain` | 域名 |
| TRTC | `QCE/TRTC` | `sdkappid` | SDKAppID |
| GME | `QCE/GME` | `appid` | AppID |
| MPS | `QCE/MPS` | 需通过 API 确认 | 实例 ID |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 直播卡顿 | Live | `Bandwidth,OnlineNum,ReqNum,ResCode4xx,ResCode5xx` |
| TRTC 音视频质量 | TRTC | 通过 DescribeBaseMetrics 确认可用的丢包率/延迟/房间数指标 |
| 笼统/不明确 | Live | `Bandwidth,OnlineNum,ReqNum` |

## 注意事项

- 直播/CDN/VOD 的 dimension key 都是 `domain`（推拉流域名）
- TRTC 的 dimension key 是 `sdkappid`（数字 ID）
- GME 的 dimension key 是 `appid`
