# 宿主编排：三类 Google 投放自控（详细步骤）

> **主题索引**：[`references/operations/hosted-automation-scenarios.md`](references/operations/hosted-automation-scenarios.md)
> **编排责任**：定时、多条件 IF、滑动时间窗、通知（含 P1 /「空耗熔断」文案）由 **OpenClaw / WorkBuddy / Cron** 等宿主实现。
> **本页责任**：说明如何用 `siluzan-tso` **拉检查项**、**执行最终写操作**、**写后复核**。
> Bing / Yandex / TikTok / Facebook **没有**本页写操作，只读巡检见 `hosted-automation-bing.md` / `hosted-automation-yandex.md` / `hosted-automation-tiktok.md` / `hosted-automation-facebook.md`。

## Contents

- 通用约定
- 场景 1：单日预算熔断（Campaign）
- 场景 2：CPA 飙升自动降价（Campaign / Ad Group）
- 场景 3：连续空耗自动暂停（Ad Group / Ad）
- 宿主编排实现清单（摘要）
- 与 `forewarning` 的关系

---

**必读交叉引用**：

- 金额与展示：`references/google-ads/google-ads.md` § Gotchas（金额单位）；**`ad campaigns --json-out` 的 `budget` 已为元**；组级 `*Display` 见 `ad groups` 的 `--json-out` 说明。
- `--json-out` 与 Node 过滤：`references/core/tips.md`
- 写命令语法：`references/google-ads/google-ads.md`（系列编辑、广告组编辑、启停等）
- 账户/维度分析、时间窗：`references/analytics/account-analytics.md`
- **异常监控**（余额、小时花费、落地页、拒审等 **`--json-out` 落盘 JSON 键名**）：[`references/operations/hosted-automation-monitoring-json.md`](references/operations/hosted-automation-monitoring-json.md)

**前置**：已 `siluzan-tso login`，并已用 `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap` 确认账户与 `mediaCustomerId`。

---

## 通用约定

### 统计日与「今日」

「今日累计」口径须与宿主配置一致。默认建议 **账户业务日 `Asia/Shanghai`** 的日历日；若宿主使用 UTC 或其他时区，须在配置中固定并在以下命令的 `--start` / `--end` 中显式换算为 **`YYYY-MM-DD`**，**不要**在文档未约定时自行假设。

### 检查项常用 JSON 字段（以当次 `siluzan-tso … --json-out ./snap` 为准）

| 检查意图               | 可关注的 JSON 字段（键名以实际 stdout 为准）                                                                                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **区间合计费用**       | 系列/组/创意列表中的 **`spend`** = **`--start`～`--end` 整段合计**（**不是**「一天的消耗」；窗口 7 天则约为 7 日之和）                                                                          |
| **日预算**             | **`ad campaigns --json-out ./snap`** 的 **`budget`**（CLI 已为元）= **每日预算上限**，与 `spend` **量纲不同**                                                                                   |
| 日预算与「当日」费用比 | **仅当** `--start` 与 `--end` 为**同一统计日**时，才可用 `spend` 对比 `budget`；**禁止**用多日 `spend` 去除以或对比日预算（会把周/月合计误当成「一天花了这么多」）                              |
| 转化次数               | **`conversions`**（窗口内合计）                                                                                                                                                                 |
| 实际 CPA               | 宿主侧 **`spend / conversions`**（同窗口合计；`conversions` 为 0 时不做 CPA 判断）                                                                                                              |
| 目标 CPA（系列 / 组）  | 系列列表 JSON 的 **`targetCpaAmountYuan`**（元）；组列表 **`targetCpaAmountYuan`**。不要读系列上的 `targetCpa_BidingAmount`（分） |
| 日均消耗（续航用）     | 用 `balance-scan` 的 **`dailySpend`**（近 7 日合计/7），或自算 `spend / 活跃天数`；**禁止**把多日 `spend` 直接当「日消耗」                                                                      |

