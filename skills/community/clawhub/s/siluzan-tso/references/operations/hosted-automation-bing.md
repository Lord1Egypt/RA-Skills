# 宿主编排：Bing（BingV2）只读巡检

> **何时 Read**：用户要 Bing / Microsoft Ads 自动化、巡检、熔断、封禁、拒审、落地页、超预算或空耗。Google 熔断走 `references/operations/guard.md`。
> **能做什么**：拉数、对比阈值、宿主告警。
> **不能做什么**：暂停系列/组/广告、改价、改预算。没有对应写命令，**禁止**假装已执行熔断。

**前置**：已 `siluzan-tso login`，并用 `list-accounts -m BingV2 --json-out ./snap` 确认 `mediaCustomerId`（数字）。

**硬约束**：

- `guard` **只支持 Google**。禁止 `guard … -m BingV2`。
- 周期报表日期**可以含昨天**；今天数据可能不完整。省略则默认截至昨天的近 7 天。含昨天/今天时不要显式传 `--return-only-complete-data true`。
- 当日花费、近两小时 CPA 必须显式传 `--aggregation Daily|Hourly`，且 `--sections` 只能是 `campaigns` / `ad-groups` / `ads`。
- Hourly 时间桶是**太平洋时区**，和北京日期可能差一天；阈值按 `timePeriod` 对齐，不要按北京日历硬切。
- 花费/转化用 `bing-analysis run --sections …`；日预算/启停状态用 `campaign-entities`。两套数据不要混成一行。

---

## 1. 余额 / 额度续航

多户先扫 TSO 余额（截至昨天的日均，**不含当天**）：

```bash
siluzan-tso balance-scan -m BingV2 --threshold-days 7 --json-out ./snap-bing
```

有插入订单（IO）的户再核对官方额度：

```bash
siluzan-tso bing-analysis insertion-orders -a <mediaCustomerId> --json-out ./snap-bing
siluzan-tso bing-analysis monthly-spend -a <mediaCustomerId> --json-out ./snap-bing
```

无 IO 时没有额度上限，只看 `monthly-spend` 与 `balance-scan`。命中续航/额度不足 → 宿主通知充值或补 IO；CLI **不能**自动充值。

---

## 2. 账户封禁

```bash
siluzan-tso bing-analysis account-status -a <mediaCustomerId> --json-out ./snap-bing
```

`status` 不是 `Active` → 宿主发 **告警P1**（账户、状态原文）。不能在 CLI 里解封。

---

## 3. 素材拒审

全账户巡检用 `bulk-ads`，**禁止**按系列循环 `ad-entities`。首次全量；下次把上次响应的 `syncTimeUtc` 原样回传做增量（最早回溯 30 天）：

```bash
siluzan-tso bing-analysis bulk-ads -a <mediaCustomerId> --editorial-status Disapproved --json-out ./snap-bing
siluzan-tso bing-analysis bulk-ads -a <mediaCustomerId> --editorial-status Disapproved --last-sync-time-utc <上次syncTimeUtc> --json-out ./snap-bing
```

`bulk-ads` 是官方异步下载，大账户可能要几分钟，适合定时任务。命中 → 告警广告 ID / 系列 / 审核状态；改创意、申诉在 Bing 后台做。

---

## 4. 落地页死链

同样用 `bulk-ads` 拉广告上的到达网址（不传 `--editorial-status` 则全量）。CLI **不**发 HTTP。宿主对 URL 做 HEAD/GET，4xx/5xx 或超时 → 告警。不要为了探活去遍历 `ad-entities`。

---

## 5. 当日超预算（只预警，不暂停）

1. 拉系列日预算：

```bash
siluzan-tso bing-analysis campaign-entities -a <mediaCustomerId> --json-out ./snap-bing
```

2. 拉**当天**花费（必须 `--aggregation Daily`，日期可含今天）：

```bash
siluzan-tso bing-analysis run -a <mediaCustomerId> --json-out ./snap-bing --sections campaigns \
  --start <当日YYYY-MM-DD> --end <当日YYYY-MM-DD> --aggregation Daily
```

3. 按同一 `campaignId` 对齐：当日花费对照 `dailyBudget`。`isSharedBudget=true` 时 `dailyBudget` 是共享总额，不要当成单系列上限。建议阈值 **110%–120%**（缓冲报表延迟）。
4. 超阈值 → 宿主告警系列名、花费、日预算。**禁止**调用 `ad campaign-status`（那是 Google 命令）。恢复加预算或暂停由人工在 Bing 后台处理。

---

## 6. CPA 飙升 / 空耗（只预警，不降价、不暂停）

近实时（近两小时或当日）用 Hourly / Daily，不要用默认周期报表冒充「今天」：

```bash
# 当日组级花费与转化
siluzan-tso bing-analysis run -a <mediaCustomerId> --json-out ./snap-bing --sections ad-groups \
  --start <当日> --end <当日> --aggregation Daily

# 近两小时（按 adGroupId 取最近两个整点相加再算）
siluzan-tso bing-analysis run -a <mediaCustomerId> --json-out ./snap-bing --sections ad-groups \
  --start <起> --end <止> --aggregation Hourly
```

宿主侧：

- 有转化：`CPA = 花费 / 转化`；超过约定目标倍数 → 告警「CPA 飙升」。
- 花费已达「目标 CPA × N」且转化为 0 → 告警「空耗预警」（文案不要写成「已熔断」）。

目标 CPA 以账户约定或系列出价策略为准；落盘里没有就不要猜。拉今天数据**不要**显式传 `--return-only-complete-data true`。

---

## 7. 多账户消耗 / 零转化巡检（截至昨天）

`accounts-digest` / `stats` 走每日同步，**今天为 0**，只适合回看已结束的日期：

```bash
siluzan-tso accounts-digest -m BingV2 --start <S> --end <D> --zero-conversions --json-out ./snap-bing
```

看当天必须走第 5、6 步的 `--aggregation` 报表。
