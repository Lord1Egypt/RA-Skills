# 自动化场景

这是skill的一些结合Agent客户端可完成的自动化功能，你可以给用户介绍下面的这些内容

## 预算 & ROI 控制引擎

三条均为 **Google 宿主编排 + siluzan-tso** 路径；IF/定时/通知在宿主，命令与 JSON 以详规为准。

| 提醒名称            | 系统在后台默默帮你做什么？(自动动作)                                                                                                                                  | 文档（references）                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. 单日预算熔断     | 当日系列 **花费**相对**日预算**达到设定比例（如 ≥110%，可配 110%–120% 抗延迟）时，**暂停 Campaign**；恢复需人工加预算后再启用。                                       | [场景 1 · 单日预算熔断](operations/hosted-automation-self-control.md) · [`google-ads/google-ads.md`](google-ads/google-ads.md)（`ad campaigns`、`ad campaign-status`、预算口径） · [`core/tips.md`](core/tips.md)（`--json-out`）                                                                                                                                                                                            |
| 2. CPA 飙升自动降价 | 滑动时间窗内 **转化数**达置信阈值且 **实际 CPA** 高于 **目标 CPA×飙升比例** 时，在 **Campaign / Ad Group** 上**下调** tCPA 或 eCPC 等**出价上限**（具体策略依账户）。 | [场景 2 · CPA 飙升自动降价](operations/hosted-automation-self-control.md) · [`operations/hosted-automation-optimize-weak-downbid.md`](operations/hosted-automation-optimize-weak-downbid.md)（组/创意侧降价关停，可与宿主组合） · [`google-ads/google-ads.md`](google-ads/google-ads.md)（`campaign-edit`、`adgroup-edit`） · [`analytics/account-analytics.md`](analytics/account-analytics.md)（窗口粒度不足时的报表拉数） |
| 3. 连续空耗自动暂停 | **当日**累计 **花费 ≥ 目标 CPA×N** 且 **转化为 0** 时，**暂停**广告组或创意；宿主发 **P1** 且文案含 **「空耗熔断」**。                                                | [场景 3 · 连续空耗自动暂停](operations/hosted-automation-self-control.md) · [`google-ads/google-ads.md`](google-ads/google-ads.md)（`ad groups`、`ad list`、`adgroup-status`、`ad-status`） · [`operations/hosted-automation-monitoring-json.md`](operations/hosted-automation-monitoring-json.md)（JSON 键名勿套用 Google Ads API 官方名）                                                                                  |

**总索引**：[`operations/hosted-automation-scenarios.md`](operations/hosted-automation-scenarios.md) · **自控全文**：[`operations/hosted-automation-self-control.md`](operations/hosted-automation-self-control.md) · **金额硬规范**（展示用 `*Display` 等）：[`SKILL.md`](../SKILL.md)「金额与货币单位硬约束」。

## 异常监控与报警系统

编排（定时、HTTP 探活、通知）在宿主；**读哪些 JSON 字段、用什么命令** 以 **[`operations/hosted-automation-monitoring-json.md`](operations/hosted-automation-monitoring-json.md)** 为准（键名以当次 `--json-out` 落盘 JSON 为准，勿套用 Google Ads API 官方字段名解析本 CLI 输出）。

| 功能名称          | 监控层级 / 说明                                                                                    | CLI 检查入口（`--json-out`）                                                                                                                                                         |
| ----------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. 账户被封禁     | 账户级；与 Google `CustomerStatus` 及 `list-accounts` 的字段映射**暂不写进本 skill**，由宿主约定。 | `list-accounts`、`balance` 等见 [`accounts/accounts.md`](accounts/accounts.md)                                                                                                       |
| 2. 落地页死链强停 | URL 不可用或跳错页时暂停关联创意，避免无效消耗。                                                   | **`google-analysis --sections final-urls`**；或 **`ad list`** / **`google-analysis --sections ads`** 取落地页字段后由宿主 HTTP 校验                                                  |
| 3. 广告素材拒审   | 创意政策状态异常时告警或配合工单。                                                                 | **`ad list`** / **`google-analysis --sections ads`**：`policyApprovalStatusV2`、`approvalStatusDetails` 等（见 **[`google-ads/google-ads.md`](google-ads/google-ads.md)**）          |
| 4. 花费异动监控   | 系列或账户维度花费相对历史异常波动。                                                               | **`google-analysis --sections campaign-hour`**：按 `campaignId` + `date` + `hour` 看 **`spend`**                                                                                     |
| 5. 余额枯竭预警   | 余额过低或按日均推算续航不足。                                                                     | **`balance-scan`**（`balance`、`remainingDays`、`hitReason`、`meta`）或 **`balance`** / **`google-analysis --sections overview`**（`remainingAccountBudget`、`averageDailyCost` 等） |

## 自动优化

编排与阈值在宿主；**命令、JSON 键名、聚合与写后复核** 见 **[`operations/hosted-automation-optimize-index.md`](operations/hosted-automation-optimize-index.md)**（及链出的三份 SOP）。

| 功能名称                | 说明                                                                                                                                               | SOP                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1. 表现差广告降价/关停  | 组/创意：CTR、CPA、转化等触达后 **下调 `targetCpa` 或 `Paused`**。                                                                                 | [`operations/hosted-automation-optimize-weak-downbid.md`](operations/hosted-automation-optimize-weak-downbid.md) |
| 2. 高转化广告提价扩量   | 系列/组：ROAS 代理、预算丢失份额等触达后 **提预算 / 上调目标 CPA**。                                                                               | [`operations/hosted-automation-optimize-scale.md`](operations/hosted-automation-optimize-scale.md)               |
| 3. A/B 测试自动决出胜者 | 同组多创意：聚合后比 **CVPI / all conv** 等，**停输家**。                                                                                          | [`operations/hosted-automation-optimize-ab-winner.md`](operations/hosted-automation-optimize-ab-winner.md)       |
| 4. 异动根因自动排查建议 | 诊断报告与归因：用 `account-analytics`、报告模板等，见 [`analytics/account-analytics.md`](analytics/account-analytics.md) 与 `report-templates/`。 | （未单独拆 SOP，沿用分析文档）                                                                                   |