> **硬约束（自动化 / 预警必读）**：凡带 `--start` / `--end` 的读命令，返回的 `spend` / `impressions` / `clicks` / `conversions` 均为**该闭区间合计**。要「一天的消耗」必须 `start=end=该日`，或显式 `合计 ÷ 天数`；要「日均」用 `balance-scan.dailySpend` / `overview.averageDailyCost`。

若某条检查所需字段在**当前**落盘 JSON 中不存在，**禁止猜测**：先换用 `references/analytics/account-analytics.md` 中其它子命令拉数，或与维护方确认是否需扩展 `siluzan-tso`；宿主侧不得编造字段。

---

## 场景 1：单日预算熔断（Campaign）

**业务目标**：当**当日**系列花费相对**日预算**达到设定比例（如 **≥ 110%**，建议 **110%–120%** 缓冲 API 延迟）时，**将系列状态置为 Paused**；恢复由人工加预算后在网页或 CLI 再启用。

### 首选（全户 / 多户 Google）

一条命令扫描名下 Google 户并交付命中表（**只读，不暂停**）：

```bash
siluzan-tso guard budget-circuit -m Google --date <当日YYYY-MM-DD> --ratio 1.1 --json-out ./snap-guard
# 确认某条命中后，对该账户单独暂停（写审计记这一次）：
siluzan-tso ad campaign-status -a <mediaCustomerId> --id <campaignId> --status Paused --commit "超预算熔断"
```

参数与落盘字段见 **`references/operations/guard.md`**。**禁止** `list-accounts` 六媒体循环 + 逐户 `ad campaigns`。

### 单户排障（可选细粒度）

1. 解析 `mediaCustomerId`（见上文前置）。
2. 拉系列列表（**必须** `--start` = `--end` = **当日**统计日；**禁止**用默认近 7 天窗口做本场景）：

```bash
siluzan-tso ad campaigns -a <mediaCustomerId> --start <当日YYYY-MM-DD> --end <当日YYYY-MM-DD> --json-out ./snap
```

3. 对 `items[]` 中每条系列（`id` 为系列 ID）：
   - 读取 **`spend`**（= **仅当日**合计费用）与 **`budget`**（**日预算**，元）。
   - 计算阈值：`threshold = budget * (coefficient / 100)`，系数 `coefficient` 建议 **110–120**（配置项）。
   - **IF** `spend >= threshold` **且**宿主策略允许对该系列熔断（如排除白名单），则进入写操作。
   - **禁止**：`--start`≠`--end` 时仍用 `spend` 对比 `budget`（会把多日合计误判成单日超预算）。

### 最终操作（单户手写时）

```bash
siluzan-tso ad campaign-status -a <mediaCustomerId> --id <campaignId> --status Paused
```

### 写后复核

```bash
siluzan-tso ad campaigns -a <mediaCustomerId> --start <当日> --end <当日> --json-out ./snap
```

确认该 `id` 的 **`statusV2`**（或等价状态字段）为 **`Paused`**。

### 恢复

```bash
siluzan-tso ad campaign-status -a <mediaCustomerId> --id <campaignId> --status Enabled
```

### CLI 能力摘要

| 状态 | 说明                                                                               |
| ---- | ---------------------------------------------------------------------------------- |
| 首选 | `guard budget-circuit -m Google`（全户扫描，只读）；暂停用 `ad campaign-status`     |
| 单户 | 读：`ad campaigns --json-out`；写：`ad campaign-status`；复核：再次 `ad campaigns` |

---

## 场景 2：CPA 飙升自动降价（Campaign / Ad Group）

**业务目标**：在过去 **X 小时**（或等价滑动窗口，由宿主定义）内 **`conversions ≥ 3`** 且 **实际 CPA > 目标 CPA × 飙升阈值**（如 **1.3**）时降价：

