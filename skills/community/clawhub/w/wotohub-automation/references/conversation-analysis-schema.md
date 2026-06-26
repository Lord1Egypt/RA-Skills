# conversation_analysis JSON Schema

用于 WotoHub 回信场景的**模型驱动历史分析**标准输出结构。

目标：
1. 让模型先基于完整邮件往来做结构化理解
2. 再由回复预览层消费该结构生成候选回复
3. 最终由执行层或 `inbox.py reply` 发送

---

## 顶层结构

支持两种形式：

### 形式 A：单条分析

```json
{
  "replyId": 12345,
  "chatId": "chat_xxx",
  "conversationStage": "negotiation",
  "latestIncoming": "...",
  "lastOutgoing": "...",
  "lastIncoming": "...",
  "subject": "Re: Collaboration",
  "replyBody": "Hi xxx, ...",
  "analysis": {
    "latestIntent": "asking_price",
    "resolvedPoints": ["sample accepted"],
    "openQuestions": ["budget range", "deliverable count"],
    "recommendedStrategy": "answer pricing clearly and ask for deliverable preference",
    "tone": "warm-professional"
  }
}
```

### 形式 B：批量分析（推荐）

```json
{
  "items": [
    {
      "replyId": 12345,
      "chatId": "chat_xxx",
      "conversationStage": "negotiation",
      "latestIncoming": "...",
      "lastOutgoing": "...",
      "lastIncoming": "...",
      "subject": "Re: Collaboration",
      "replyBody": "Hi xxx, ...",
      "analysis": {
        "latestIntent": "asking_price",
        "resolvedPoints": ["sample accepted"],
        "openQuestions": ["budget range"],
        "recommendedStrategy": "answer pricing clearly",
        "tone": "warm-professional"
      }
    }
  ]
}
```

---

## 字段定义

### 绑定字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `replyId` | integer/string | 推荐 | 当前待回复收件邮件 ID；优先用它和脚本匹配 |
| `chatId` | string | 推荐 | 邮件会话 ID；`replyId` 缺失时可用它匹配 |
| `bloggerId` | string | 否 | 博主 ID，便于后续发送 |
| `bloggerName` | string | 否 | 博主昵称 |

> 匹配优先级：`replyId` > `chatId`

### 对话理解字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `conversationStage` | string | 是 | 当前对话阶段，使用下方枚举 |
| `latestIntent` | string | 推荐 | 对方最新来信的核心意图 |
| `latestIncoming` | string | 推荐 | 最近一封对方来信摘要或原文精简 |
| `lastIncoming` | string | 否 | 上一封对方来信摘要 |
| `lastOutgoing` | string | 推荐 | 最近一封我方发信摘要 |
| `resolvedPoints` | array[string] | 推荐 | 已经确认/谈妥的事项 |
| `openQuestions` | array[string] | 推荐 | 尚未解决的问题 |
| `riskFlags` | array[string] | 否 | 风险点，如压价、拖延、拒绝倾向 |
| `tone` | string | 推荐 | 建议语气 |
| `recommendedStrategy` | string | 推荐 | 本次回复建议策略 |
| `avoidances` | array[string] | 否 | 本次回复不该说的话或不该重复的点 |

### 生成结果字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `subject` | string | 推荐 | 建议回复主题 |
| `replyBody` | string | 是 | 建议回复正文 |
| `cta` | string | 否 | 建议结尾推进动作 |
| `nextStep` | string | 否 | 建议下一步动作 |

### 风险与执行辅助字段（推荐）

这些字段不是最小硬要求，但强烈建议模型一并给出，方便 skill 的 deterministic risk layer 直接消费，而不是再次靠脚本猜测：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `classification` | string | 否 | 如 `pricing_discussion` / `asks_for_sample_process` / `soft_rejection` |
| `requiresHuman` | boolean | 否 | 是否建议人工复核后再发 |

### 嵌套分析字段（可选）

允许额外放一个 `analysis` 对象，便于更整洁地组织：

```json
{
  "analysis": {
    "latestIntent": "asking_price",
    "resolvedPoints": ["sample accepted"],
    "openQuestions": ["budget range"],
    "riskFlags": ["price_sensitive"],
    "recommendedStrategy": "answer pricing clearly and narrow the deliverable scope",
    "tone": "warm-professional",
    "avoidances": ["do not repeat product intro", "do not ask the same shipping question again"]
  }
}
```

脚本消费时，推荐将关键信息同时提升到顶层，降低兼容复杂度。

---

## conversationStage 枚举

推荐使用以下标准值：

- `first_response`：首次回应
- `product_question`：询问产品细节
- `pricing_negotiation`：报价/预算谈判
- `sample_shipping`：样品/发货确认
- `deliverable_alignment`：内容形式/交付要求确认
- `collaboration_confirm`：合作确认
- `follow_up`：一般跟进
- `soft_rejection`：委婉拒绝
- `hard_rejection`：明确拒绝
- `closed`：对话结束

---

## latestIntent 枚举建议

- `asking_price`
- `asking_sample`
- `asking_shipping`
- `asking_product_details`
- `asking_deliverables`
- `asking_timeline`
- `interested`
- `hesitating`
- `rejecting`
- `counter_offer`
- `confirming_collab`
- `generic_follow_up`

---

## tone 枚举建议

- `warm-professional`
- `friendly-concise`
- `sales-soft`
- `negotiation-clear`
- `supportive`
- `closure-polite`

---

## 最小可用输出

如果要极简，至少保证：

```json
{
  "items": [
    {
      "replyId": 12345,
      "chatId": "chat_xxx",
      "conversationStage": "pricing_negotiation",
      "latestIncoming": "Creator asks for pricing and deliverables.",
      "lastOutgoing": "We previously offered sample support.",
      "subject": "Re: Collaboration Opportunity",
      "replyBody": "Hi xxx, ..."
    }
  ]
}
```

---

## 推荐高质量输出

```json
{
  "items": [
    {
      "replyId": 12345,
      "chatId": "chat_xxx",
      "bloggerId": "6864357241236603910tt7a3d",
      "bloggerName": "haven",
      "conversationStage": "pricing_negotiation",
      "latestIntent": "asking_price",
      "latestIncoming": "The creator is interested and asks for budget and expected deliverables.",
      "lastIncoming": "The creator said the product looks relevant to her audience.",
      "lastOutgoing": "We introduced the product, sample support, and collaboration interest.",
      "resolvedPoints": [
        "Creator is open to collaboration",
        "Product fit has been acknowledged"
      ],
      "openQuestions": [
        "Budget range",
        "Video deliverable count",
        "Posting timeline"
      ],
      "riskFlags": [
        "price_sensitive"
      ],
      "tone": "warm-professional",
      "recommendedStrategy": "Answer pricing directly, keep scope flexible, and ask which deliverable format she prefers.",
      "avoidances": [
        "Do not repeat the full product introduction",
        "Do not ask again whether she is interested"
      ],
      "subject": "Re: Collaboration Opportunity",
      "replyBody": "Hi haven,\n\nThanks for getting back to us...",
      "cta": "Let us know which deliverable option fits you best.",
      "nextStep": "Wait for creator confirmation on pricing / deliverables"
    }
  ]
}
```

---

## 对模型的硬要求

输出时必须遵守：

1. **基于完整历史**，不是只看最后一封邮件
2. `replyBody` 必须可直接发送，不能只是提纲
3. 不要重复历史已确认事项，除非是为了确认最终方案
4. 如果对方在谈价格，优先回应价格；如果对方在问发货，优先回应发货
5. 如无法判断，宁可在 `openQuestions` 里明确不确定点，也不要臆造事实
