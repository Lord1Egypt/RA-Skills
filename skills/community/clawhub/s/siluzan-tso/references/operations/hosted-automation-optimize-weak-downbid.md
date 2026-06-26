# SOP：表现差广告 — 降价 / 关停（Ad Group / Ad）

> **索引**：[`operations/hosted-automation-optimize-index.md`](operations/hosted-automation-optimize-index.md)  
> **层级**：广告组与创意均可；组级用 **`ad groups`**，创意级用 **`ad list`**（或 **`google-analysis --sections ads`**，同源）。

---

## 业务目标（宿主配置化）

在约定统计窗口内：若素材/组 **引流弱**（如 CTR 显著低于同池基准）或 **转化效率差**（如实际 CPA 显著高于目标且转化次数不足），则 **下调目标 CPA** 或 **暂停**；连续多轮仍无改善时可升级为关停。具体系数、窗口天数、P2 通知文案由宿主配置。

---

## 检查项（宿主每轮）

### 1. 拉数命令

**广告组**（含目标 CPA、花费、转化等）：

```bash
siluzan-tso ad groups -a <mediaCustomerId> --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap
```

**创意**（含拒审、价值与 all conv 等）：

```bash
siluzan-tso ad list -a <mediaCustomerId> --start <YYYY-MM-DD> --end <YYYY-MM-DD> --json-out ./snap
```

（与上条等价数据源：`siluzan-tso google-analysis -a … --sections ads --start … --end … --json-out <dir>`，读目录内 **`ads.json`**。）

### 2. 聚合与常用键名

- 响应为 `items[]`（外层结构见 `wrapListJson` 约定，以当次输出为准）。
- **须按 `id` 聚合**（见索引「按日多行」）：对 `impressions`、`clicks`、`spend`、`conversions`、**`allConversions`**、**`conversionsValue`** 等同名字段做**求和**；比率在聚合后计算，例如
  - **实际 CPA**（主币种）：`spend / conversions`（`conversions == 0` 时不做 CPA 规则判断）。
  - **CTR**：聚合后 `clicks / impressions` 或与行上 **`ctr`** 口径对齐前，先确认组列表与创意列表 **`ctr` 是否均为 0–1 或均为百分比**，避免跨命令混比。

创意行上（在已部署网关、且 `skipReport` 为 false 时）常见扩展字段：

- **`allConversions`**
- **`conversionsValue`**
- **`conversionsValuePerImpression`**（可能由后端计算属性序列化；若无则宿主用 `conversionsValue / impressions` 自行计算，与索引说明一致。）

组行上常见：

- **`targetCpaAmountYuan`** / **`maxCPCAmountYuan`**（元，CLI 出口已统一；写入口径见 `google-ads/google-ads.md`）
- **`spend`**、**`conversions`**、**`impressions`**、**`ctr`**

### 3. 条件示例（仅示意，以宿主配置为准）

- **数据置信**：聚合后 **`impressions`**（或 **`clicks`**）高于配置下限再参与判定。
- **弱引流**：聚合后 CTR 低于「同池基准 × 配置比例」（基准由宿主对同类型/同系列池计算）。
- **弱转化**：**`spend / conversions`**（或 **`costPerConversion`** 与目标同口径比较）高于 **目标 CPA × 配置倍数**，且 **`conversions`** 低于配置上限。

目标 CPA：组级从 **`targetCpaAmount`** 与 `google-ads/google-ads.md` 货币单位说明读取；创意级通常需用 **`adGroupId`** 关联到对应组行再取目标。

---

## 最终操作

**下调组目标 CPA**（数值单位与 `ad groups --json-out ./snap` 一致，见 `google-ads/google-ads.md`「广告组编辑」）：

```bash
siluzan-tso ad adgroup-edit -a <mediaCustomerId> --id <adGroupId> --target-cpa <新值>
```

**暂停组或创意**：

```bash
siluzan-tso ad adgroup-status -a <mediaCustomerId> --id <adGroupId> --status Paused
# 或
siluzan-tso ad ad-status -a <mediaCustomerId> --id <adId> --status Paused
```

（`ad-status` 若需 `--start`/`--end` 见 `google-ads/google-ads.md`。）

---

## 写后复核

```bash
siluzan-tso ad groups -a <mediaCustomerId> --start <当日或下一窗> --end <…> --json-out ./snap
# 或
siluzan-tso ad list -a <mediaCustomerId> --start <…> --end <…> --json-out ./snap
```

确认 **`statusV2`**、**`targetCpaAmount`**（或创意侧父级状态）与预期一致。

---

## 通知（宿主）

命中降价/关停时走组织规定的 **P2**（或等价）通道；正文建议含 `mediaCustomerId`、对象类型、**`id`**、当次关键指标与阈值摘要。