- 系列为 **tCPA**：下调 **target_cpa** 约 **10%–15%**（具体比例配置在宿主）。
- **eCPC**：下调 **cpc_bid_ceiling** 约 **15%**（系列侧多为 `ad campaign-edit --bid-ceiling` 等，见 `references/google-ads/google-ads.md`；组侧手动上限可用 **`ad adgroup-edit --max-cpc`**，策略以实际账户为准）。

### 检查项（宿主每轮执行）

1. **时间窗**：由宿主将「过去 X 小时」映射为 **`--start` / `--end`**（或按小时粒度拆多次拉取再聚合，以 `references/analytics/account-analytics.md` 与接口能力为准）。
2. **拉数**（至少覆盖费用、转化；字段以实际 JSON 为准）：
   - 系列维度：`ad campaigns … --json-out ./snap`
   - 组维度：`ad groups … --json-out ./snap`
   - 若列表不足以算「过去 X 小时」，使用 **`account-analytics`** 或报表子命令中可下到系列/组且带时间粒度的接口（见 `references/analytics/account-analytics.md`）。
3. 对候选对象：
   - `conversions`（窗口内）**≥ 3**
   - `actual_cpa = spend / conversions`（`conversions > 0`）
   - 读取 **目标 CPA**（系列：`targetCpaAmountYuan`；组：`targetCpaAmountYuan`，都是元）。`spend` 已是账户币种，与这两个字段同单位后再比。不要用 `targetCpa_BidingAmount`（分）。
   - **IF** `actual_cpa > target_cpa * spike_threshold`（如 `1.3`），则进入写操作。

### 最终操作

**系列（tCPA / 出价上限等）**：

```bash
# 所有金额参数均为「主币种金额」（如 50 表示 ¥50）；CLI 内部自动 ×100 写入「分」字段
siluzan-tso ad campaign-edit -a <mediaCustomerId> --id <campaignId> --target-cpa <新值（主币种）>
# 或 eCPC / 最大化点击上限等：
# siluzan-tso ad campaign-edit ... --bid-ceiling <主币种金额> --bidding TARGET_SPEND
```

参数与单位见 **`references/google-ads/google-ads.md`**「ad campaign-edit」金额单位说明。

**广告组**：

```bash
siluzan-tso ad adgroup-edit -a <mediaCustomerId> --id <adGroupId> --target-cpa <主币种金额>
# 或
siluzan-tso ad adgroup-edit -a <mediaCustomerId> --id <adGroupId> --max-cpc <主币种金额>
```

见 **`references/google-ads/google-ads.md`**「广告组编辑」。

写前**必须**先 **`ad groups --json-out ./snap` / `ad campaigns --json-out ./snap`** 取当前值，**读取主币种金额**：组侧读 `maxCPCAmountYuan` / `targetCpaAmountYuan`（元）；系列列表侧 `ad campaigns` 的 `budget` 也是元（与写参 `--budget` 一致）；`google-analysis campaigns-*.json` 的 `items[]` 行 `budgetAmountYuan` 同。在宿主内按主币种算新值（如下调 12%：`newYuan = round(oldYuan * 0.88 * 100) / 100`），再以主币种金额作为 `--target-cpa` / `--max-cpc` / `--budget` 传回。
**严禁** 自己再做 `÷100` / `÷1_000_000` 换算——`*Yuan` 字段已经是元，再换算就是错的。

### 写后复核

再次 **`ad campaigns --json-out ./snap`** 或 **`ad groups --json-out ./snap`**（刚改完系列/组加 `--fresh`）：

- 系列比对 `budget`、`targetSpendBidCeilingYuan`、`targetCpaAmountYuan`（已是元）。不要用 `targetSpend_BidCeilingAmount` / `targetCpa_BidingAmount`（分），也不要再 ×100。
- 组只比对 `maxCPCAmountYuan`、`targetCpaAmountYuan`。出口里没有 `maxCPCAmount` / `targetCpaAmount`。

### CLI 能力摘要

