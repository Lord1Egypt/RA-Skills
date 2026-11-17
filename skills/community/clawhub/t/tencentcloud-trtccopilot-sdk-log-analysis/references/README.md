# References

本目录存放 Agent 阅读用的日志分析经验文档，按两层组织：

## 平台模式文档（日志格式/字段/基础模式）

| 文档 | 适用范围 |
|---|---|
| `web-log-patterns.md` | Web 端 TRTC 日志 |
| `native-log-patterns.md` | Native（LiteAV）日志基础模式 |
| `miniprogram-log-patterns.md` | 微信小程序日志 |
| `audio-troubleshooting.md` | 跨平台音频症状速查 |
| `im-xlog-patterns.md` | IM SDK xlog Title 锚点速查（登录/消息/群组/信令） |

## TRTC 深度诊断知识（按问题类型路由）

| 文档 | 内容 |
|---|---|
| `trtc-analysis-playbook.md` | **分析总决策树**：症状 → 搜索关键字 → 根因（无声/回声/黑屏/卡顿/卡死/掉线/进房失败/退房超时/反压级联鉴别） |
| `trtc-deep-log-patterns.md` | Native 深度日志模式库：13 个真实案例模式（蓝牙 HFP 慢放、美颜反压级联、DirectShow ANR、192kHz AEC 溢出等） |
| `trtc-audio-diagnostics.md` | Windows 音频模块诊断链路（WASAPI / AudioIOWatchdog / HRESULT 速查） |
| `trtc-screen-share-diagnostics.md` | 屏幕分享诊断链路（状态机 / 黑屏因果链 / is_started_ 残留） |
| `trtc-known-issues.md` | 已知问题速查 36 条（私有化进房失败、NVENC、DShow 泄露、隐藏接口等） |
| `trtc-sdk-versions.md` | SDK 版本发布历史与版本号平台识别 |
| `trtc-product-concepts.md` | 产品概念（UserSig / RoomID / 房间生命周期 / 互踢 / 防火墙白名单 / 日志路径） |
| `trtc-event-id-mapping.md` | 监控/上报事件 ID 反查字典 |
| `sdk-crash-analysis.md` | Native crash 符号化分析（addr2line / IDA / WinDbg） |

---

机器消费的接口 JSON 数据不要放这里，统一放在 `../data/api/`：

- `data/api/log-rule.json`
- `data/api/timeline.json`
- `data/api/error-code.json`
