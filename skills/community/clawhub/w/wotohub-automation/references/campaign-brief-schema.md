# Campaign Brief Schema

## 目标

`campaign brief` 用来把搜索、推荐、邮件生成、批量发送串成一条轻量且稳定的主链路，减少字段在多步骤间漂移。

核心原则：
- 语义理解优先交给宿主模型层
- 执行动作优先交给脚本层
- 只要求最小必要字段，缺什么补什么

---

## 最小必填字段

进入邮件生成前，至少需要：

```json
{
  "product": {
    "productName": "string"
  },
  "outreach": {
    "senderName": "string",
    "offerType": "sample | paid | affiliate"
  }
}
```

---

## Canonical 结构

```json
{
  "product": {
    "productName": "string",
    "brandName": "string",
    "sellingPoints": ["string"],
    "productType": "string",
    "targetMarket": "string",
    "language": "en"
  },
  "search": {
    "platform": "tiktok",
    "regions": ["us"],
    "languages": ["en"],
    "keywordHints": ["string"],
    "categoryHints": ["string"]
  },
  "outreach": {
    "senderName": "string",
    "offerType": "sample",
    "deliverable": "string",
    "compensation": "string",
    "ctaGoal": "string"
  },
  "meta": {
    "source": "merged",
    "confidence": "medium"
  }
}
```

---

## 字段说明

### `product`

- `productName`: 产品名，邮件生成阶段必填
- `brandName`: 品牌名，可选
- `sellingPoints`: 核心卖点列表，推荐 1-5 条
- `productType`: 产品类型或大类
- `targetMarket`: 目标市场，可选
- `language`: 默认邮件语言，默认 `en`

### `search`

- `platform`: 搜索平台，默认 `tiktok`
- `regions`: 地区代码列表，如 `["us"]`
- `languages`: 语言代码列表，如 `["en"]`
- `keywordHints`: 搜索关键词提示
- `categoryHints`: 类目提示，供模型/脚本辅助使用

### `outreach`

- `senderName`: 邮件署名，邮件生成阶段必填
- `offerType`: 合作方式，`sample | paid | affiliate`，邮件生成阶段必填
- `deliverable`: 希望达人产出的内容形式
- `compensation`: 报酬说明，敏感场景建议人工确认
- `ctaGoal`: 希望邮件推动的下一步

---

## 选择语义

邮件生成 / 发信前，必须有明确选择语义，但不要求一定是人工逐个点选。

支持两类：

1. 人工选择型
   - `selected_blogger_ids`
   - `selected_ranks`
   - 适合一次性执行

2. 规则选择型
   - `all_search_results_selected=true`
   - `selection_rule={"type":"all_search_results"}`
   - `selection_rule={"type":"top_n","topN":20}`
   - 适合定时任务 / scheduler，执行时再展开为本轮明确名单

原则：
- `send_email` 只认本轮明确名单，不在执行层临时脑补目标
- 定时任务保存的是选择规则，不是某次执行时的人名单

## 推荐使用节奏

1. 先完成产品分析和搜索推荐
2. 明确目标选择语义（人工名单或规则）
3. 若缺 `productName` / `senderName` / `offerType`，只追问这几个缺口字段
4. 由宿主模型层优先生成 outreach drafts
5. 脚本层只负责标准化、校验、批量发送和状态记录

---

## 轻量补齐模板

```text
请直接补齐下面这几个字段（没有的留空也行，我会继续接着补）：
* productName:
* senderName:
* offerType:
```
