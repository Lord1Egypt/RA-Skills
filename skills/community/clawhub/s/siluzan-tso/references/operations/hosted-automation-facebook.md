# 宿主编排：Facebook / MetaAd 只读巡检

> **何时 Read**：用户要 Facebook / Meta / MetaAd 自动化、巡检、熔断、封禁、拒审、落地页、超预算或空耗。Google 熔断走 `references/operations/guard.md`。
> **能做什么**：拉数、对比阈值、宿主告警。
> **不能做什么**：暂停系列/组/广告、改价、改预算。本批只读，**禁止**假装已执行熔断。

**前置**：已 `siluzan-tso login`，并用 `list-accounts -m MetaAd --json-out ./snap` 确认 `mediaCustomerId`（数字或 `act_` 均可；`balance-scan` / `stats` / `balance` 会把裸数字规范成官方 `act_` 再打 TSO）。

**硬约束**：

- `guard` **只支持 Google**。禁止 `guard … -m MetaAd`。
- `facebook-analysis run` 是 TSO **看板周期报表**（默认截至昨天），**不要**拿它当「当天 / 小时」巡检。
- 当天花费、小时 CPA、拒审、落地页、系列预算/组出价走下面的 **FacebookAPI 子命令**。
- 「当天」按 `account-status` 返回的 `timezone_name` 自然日，不是服务器时区，也不是默认北京时间。
- 结构对象的 `daily_budget` / `balance` / `spend_cap` / `bid_amount` 是**最小货币单位字符串**；Insights 的 `spend` / `cpc` / `cpm` 是**币种小数**。两套不要混除。
- CBO 系列才有 `daily_budget`。只有 `lifetime_budget`、没有日预算时，不能当单日熔断分母。
- `LOWEST_COST_WITHOUT_CAP` 或组上没有 `bid_amount` 时，不能按手动出价去改价。
- `conversions[]` / `purchase_roas[]` 是数组，接口不挑 `action_type`。算 CPA / ROAS 时由宿主自己选类型。
- hourly breakdown 与 `--time-increment` **不能同时传**（400 `VALIDATION`）。不要叠 hour × 地域。
- 列表分页只用响应里的 `paging.cursors.after`；CLI 已自动翻。禁止用 `paging.next`（已被清空，里面本来带 Graph token）。

---

## 1. 余额 / 账户状态

```bash
siluzan-tso facebook-analysis account-status -a <mediaCustomerId> --json-out ./snap-fb
```

读 `account_status`、`disable_reason`、`balance`、`spend_cap`、`amount_spent`、`currency`、`timezone_name`。`account_status == 1` 为正常，其余 → 宿主发 **告警P1**。`spend_cap` 为 `0` 或空表示未设上限。预付账户才看 `balance`。CLI **不能**自动充值，也**不能**解封。

多户续航也可先扫 TSO 余额（截至昨天的日均）：

```bash
siluzan-tso balance-scan -m MetaAd --threshold-days 7 --json-out ./snap-fb
```

---

## 2. 素材拒审

```bash
siluzan-tso facebook-analysis ad-entities -a <mediaCustomerId> \
  --effective-status DISAPPROVED --json-out ./snap-fb
```

也可 `DISAPPROVED,WITH_ISSUES`。过滤在 Graph 侧完成。列表为空 = 没有拒审，不是失败。命中 → 告警 `id` / `campaign_id` / `effective_status` / `issues_info`。

---

## 3. 落地页死链

```bash
siluzan-tso facebook-analysis ad-entities -a <mediaCustomerId> --json-out ./snap-fb
```

读每条广告的 `landing_urls`（从创意抽出）。空数组 **不要**当死链。CLI **不**发 HTTP。宿主对非空 URL 做 HEAD/GET，4xx/5xx 或超时 → 告警。Instant Form 线索广告可能没有常规落地页。

---

## 4. 当日超预算（只预警，不暂停）

先看账户时区下的当天，再打两次：系列实体 + 系列日报。

```bash
siluzan-tso facebook-analysis campaign-entities -a <mediaCustomerId> --json-out ./snap-fb
siluzan-tso facebook-analysis insights -a <mediaCustomerId> --json-out ./snap-fb \
  --level campaigns --start <当天> --end <当天> --time-increment 1
```

用同一 `campaign_id` 算 `spend / (daily_budget 换算后的主单位)`。`effective_status` 已停的系列跳过。只有 lifetime、没有日预算的跳过。命中 → **告警P1**，不要写「已暂停」。

---

## 5. CPA / 空耗（只预警，不降价、不暂停）

近两小时 CPA（组级 hourly；查询区间用 1～2 天即可）：

```bash
siluzan-tso facebook-analysis insights -a <mediaCustomerId> --json-out ./snap-fb \
  --level adsets --start <昨天> --end <今天> --breakdown hourly
siluzan-tso facebook-analysis adset-entities -a <mediaCustomerId> --json-out ./snap-fb
```

按 `adset_id` 取最近两个整点，**先加总 spend / conversions 再算窗口 CPA**。转化为 0 时 CPA 无意义。`LOWEST_COST_WITHOUT_CAP` 只告警、不改价。

当日空耗：

```bash
siluzan-tso facebook-analysis insights -a <mediaCustomerId> --json-out ./snap-fb \
  --level adsets --start <当天> --end <当天> --time-increment 1
```

花费已达「目标 CPA × N」且转化为 0 → 告警「空耗预警」，文案不要写成「已熔断」。

---

## 6. 花费异动 / 广告效果 / A/B / 根因

小时花费（同一对象 + 同一小时槽做今昨对比）：

```bash
siluzan-tso facebook-analysis insights -a <mediaCustomerId> --json-out ./snap-fb \
  --level campaigns --start <昨天> --end <今天> --breakdown hourly
```

广告效果（ROAS / CPA / CTR；`purchase_roas[]` / `cost_per_conversion[]` 自行选 `action_type`）：

```bash
siluzan-tso facebook-analysis insights -a <mediaCustomerId> --json-out ./snap-fb \
  --level ads --start <起始日> --end <结束日>
```

同组多条广告对比：Insights `--level ads` + `ad-entities --campaign-id <系列>`，按 `ad_id` 汇总后再比。本批 **不**暂停败者。

根因分解需要地域或设备时**另开一次**请求（`--breakdown country` / `device_platform`），不要和 hourly 叠在一起。
