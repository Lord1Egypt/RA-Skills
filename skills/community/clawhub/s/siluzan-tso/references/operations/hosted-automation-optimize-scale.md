# SOP：高转化广告 — 提预算 / 上调目标 CPA 扩量（Campaign / Ad Group）

> **索引**：[`references/operations/hosted-automation-optimize-index.md`](references/operations/hosted-automation-optimize-index.md)

---

## 业务目标（宿主配置化）

在约定窗口内：系列（或策略允许的组）**转化价值相对花费**高、且存在**预算丢失展示份额**等「有量接不住」信号时，**小幅提高日预算**与/或 **上调目标 CPA**，并配合 **P1** 类通知。比例、冷却时间（避免频繁改预算触发学习期波动）由宿主配置。

---

## 检查项（宿主每轮）

### 1. 系列报表（ROAS 代理、搜索丢失份额）

```bash
mkdir -p ./snap-scale && siluzan-tso google-analysis -a <mediaCustomerId> --sections campaigns --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap-scale
```

读 **`./snap-scale/campaigns-<accountId>.json`**（具体路径见 stdout 摘要的 `writtenFiles[0]` 或 `manifest-<accountId>.json` 的 `artifacts`）。系列行在 **`items[]`**（`schemaVersion 3` 统一信封），单行关注（键名以当次落盘 JSON 为准）：

- **`conversionsValuePerCost`**（与 Google「转化价值/费用」语义一致，作 ROAS 代理）
- **`searchBudgetLostImpressionShare`**、**`searchRankLostImpressionShare`**、**`searchImpressionShare`**
- **`spend`**、**`impressions`**、**`conversions`**、**`campaignId`**、**`campaignName`**

> **说明**：**不要**仅用 `ad campaigns --json-out ./snap` 替代本步：系列列表接口未必带齐上述份额与 `conversionsValuePerCost`；扩量判据以 **`google-analysis --sections campaigns`** 为主。

### 2. 日预算与系列状态（写前读当前值）

```bash
siluzan-tso ad campaigns -a <mediaCustomerId> --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap
```

关注 **`budget`**（`ad campaigns --json-out ./snap` 下**已为元**）、**`statusV2`**、**`id`**（系列 ID），与 `SKILL.md` 金额硬规范一致后再算「+20%」等新预算。

### 3. 消耗节奏（可选）

```bash
mkdir -p ./snap-scale && siluzan-tso google-analysis -a <mediaCustomerId> --sections campaign-hour --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap-scale
```

读 **`./snap-scale/campaign-hour.json`**。行在 **`items[]`**：**`campaignId`**、**`date`**、**`hour`**、**`spend`**。宿主可做「近若干小时花费 vs 预期」的辅助条件。

### 4. 条件示例（仅示意）

- 连续 **N** 日 **`conversionsValuePerCost`** 高于宿主配置的「目标 × 倍数」。
- 且 **`searchBudgetLostImpressionShare`** 高于配置阈值（注意接口多为 **0–1 小数**，比较时与配置统一）。
- 可选：`campaign-hour` 上近端 **`spend`** 增速超过配置。

---

## 最终操作

> **金额单位（关键）**：`ad campaign-edit` / `ad adgroup-edit` 所有金额参数均为 **主币种金额**（如 `100` 表示 ¥100，支持小数 `10.5`）；CLI 内部自动 `Math.round(value × 100)` 写入「分」字段。详见 `references/google-ads/google-ads.md`「ad campaign-edit」金额单位说明。
>
> **必须先用 `*Display` 字段取主币种当前值，加减后再传回**；不要把 `budget` / `targetCpaAmount` / `maxCPCAmount` 这些"分"字段当作主币种传给 CLI。

**提高系列日预算**（在原值基础上 +10 元的写法）：

```bash
# 1) GET 取主币种当前值
CUR=$(siluzan-tso ad campaigns -a <mediaCustomerId> --json-out ./snap | node -e '...筛选 budget（元）')
# 2) 主币种 + 10
NEW=$(node -e "console.log((${CUR} + 10).toFixed(2))")
# 3) 主币种金额传回
siluzan-tso ad campaign-edit -a <mediaCustomerId> --id <campaignId> --budget ${NEW}
```

**上调系列目标 CPA**（若策略为 tCPA 等）：

```bash
siluzan-tso ad campaign-edit -a <mediaCustomerId> --id <campaignId> --target-cpa <主币种金额>
```

若策略在**组级**调目标 CPA：

```bash
siluzan-tso ad adgroup-edit -a <mediaCustomerId> --id <adGroupId> --target-cpa <主币种金额>
```

写前务必先 **`ad campaigns --json-out ./snap` / `ad groups --json-out ./snap`** 取当前值，**读取 `*Display` 字段**（主币种）后按配置比例计算，再以主币种金额传回。

---

## 写后复核

```bash
siluzan-tso ad campaigns -a <mediaCustomerId> --start <…> --end <…> --json-out ./snap
mkdir -p ./snap-scale && siluzan-tso google-analysis -a <mediaCustomerId> --sections campaigns --start <…> --end <…> --json-out ./snap-scale
```

确认 **`budget`**（元）、**`targetCpa_BidingAmount`**（或组上 **`targetCpaAmount`**）与 **`statusV2`** 符合预期。

---

## 通知（宿主）

命中扩量时走 **P1**（或等价）通道；建议含 `mediaCustomerId`、**`campaignId`**（或组 `id`）、新旧预算/目标 CPA 摘要及判据引用（如 `conversionsValuePerCost`、`searchBudgetLostImpressionShare`）。
