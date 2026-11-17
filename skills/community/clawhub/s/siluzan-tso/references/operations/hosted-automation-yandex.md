# 宿主编排：Yandex 只读巡检

> **何时 Read**：用户要 Yandex / 直通广告自动化、巡检、熔断、封禁、拒审、落地页、超预算或空耗。Google 熔断走 `references/operations/guard.md`；Bing 走 `hosted-automation-bing.md`。
> **能做什么**：拉数、对比阈值、宿主告警。
> **不能做什么**：暂停系列/组/广告、改价、改预算。本批只读，**禁止**假装已执行熔断。

**前置**：已 `siluzan-tso login`，并用 `list-accounts -m Yandex --json-out ./snap` 确认 `mediaCustomerId`（形如 `porg-…`，**不是**纯数字，也不是 `entityId`）。

**硬约束**：

- `guard` **只支持 Google**。禁止 `guard … -m Yandex`。
- `yandex-analysis run` 是**周期报表**（默认 8 维、SEARCH、区间汇总）。当天花费、拒审、落地页、组级 CPA、全网花费走下面的**只读运营子命令**。
- 省略 `--start/--end` 时运营子命令默认**当天**（本机日历日）。`run` 省略则仍是近 7 天含今天。
- Direct **没有小时报表**。不要传 hourly，也不要编造近两小时 CPA。
- `revenue` 是成交额 PurchaseRevenue；`roi = (成交额 − 花费) / 花费`。不要用目标赋值反推。
- 默认报表路径只出现**有消耗**的对象。拒审须带 `--status`（结构查询，行内 `spend` 为 0）。
- `--status` 与 `--time-increment` **不能同时传**（400）。
- `/campaigns` `/geo` `/devices` 默认 SEARCH。全渠道花费须 `--network ALL`（行内 `network` 为 null，不拆行）。
- 自动策略与共享账户通常只有**周预算**，`budget`（日预算）常为 null。不要把周预算写进日预算字段。

---

## 1. 余额 / 账户状态

```bash
siluzan-tso yandex-analysis account-status -a <porg-xxx> --json-out ./snap-yandex
```

读 `archived`、`balance`、`currency`、`balanceAsOf`。`archived=true` → 宿主告警「已归档」。官方**无**封户状态与原因，不要把 `archived` 写成「因违规被封」。官方无独立额度；续航用余额 ÷ 近几日日均花费（日均走 `insights --level daily`）。CLI **不能**自动充值。

多户续航也可先扫 TSO 余额（截至昨天的日均）：

```bash
siluzan-tso balance-scan -m Yandex --threshold-days 7 --json-out ./snap-yandex
```

---

## 2. 素材拒审

```bash
siluzan-tso yandex-analysis ad-entities -a <porg-xxx> \
  --start <当天> --end <当天> --status REJECTED --json-out ./snap-yandex
```

也可 `MODERATION` / `PREACCEPTED`。合法值：`DRAFT,MODERATION,PREACCEPTED,ACCEPTED,REJECTED,UNKNOWN`。空列表 = 成功且没有未归档拒审，不是失败。已归档素材不会出现。命中 → 告警 `adId` / `campaignId` / `status` / `statusClarification`。

---

## 3. 落地页死链

```bash
siluzan-tso yandex-analysis ad-entities -a <porg-xxx> \
  --start <当天> --end <当天> --json-out ./snap-yandex
```

读每条广告的 `landingUrls`（数组）。空数组 **不要**当死链（Dynamic / Smart / Shopping 或仅 `TurboPageId` 常为 `[]`）。CLI **不**发 HTTP。宿主对非空 URL 做 HEAD/GET，4xx/5xx 或超时 → 告警。扫在投、含 0 消耗素材用 `--status ACCEPTED`（该路径不带花费）。

---

## 4. 当日超预算（只预警，不暂停）

全渠道当日花费 + 周预算（官方常无系列日预算）：

```bash
siluzan-tso yandex-analysis campaign-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start <当天> --end <当天> --time-increment 1 --network ALL
```

用同一 `campaignId` 看 `spend` 对 `weeklyBudget`（点击策略、投放天数 ≥ 3 时，单日大约最多花到周预算的 35%）。`budget` 仍是系列日预算，自动策略下通常为 null。命中 → **告警P1**，不要写「已暂停」。

---

## 5. CPA / 空耗（只预警，不降价、不暂停）

近 3 日组级转化成本（无小时维度，不要编造近两小时）：

```bash
siluzan-tso yandex-analysis adgroup-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start <今天-2> --end <今天>
```

对照 `conversions`、`costPerConversion`、`campaignTargetCpa`。`conversions <= 0` 时通常不判 CPA。有目标价时可用 `costPerConversion > campaignTargetCpa × 1.5` 作为飙升参考。没有目标价不算读取失败。`campaignStrategy` 只说明策略类型。

当日空耗（组 / 广告）：

```bash
siluzan-tso yandex-analysis adgroup-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start <当天> --end <当天> --time-increment 1
siluzan-tso yandex-analysis ad-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start <当天> --end <当天> --time-increment 1
```

有花费、无转化 → 告警「空耗预警」，文案不要写成「已熔断」。连续天数由宿主按日统计。

---

## 6. 花费异动 / 广告效果 / A/B / 根因

按日花费环比（前天～今天）：

```bash
siluzan-tso yandex-analysis insights -a <porg-xxx> --json-out ./snap-yandex \
  --level daily --start <前天> --end <今天>
```

差广告 / A/B（同一份广告列表，按 `adId` 比 `spend` / `ctr` / `conversions` / `roi` / `costPerConversion`）：

```bash
siluzan-tso yandex-analysis ad-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start <区间起> --end <区间止>
```

高转化扩量（组绩效 + 关键词搜索出价；自动策略下看系列周预算，不要按手动 CPC 改价）：

```bash
siluzan-tso yandex-analysis adgroup-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start <区间起> --end <区间止>
siluzan-tso yandex-analysis insights -a <porg-xxx> --json-out ./snap-yandex \
  --level keywords --start <区间起> --end <区间止>
```

异动根因（地域与设备须分别请求；全网加 `--network ALL`）：

```bash
siluzan-tso yandex-analysis insights -a <porg-xxx> --json-out ./snap-yandex \
  --level geo --start <S> --end <D> --network ALL
siluzan-tso yandex-analysis insights -a <porg-xxx> --json-out ./snap-yandex \
  --level devices --start <S> --end <D> --network ALL
```

`/geo` 有 `limit`（默认 100）。截断后的地域 `spend` 合计通常低于全网，不宜直接拿去对 `/devices`。

---

## 7. 周期报告与多账户（给人看，不代替巡检告警）

```bash
siluzan-tso accounts-digest -m Yandex --start <S> --end <D> --json-out ./snap-yandex
siluzan-tso yandex-analysis -a <porg-xxx> --start <S> --end <D> --json-out ./snap-yandex
```

`accounts-digest` / `balance-scan` 的消耗截至**昨天**。出 HTML 按 `report-templates/yandex-period-report.md` 写 narrative 后再 `yandex-analysis render`。阈值告警仍走上面 1–6 步。

---

## 做不到（勿编造命令）

| 场景            | 现状                                      |
| --------------- | ----------------------------------------- |
| 账户封禁原因    | 无；只能读 `archived`                     |
| 小时花费 / 小时 CPA | 无；改用按日或近 3 日区间              |
| 自动暂停 / 改价 / 改预算 | 无写接口；告警后人工在 Yandex 后台处理 |
