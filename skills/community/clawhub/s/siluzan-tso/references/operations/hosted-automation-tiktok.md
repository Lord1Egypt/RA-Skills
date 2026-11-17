# 宿主编排：TikTok 只读巡检

> **何时 Read**：用户要 TikTok 自动化、巡检、熔断、封禁、拒审、落地页、超预算或空耗。Google 熔断走 `references/operations/guard.md`。
> **能做什么**：拉数、对比阈值、宿主告警。
> **不能做什么**：暂停系列/组/广告、改价、改预算。本批只读，**禁止**假装已执行熔断。

**前置**：已 `siluzan-tso login`，并用 `list-accounts -m TikTok --json-out ./snap` 确认 `mediaCustomerId`（**完整数字广告主 ID**，界面常拆成两段，须拼完整，例如 19 位）。

**硬约束**：

- `guard` **只支持 Google**。禁止 `guard … -m TikTok`。
- `tiktok-analysis run` 是 TSO **看板周期报表**（默认截至昨天），**不要**拿它当「当天 / 小时」巡检。
- 当天花费、小时 CPA、拒审、落地页、系列预算/组出价走下面的 **TikTokAPI 子命令**。
- 「当天」按 `account-status` 返回的 `timezone` 自然日，不是服务器时区，也不是默认北京时间。
- 账户信息须**拥有**该广告主；仅列表可见会 HTTP 400。
- 不同 `DataLevel` 的 spend / conversion **不要加总到一起**。
- CBO（`budget_optimize_on`）或 `BUDGET_MODE_INFINITE` 时系列/组 `budget` 可能为 `0`，不能当熔断分母。
- `BID_TYPE_NO_BID` 没有外部出价，不要走改价逻辑。

---

## 1. 余额 / 账户状态

```bash
siluzan-tso tiktok-analysis account-status -a <mediaCustomerId> --json-out ./snap-tt
```

读 `status`、`balance`、`currency`、`timezone`。`STATUS_ENABLE` 为正常，其余（如 `STATUS_LIMIT`）→ 宿主发 **告警P1**。余额不足 → 通知充值。CLI **不能**自动充值，也**不能**解封。

多户续航也可先扫 TSO 余额（截至昨天的日均）：

```bash
siluzan-tso balance-scan -m TikTok --threshold-days 7 --json-out ./snap-tt
```

---

## 2. 素材拒审

```bash
siluzan-tso tiktok-analysis ad-entities -a <mediaCustomerId> \
  --secondary-status AD_STATUS_AUDIT_DENY --json-out ./snap-tt
```

`code == 0` 且列表为空 = 没有拒审，不是失败。须翻完页（CLI 已自动翻）。命中 → 告警 `ad_id` / 系列 / `secondary_status`。

**禁止**传 `AD_STATUS_REVIEW_PARTIALLY_APPROVED`（后台黄条，官方过滤会 40002）。黄条只能在不带过滤的 `ad-entities` 响应里读。组状态 ≠ 广告状态。

---

## 3. 落地页死链

```bash
siluzan-tso tiktok-analysis ad-entities -a <mediaCustomerId> --json-out ./snap-tt
```

读 `landing_page_url` / `landing_page_urls` / `deeplink`。默认字段集可能全空，空 URL **不要**当死链。CLI **不**发 HTTP。宿主对非空 URL 做 HEAD/GET，4xx/5xx 或超时 → 告警。Spark 看 `tiktok_item_id`，可能没有常规落地页。

---

## 4. 当日超预算（只预警，不暂停）

先看广告主时区下的当天，再打两次：系列实体 + 系列日报。

```bash
siluzan-tso tiktok-analysis campaign-entities -a <mediaCustomerId> --json-out ./snap-tt
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start <当天> --end <当天> \
  --data-level AUCTION_CAMPAIGN --dimensions campaign_id --metrics spend
```

用同一 `campaign_id` 算 `spend / budget`。`operation_status == DISABLE` 的系列跳过。CBO / 不限预算跳过（预算可能为 0）。命中 → **告警P1**，不要写「已暂停」。

---

## 5. CPA / 空耗（只预警，不降价、不暂停）

近 N 小时 CPA（起止必须同一天；跨 0 点再打昨天一条后按小时拼）：

```bash
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start <当天> --end <当天> \
  --data-level AUCTION_ADGROUP --dimensions adgroup_id,stat_time_hour \
  --metrics spend,conversion,cost_per_conversion
siluzan-tso tiktok-analysis adgroup-entities -a <mediaCustomerId> --json-out ./snap-tt
```

按 `adgroup_id` 取出最近 N 个整点，**先加总 spend / conversion 再算窗口 CPA**。不要用单小时 `cost_per_conversion`。转化为 0 时 CPA 无意义。`BID_TYPE_NO_BID` 只告警、不改价。

当日空耗（先定一层，勿把组报和广告报加在一起）：

```bash
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start <当天> --end <当天> \
  --data-level AUCTION_ADGROUP --dimensions adgroup_id --metrics spend,conversion
```

---

## 6. 花费异动 / 广告效果 / 根因

小时花费（今昨对比拆成两次请求，不要把起止写成两天）：

```bash
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start <当天> --end <当天> \
  --data-level AUCTION_CAMPAIGN --dimensions campaign_id,stat_time_hour --metrics spend
```

广告效果（CPA 用 `cost_per_conversion` 或 `spend/conversion`；**ROAS 用落盘 `roas` / `totals.roas`**）：

```bash
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start <当天> --end <当天> \
  --data-level AUCTION_AD --dimensions ad_id \
  --metrics spend,conversion,cost_per_conversion,complete_payment,ctr
```

`--metrics` 含完付/ROAS 时 CLI 自动附带 `total_purchase_value,complete_payment_roas,total_active_pay_roas`。口径对齐 Ads Manager：`complete_payment` 是网页支付完成**次数**（不是金额）；ROAS 优先官方列 `complete_payment_roas`（网页）/ `total_active_pay_roas`（App 付费），否则 `total_purchase_value/spend`。多行用 `totals`（先加总再除），**禁止**对各组 `roas` 取平均。**`complete_payment=0` 不是像素坏了**——App / `ACTIVE_PAY` 看 `total_purchase_value`。不确定优化目标时先 `adgroup-entities` 看 `optimization_event`。出价在组，广告层只能关停（本批 CLI **不**关停）。

根因分解（含小时时起止仍须同一天，必须翻完页；CLI 已自动翻）：

```bash
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start <当天> --end <当天> \
  --data-level AUCTION_CAMPAIGN \
  --dimensions campaign_id,stat_time_hour,country_code --metrics spend
```
