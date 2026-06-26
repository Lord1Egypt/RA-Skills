# conversation_analysis Prompt Template

你正在为 WotoHub 邮件回复场景生成 **conversation_analysis JSON**。

你的任务不是直接随意写回复，而是：
1. 先阅读完整历史邮件往来
2. 输出结构化分析
3. 再给出可以直接发送的回复主题和正文

你必须严格遵守：
- 输出必须是 **JSON**，不要输出 markdown、解释、前后缀
- JSON 结构必须符合 `references/conversation-analysis-schema.md`
- 必须基于完整历史，不可只基于最后一封邮件
- 如果信息不确定，写进 `openQuestions`，不要编造事实
- `replyBody` 必须是可直接发送的完整邮件正文，不要只给提纲

---

## 输入结构

你将收到一个 JSON，通常包含：

```json
{
  "items": [
    {
      "replyId": 12345,
      "chatId": "chat_xxx",
      "bloggerId": "besId_xxx",
      "bloggerName": "haven",
      "thread": [
        {
          "type": 2,
          "subject": "Collab idea",
          "cleanContent": "Hi ...",
          "createTime": "2026-03-26 09:00:00"
        },
        {
          "type": 1,
          "subject": "Re: Collab idea",
          "cleanContent": "What is the budget?",
          "createTime": "2026-03-26 09:20:00"
        }
      ]
    }
  ]
}
```

其中：
- `type=1`：对方来信
- `type=2`：我方发信

---

## 输出要求

输出格式：

```json
{
  "items": [
    {
      "replyId": 12345,
      "chatId": "chat_xxx",
      "bloggerId": "besId_xxx",
      "bloggerName": "haven",
      "conversationStage": "pricing_negotiation",
      "latestIntent": "asking_price",
      "latestIncoming": "The creator asks for pricing and deliverables.",
      "lastIncoming": "The creator expressed interest in the product.",
      "lastOutgoing": "We introduced the product and proposed a collaboration.",
      "resolvedPoints": ["creator is interested"],
      "openQuestions": ["budget range", "deliverable count"],
      "riskFlags": ["price_sensitive"],
      "tone": "warm-professional",
      "recommendedStrategy": "Answer pricing clearly and ask which deliverable format the creator prefers.",
      "avoidances": ["Do not repeat the full product intro"],
      "subject": "Re: Collaboration Opportunity",
      "replyBody": "Hi haven, ...",
      "cta": "Let us know which option fits you best.",
      "nextStep": "Wait for creator confirmation"
    }
  ]
}
```

---

## 分析规则

### 1. conversationStage 判断
优先从完整对话判断当前阶段：
- `first_response`
- `product_question`
- `pricing_negotiation`
- `sample_shipping`
- `deliverable_alignment`
- `collaboration_confirm`
- `follow_up`
- `soft_rejection`
- `hard_rejection`
- `closed`

### 2. latestIntent 判断
用最贴近当前来信的意图：
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

### 3. 回复生成原则
- 如果对方问价格，优先回答价格，不要继续泛泛介绍产品
- 如果对方问样品/物流，优先回应发货与流程
- 如果已经明确合作意向，回复要推进下一步，不要退回到“你是否有兴趣”
- 如果对方明显拒绝，不要强推；回复应礼貌收尾
- 如果历史里某个问题已经回答过，不要重复提问

### 4. tone 选择
只用以下值之一：
- `warm-professional`
- `friendly-concise`
- `sales-soft`
- `negotiation-clear`
- `supportive`
- `closure-polite`

---

## replyBody 写作要求

- 必须自然、简洁、可直接发送
- 基于上下文延续对话，不要像首次开发邮件
- 回应对方当前问题
- 保留适度推进感（CTA）
- 不要编造价格、物流、合作条款等未提供事实
- 如果事实不足，可用保守表达，例如：
  - "I’d be happy to align on the exact scope and budget range with you."
  - "We can confirm the shipping details based on your location and preferred timeline."

---

## 输出检查清单

输出前请自查：
1. 是否纯 JSON
2. 是否每条都含 `replyId` 或 `chatId`
3. 是否包含 `conversationStage`
4. 是否包含可直接发送的 `replyBody`
5. 是否基于完整历史，而不是只复述最后一封邮件
