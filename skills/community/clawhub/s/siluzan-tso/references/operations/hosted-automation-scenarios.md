# 宿主编排（Google）：文档索引

> **编排责任**：定时、多条件 IF、滑动时间窗、通知（含 P1 /「空耗熔断」文案）由 **OpenClaw / WorkBuddy / Cron** 等宿主实现。  
> **CLI 责任**：单次调用下给出检查与写操作所需命令；**不**内置常驻调度或通知渠道。

本主题拆成下面两份子文档，按需打开（本文件只做**入口与导航**）。

| 文档                                                                                                 | 内容                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`references/operations/hosted-automation-self-control.md`](references/operations/hosted-automation-self-control.md)       | **三类投放自控**：单日预算熔断、CPA 飙升降价、连续空耗暂停；通用约定与常用 JSON 字段表；宿主编排实现清单；与 `forewarning` 的关系                                                                                                           |
| [`references/operations/hosted-automation-monitoring-json.md`](references/operations/hosted-automation-monitoring-json.md) | **异常监控巡检**：`balance-scan` / `balance` 等 **`--json-out` 落盘**；**`google-analysis --sections overview` / `campaign-hour` / `final-urls`** 与账户分析口径一致时用 **`--json-out <dir>`** 读落盘 `*.json`；拒审相关键名与命令见该文档 |
| [`references/operations/hosted-automation-optimize-index.md`](references/operations/hosted-automation-optimize-index.md)   | **自动优化（宿主编排）**：差素材降价/关停、高转化扩量、A/B 停输家 — 分文件 SOP（含 `ad list` 按日聚合、`google-analysis --sections campaigns` 等）                                                                                          |
| [`references/operations/hosted-automation-user-catalog.md`](references/operations/hosted-automation-user-catalog.md)       | **用户向一览**：预算/ROI 自控、异常监控、自动优化表格（可节选给用户；与上表互补）                                                                                                                                                           |

**必读交叉引用**（子文档内会再写一遍）：

- 金额与展示：`SKILL.md`「金额与货币单位硬约束」；`*Display` 与写入口径见 `references/google-ads/google-ads.md`
- 通用读命令 **`--json-out`** 与 Node 过滤：`references/core/tips.md`；**`google-analysis` 账户分析** 用 **`--json-out`**：`references/analytics/account-analytics.md`
- 写命令语法：`references/google-ads/google-ads.md`
- 账户/维度分析、时间窗：`references/analytics/account-analytics.md`
- 余额类命令详解：`references/accounts/accounts.md`

**前置**：已 `siluzan-tso login`，并已用 `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap` 确认账户与 `mediaCustomerId`。
