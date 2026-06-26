# Google 搜索广告关键词分层与数量规范（Agent 参考）

> 所属 skill：`siluzan-tso`。本文为**方案撰写参考**，**不由** `ad campaign-validate` / `ad campaign-create` 强制执行。  
> 建户 JSON 契约与 CLI 硬约束见 `assets/campaign-create-template.md`、`references/google-ads/google-ads-campaign-plan.md`。

---

## 结构数量（每广告系列 / 每广告组）

| 模块 | 规则 | 建议数量 | 示例 |
|------|------|----------|------|
| Campaign | 按产品线拆分 | 3–10 个系列（多文件 + `campaign-manifest.json`） | Payment Gateway / CRM |
| Ad Group | 一个搜索意图一组 | 每组 5–20 个词 | Payment API Integration |
| 核心词 | 高商业意图 | 每组 **5–15** | payment api pricing |
| 长尾词 | 场景明确的长 query | 每组 **10–25** | crm for manufacturing |
| Exact Match | 核心高转化 | 每组 **2–8** 条 | [stripe alternative] |
| Phrase Match | 主流量 | 每组 **3–10** 条 | "payment solution" |
| Broad Match | 少量测试 | 每组 **1–3** 条 | payment platform |
| 否定关键词 | 基础否词库 | 系列级建议 **≥20** | free / jobs / tutorial |

**写入位置（Agent 必遵，勿混放）**

| 类型 | JSON 字段 | 层级 |
| ---- | --------- | ---- |
| 正向关键词 | `campaign.AdGroupsForBatchJob[].KeywordsForBatchJob[]` | 广告组 |
| 否定关键词 | `campaign.NegativeKeywordsForBatchJob[]` | **系列**（非 KeywordsForBatchJob 内） |

方案 Markdown 的「关键词矩阵」→ 前者；「系列级补充否定词 / 账户级否定词表」→ 后者（账户级列表另在 Google 后台应用）。**禁止**把否词抄进正向 `KeywordsForBatchJob`。`ad campaign-validate` 会对常见否词词根误填给出 warnings。

| 品牌系列 | 独立 Campaign | manifest `role: brand` | company crm |
| 竞品系列 | 独立 Campaign | manifest `role: competitor` | stripe alternative |
| Search Terms | 运营节奏 | 每周检查 | `ad search-terms` |

### 初始匹配类型占比（按组内词条数）

| 匹配类型 | 占比    | 用途     |
| -------- | ------- | -------- |
| Exact    | 30%–40% | 控制 ROI |
| Phrase   | 50%–60% | 主流量   |
| Broad    | 10%–20% | 扩量测试 |

关键词写入 JSON 的 **`campaign.AdGroupsForBatchJob[].KeywordsForBatchJob`**（`MatchTypeV2` + `KeywordText` 词面）；无顶层 `KeywordRecommendationsV2` 字段。

---

## 核心词生成规则

| 类型     | 规则                     | 示例                       |
| -------- | ------------------------ | -------------------------- |
| 产品词   | 产品 + 商业动作          | payment gateway pricing    |
| 服务词   | 行业 + company/agency    | saas marketing company     |
| 痛点词   | 问题 + solution          | reduce chargeback solution |
| 竞品词   | competitor + alternative | stripe alternative         |
| 行业术语 | 专业词汇/缩写            | merchant acquiring         |

---

## 长尾词生成规则

| 类型   | 规则                | 示例                          |
| ------ | ------------------- | ----------------------------- |
| 场景词 | 产品 + 行业场景     | crm for manufacturing         |
| 地域词 | 产品 + 国家         | payment gateway uae           |
| 技术词 | api/sdk/integration | payment sdk integration       |
| 问题词 | how to + 问题       | how to reduce failed payments |

拓词编排见 `references/analytics/keyword-planner-workflows.md`；Planner 出价见 `averageCpc` / `lowTopOfPageBid` / `highTopOfPageBid` 与根级、每条 `bidAmountCurrency`。

---

## 多系列 manifest（可选，仅组织多份 JSON）

```json
{
  "account": "<mediaCustomerId>",
  "customerName": "<mediaAccountName>",
  "campaigns": [
    { "configFile": "./campaign-generic.json", "role": "generic" },
    { "configFile": "./campaign-brand.json", "role": "brand" },
    { "configFile": "./campaign-competitor.json", "role": "competitor" }
  ]
}
```

---

## 搜索网络（`campaign-validate` / `campaign-create` 硬约束）

JSON 中必须为：

- `campaign.TargetGoogleSearch`: true
- `campaign.TargetSearchNetwork`: false
- `campaign.TargetContentNetwork`: false
- `campaign.TargetPartnerSearchNetwork`: false

否则 `campaign-validate` 报 **error**。
