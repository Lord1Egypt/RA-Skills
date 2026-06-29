# 宿主编排：自动优化（Google）— 文档索引

> **编排责任**：定时、阈值、多轮状态（如「连续 3 日未改善」）、统计检验、通知（P1/P2）由 **宿主** 实现。  
> **本组文档**：说明如何用 `siluzan-tso` **拉检查项**、**执行写操作**、**写后复核**；每条 SOP 独立成文，避免单文件过长。

| 文档                                                                                                             | 场景                                   |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| [`references/operations/hosted-automation-optimize-weak-downbid.md`](references/operations/hosted-automation-optimize-weak-downbid.md) | 表现差：组/创意 **降价或暂停**         |
| [`references/operations/hosted-automation-optimize-scale.md`](references/operations/hosted-automation-optimize-scale.md)               | 高转化：**提预算 / 上调目标 CPA** 扩量 |
| [`references/operations/hosted-automation-optimize-ab-winner.md`](references/operations/hosted-automation-optimize-ab-winner.md)       | 同组多创意：**A/B 决胜负、停输家**     |

**必读交叉引用**：`SKILL.md`（金额与 `*Display` 硬规范）、`references/google-ads/google-ads.md`（`ad campaign-edit` / `ad adgroup-edit` / `ad-status`）、`references/analytics/account-analytics.md`（日期与 **`google-analysis --json-out`**）、`references/core/tips.md`（通用 **`--json-out`** 落盘 + 读文件技巧）、[`references/operations/hosted-automation-self-control.md`](references/operations/hosted-automation-self-control.md)（统计日与时区约定）。

---

## 通用约定（三条 SOP 共用）

### 1. 统计区间

`--start` / `--end` 为 **`YYYY-MM-DD`**，与宿主业务日一致；约定见 **`references/operations/hosted-automation-self-control.md`**「统计日与今日」。

### 2. `ad list` / `ad groups` 与「按日多行」

`admanagement/v2/list`（`ad list`、`google-analysis --sections ads`）在带日期区间时，底层 GAQL 含 **`segments.date`**，**同一创意 `id` 可出现多行（一日一行）**。做「过去 7 天总展现 / 总花费 / 总转化」时，宿主须对 **`items[]` 按广告 `id`（及需要时 `adGroupId`）聚合** 后再算比率或阈值，**禁止**把未聚合的多行直接当作多条独立创意误判。

### 3. JSON 键名以当次 **`--json-out`** 落盘文件为准

下列键名为当前网关常见命名；若某键缺失，以实际 stdout 为准，勿猜测。

### 4. 写操作与复核

所有写入须遵守 **`references/google-ads/google-ads.md`** 的确认与安全约定；写后**同区间或下一统计日**再拉一次读命令核对 `statusV2`、预算、`targetCpaAmount` 等。
