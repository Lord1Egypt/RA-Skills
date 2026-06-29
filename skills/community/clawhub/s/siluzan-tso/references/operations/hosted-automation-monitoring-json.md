# 异常监控巡检：`siluzan-tso` CLI `--json-out` 落盘 JSON 键名与命令

> **主题索引**：[`references/operations/hosted-automation-scenarios.md`](references/operations/hosted-automation-scenarios.md)  
> **编排责任**：定时、HTTP 探活、通知等在宿主。本页只列 **读数命令与常见 JSON 键名**。  
> **统计日 / 时区**：与自控场景相同，见 [`references/operations/hosted-automation-self-control.md`](references/operations/hosted-automation-self-control.md)「统计日与今日」。

宿主做定时巡检时，**只以当次 CLI 落盘 JSON 键名为准**（读命令统一 **`--json-out <dir>`**，以**落盘 `*.json` 文件正文**为准；`google-analysis` 等同理）。Google Ads API 文档里的资源名（如 `billing_setup`、`account_budget`、`amount_served_micros`）**与本 CLI 输出不是同一套命名**，不要当作本仓库 JSON 的键去解析。若某键缺失，**禁止猜测**：以实际输出为准，或换用 `references/analytics/account-analytics.md` 中的其它子命令。

---

## 1. 余额枯竭 / 续航不足（多账户批扫）

**批扫（推荐）** — 命令：

```bash
siluzan-tso balance-scan -m Google [--threshold-days <n>] [--min-balance <n>] [--json-out ./snap]
```

`--json-out` 落盘后根结构常为 **`{ ok, data: { items }, meta }`**（以实际输出为准）。宿主常用字段：

| 用途                                                       | JSON 路径 / 字段名                                                                                                                                           |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 账户                                                       | `data.items[].mediaCustomerId`、`data.items[].name`、`data.items[].advertiserName`                                                                           |
| 余额（主币种金额，与平台余额接口一致）                     | **`data.items[].balance`**（由 `remainingAccountBudget` 计算而来）                                                                                           |
| 近 7 日估算日均消耗                                        | **`data.items[].dailySpend`** = 近 7 日总消耗 / 7（窗口为 **[T-7, T-1]**，即截至昨天的 7 个自然日，**不含当天**，避免拉到当天未结算数据）                    |
| 按余额÷日均估算的续航天数                                  | **`data.items[].remainingDays`** = `balance / dailySpend`（消耗过低 < `minDailySpend` 时为 `null`）                                                          |
| 建议充值额（按 `meta.thresholds.targetDaysForTopup` 目标） | **`data.items[].recommendedTopup`**                                                                                                                          |
| 命中原因（阈值逻辑）                                       | **`data.items[].hitReason`**：`low-days` \| `low-balance` \| `both`                                                                                          |
| 币种 / 状态 / OAuth                                        | `data.items[].currencyCode`、`data.items[].status`、`data.items[].invalidOAuthToken`                                                                         |
| 本轮扫描元数据                                             | **`meta`**：`scannedAccounts`、`validAccounts`、`hitCount`、`thresholds`（含 `days`、`minBalance`、`minDailySpend`、`targetDaysForTopup`）、`generatedAt` 等 |

**单账户** — 命令：

```bash
siluzan-tso balance -m Google --accounts <mediaCustomerId> --json-out ./snap
```

`items[]` 每行：**`mediaCustomerId`**、**`remainingAccountBudget`**、**`status`**、**`currencyCode`**、**`name`**（与 `references/accounts/accounts.md` 中 `balance` 说明一致）。

**账户总览（区间内的费用与日均，可与续航逻辑组合）** — 命令：

```bash
mkdir -p ./snap-monitor && siluzan-tso google-analysis -a <mediaCustomerId> --sections overview --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap-monitor
```

读 **`./snap-monitor/overview-<accountId>.json`**（具体路径见 stdout 摘要的 `writtenFiles[0]` 或 `manifest-<accountId>.json` 的 `artifacts`）。根对象常见字段：**`remainingAccountBudget`**（余额）、**`averageDailyCost`**、**`totalCost`**、**`activeDays`**、**`currencyCode`**、**`accountId`**（无 **`balance`**，网关为 0 时 CLI 已剔除）；**`currentPeriod`** / **`previousPeriod`** 为对象块，内含 **`spend`**、`impressions`、`clicks`、`conversions` 等与 `references/analytics/account-analytics.md` 总览口径一致的指标（块内还可能出现 **`currencyCode`**）。

---

## 2. 花费异动（按系列 × 日历小时）

命令：

```bash
mkdir -p ./snap-monitor && siluzan-tso google-analysis -a <mediaCustomerId> --sections campaign-hour --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap-monitor
```

读 **`./snap-monitor/campaign-hour.json`**。**根 JSON 为数组**（不是 `items` 包装）。每元素常见字段：

**`campaignId`**、**`campaignName`**、**`date`**、**`hour`**、**`spend`**、`impressions`、`clicks`、`conversions`。

宿主侧可做：同一 `campaignId` 在相邻小时或相邻日的 **`spend`** 对比、滑动均值、超阈值告警等（阈值与统计时区由宿主配置，见 [`references/operations/hosted-automation-self-control.md`](references/operations/hosted-automation-self-control.md)「统计日与今日」）。

---

## 3. 落地页 URL 收集（HTTP 探活由宿主完成）

**仅拉 URL 列表（无日期参数）**：

```bash
mkdir -p ./snap-monitor && siluzan-tso google-analysis -a <mediaCustomerId> --sections final-urls --json-out ./snap-monitor
```

读 **`./snap-monitor/final-urls.json`**。`final-urls` 为**汇总维度**，整块对象在 **`record`**（`schemaVersion 3` 起；`items` 为 `[]`）：`record` 的**键名**为网关返回的资源标识（以当次 JSON 为准），**值为字符串数组**（每个元素是一条最终到达网址）。CLI **不**代发 HTTP 请求判断 4xx/5xx；死链判定须在宿主对 URL 执行 HEAD/GET（注意频率与 robots/合规）。

**按创意行拉数**（可与拒审、启停共用一轮数据）：

```bash
siluzan-tso ad list -a <mediaCustomerId> --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap
```

`items[]` 为网关原样字段集合；落地页相关键名以当次输出为准（类型说明里常见 **`finalurl`**；亦可用 **`google-analysis --sections ads`** 列表，结构见 `references/google-ads/google-ads.md` / `references/analytics/account-analytics.md`）。命中后暂停创意用 **`ad ad-status`**（见 `references/google-ads/google-ads.md`），写后复核再次 `ad list --json-out ./snap` 看 **`statusV2`**。

---

## 4. 广告素材拒审

不依赖 `PolicyTopic` 等 API 资源名；直接读 CLI 拒审字段：**`policyApprovalStatusV2`**、**`approvalStatusDetails`**、**`statusV2`** 等。逐步说明见 **`references/google-ads/google-ads.md`**「拒审与政策」；**`ad list`** 与 **`google-analysis --sections ads`** 列表同源，任选其一做巡检。

---

## 5. 账户「封禁」与 Google 客户状态（暂不展开）

Google 客户级 **`SUSPENDED` / `CANCELED`** 与 **`list-accounts --json-out ./snap`** 中 **`status`** 的逐项对应关系**不在本页维护**；宿主若需该判定，请以内部运维约定或后续专门文档为准。