| 状态   | 说明                                                                                                                               |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| 已完成 | 系列：`campaign-edit`；组：`adgroup-edit`；检查项依赖宿主时间窗 + 多字段；若某策略字段未在 JSON 出现，须按上文「缺字段勿猜」处理。 |

---

## 场景 3：连续空耗自动暂停（Ad Group / Ad）

**业务目标**：**今日**（或约定日）累计 **`cost`（费用）≥ 目标 CPA × N`** 且 **`conversions = 0`** 时，**暂停**广告组或广告；**P1 告警 + 文案「空耗熔断」** 由宿主通知 skill 发送（本 CLI 不发送 P1）。

### 首选（全户 / 多户 Google）

```bash
siluzan-tso guard zero-conv -m Google --date <当日> --cpa-multiple 3 --level adgroup --json-out ./snap-guard
# 确认某条命中后，对该账户单独暂停；创意维加 --level ad|both --fallback-target-cpa <元>
siluzan-tso ad adgroup-status -a <mediaCustomerId> --id <adGroupId> --status Paused --commit "空耗熔断"
```

见 **`references/operations/guard.md`**。摘要文案为「空耗熔断」。

### 单户排障（可选）

1. 确定「今日」`--start` / `--end`（同场景 1 时区约定）。
2. **广告组**：

```bash
siluzan-tso ad groups -a <mediaCustomerId> --start <当日> --end <当日> --json-out ./snap
```

对 `items[]`：读取 **`spend`**（费用）、**`conversions`**；目标 CPA 来自 **`targetCpaAmountYuan`**（元）或宿主配置；计算 `limit = target_cpa * N`。

- **IF** `conversions === 0` **且** `spend >= limit`，则对该 `id` 执行组暂停。

3. **广告（创意）**级：若策略在创意维熔断：

```bash
siluzan-tso ad list -a <mediaCustomerId> --start <当日> --end <当日> --json-out ./snap
```

同样判断费用与转化；命中则 **`ad ad-status`**。

### 最终操作（单户手写时）

```bash
siluzan-tso ad adgroup-status -a <mediaCustomerId> --id <adGroupId> --status Paused
# 或
siluzan-tso ad ad-status -a <mediaCustomerId> --id <adId> --status Paused
```

### 通知（宿主）

调用组织规定的 **P1** 通道（钉钉/飞书/Slack 等），标题或正文须含 **「空耗熔断」** 及 `mediaCustomerId`、对象类型、对象 `id`、当次 `spend` / 阈值。

### 写后复核

```bash
siluzan-tso ad groups -a <mediaCustomerId> --start <当日> --end <当日> --json-out ./snap
```

确认对应 **`statusV2`** 为 **`Paused`**。

### CLI 能力摘要

| 状态 | 说明                                                                        |
| ---- | --------------------------------------------------------------------------- |
| 首选 | `guard zero-conv -m Google`                                                 |
| 单户 | 读：`ad groups` / `ad list`；写：`adgroup-status` / `ad-status`；通知：宿主 |

---

## 宿主编排实现清单（摘要）

| 步骤 | 说明                                                             |
| ---- | ---------------------------------------------------------------- |
| 1    | 配置：账户列表、系数、N、X 小时、白名单、是否自动写、通知        |
| 2    | 每轮：`list-accounts` 或固定 `mediaCustomerId` → 拉 `--json-out` |
| 3    | 宿主内算 IF（本页公式）                                          |
| 4    | 命中则调用写命令（可批量，注意 API 限速）                        |
| 5    | 每写一条即复核读；失败重试与告警由宿主处理                       |
| 6    | 审计日志建议写在宿主侧（CLI 不内置）                             |

---

## 与 `forewarning` 的关系

`siluzan-tso forewarning` 为丝路赞侧 **单条件、固定阈值、微信通知**，**不能**单独表达「预算 × 系数」「多条件 AND」等。上述三场景以 **宿主拉数 + 写命令** 为主路径；`forewarning` 仅作可选补充通知。
