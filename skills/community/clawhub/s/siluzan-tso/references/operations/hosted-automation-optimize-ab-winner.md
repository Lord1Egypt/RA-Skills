# SOP：同组多创意 A/B — 停输家、保赢家（Ad）

> **索引**：[`references/operations/hosted-automation-optimize-index.md`](references/operations/hosted-automation-optimize-index.md)

---

## 业务目标（宿主配置化）

在同一 **广告组** 内存在多条可比较的创意时，根据约定窗口内的 **转化价值效率**、**全部转化** 或宿主侧统计检验，将**明显劣势**的创意 **Paused**，保留优势创意继续投放。显著性水平、最小样本、冷却期由宿主配置。

---

## 检查项（宿主每轮）

### 1. 拉创意列表

```bash
siluzan-tso ad list -a <mediaCustomerId> --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap
```

（等价：`siluzan-tso google-analysis --sections ads …`。）

### 2. 按组筛选、按创意聚合

- 对同一 **`adGroupId`** 下的行，先按创意 **`id`** 聚合（见索引「按日多行」）：对 **`impressions`**、**`clicks`**、**`spend`**、**`conversions`**、**`allConversions`**、**`conversionsValue`** **求和**。
- **每次展现价值（聚合后）**：宿主计算

  `cvpi = (Σ conversionsValue) / (Σ impressions)`，当分母为 0 时跳过该创意判定。

若单行上已有后端提供的 **`conversionsValuePerImpression`**，在未聚合前**勿直接跨日相加**；应在聚合后用上式或按业务约定只对单日行比较。

### 3. 参与判定的最小样本（示例）

- 聚合后 **`impressions`**（或 **`clicks`**）低于配置下限的创意**不参与**胜负判定。
- 同组内「活跃且达样本」的创意 **≥ 2** 条时才进入 A/B 决策。

### 4. 统计显著性

**p 值、贝叶斯后验、序贯检验等**须由宿主实现；CLI **不提供**检验函数。可用聚合后的 **`conversions`/`clicks`** 或 **`conversionsValue`/`impressions`** 等输入自定义检验。

---

## 最终操作

对判定为 **Loser** 的创意：

```bash
siluzan-tso ad ad-status -a <mediaCustomerId> --id <adId> --status Paused
```

（若需 `--start`/`--end` 见 `references/google-ads/google-ads.md`。）

**不在此 SOP 内**：Google Ads 界面「将流量倾斜给赢家」的算法开关；宿主仅能 **停输家** 或结合人工/网页调整轮换策略。

---

## 写后复核

```bash
siluzan-tso ad list -a <mediaCustomerId> --start <当日或下一窗> --end <…> --json-out ./snap
```

确认 Loser 的 **`statusV2`** 为 **`Paused`**；Winner 仍为 **`ENABLED`**（或宿主期望状态）。

---

## 通知（宿主）

建议 **P2**：含 `mediaCustomerId`、**`adGroupId`**、输/赢 **`id`**、聚合指标摘要与判定规则版本号，便于审计。
