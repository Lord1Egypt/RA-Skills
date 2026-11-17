# 宿主编排：文档索引

> **编排责任**：定时、多条件 IF、滑动时间窗、通知（含 P1 /「空耗熔断」文案）由 **OpenClaw / WorkBuddy / Cron** 等宿主实现。
> **CLI 责任**：单次调用给出检查与（仅 Google 具备的）写操作命令；**不**内置常驻调度或通知渠道。

按媒体选文档（本文件只做入口）。

| 文档                                                                                                                       | 内容                                                                                                                                         |
| -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| [`references/operations/hosted-automation-user-catalog.md`](references/operations/hosted-automation-user-catalog.md)       | **用户向一览**：先看这张表，每行只 Read **一个** SOP                                                                                         |
| [`references/operations/hosted-automation-self-control.md`](references/operations/hosted-automation-self-control.md)       | **Google 三类投放自控**：单日预算熔断、CPA 飙升降价、连续空耗暂停                                                                            |
| [`references/operations/hosted-automation-monitoring-json.md`](references/operations/hosted-automation-monitoring-json.md) | **Google 异常监控**落盘与读数                                                                                                                |
| [`references/operations/hosted-automation-optimize-index.md`](references/operations/hosted-automation-optimize-index.md)   | **Google 自动优化**：差素材降价/关停、高转化扩量、A/B 停输家                                                                                 |
| [`references/operations/hosted-automation-bing.md`](references/operations/hosted-automation-bing.md)                       | **Bing 只读巡检**：余额/IO、封禁、拒审、落地页、当日超预算预警、CPA/空耗预警；**不能**自动暂停/改价                                          |
| [`references/operations/hosted-automation-yandex.md`](references/operations/hosted-automation-yandex.md)                   | **Yandex 只读巡检**：归档/余额、拒审、落地页、当日超预算、CPA/空耗、按日异动；**不能**自动暂停/改价                                          |
| [`references/operations/hosted-automation-tiktok.md`](references/operations/hosted-automation-tiktok.md)                   | **TikTok 只读巡检**：封禁/余额、拒审、落地页、当日超预算、CPA/空耗、小时异动；**不能**自动暂停/改价                                          |
| [`references/operations/hosted-automation-facebook.md`](references/operations/hosted-automation-facebook.md)               | **Facebook / MetaAd 只读巡检**：封禁/余额、拒审、落地页、当日超预算、CPA/空耗、小时异动；**不能**自动暂停/改价                                |

**必读交叉引用**：

- Google 金额与写命令：`references/google-ads/google-ads.md`
- 各媒体拉数与日期限制：`references/analytics/account-analytics.md`
- 余额类命令：`references/accounts/accounts-balance-stats.md`
- `--json-out`：`references/core/tips.md`

**前置**：已 `siluzan-tso login`。Google 用 `list-accounts -m Google`；Bing 用 `-m BingV2`（数字 ID）；Yandex 用 `-m Yandex`（`porg-…`）；TikTok 用 `-m TikTok`（完整数字广告主 ID）；Facebook 用 `-m MetaAd`（数字或 `act_`）。
