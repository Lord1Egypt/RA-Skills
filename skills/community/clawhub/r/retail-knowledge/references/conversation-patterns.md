# Conversation Patterns

## Context Tracking

Within a session, maintain a lightweight conversation context object:

```json
{
  "last_product": { "sku": "...", "name": "..." },
  "stated_preferences": {
    "budget_max": 500,
    "recipient": "妈妈",
    "style": "素色",
    "size": "M"
  },
  "last_policy_topic": "return",
  "pending_clarification": null
}
```

Update this context after each turn. Use it to resolve ambiguous references.

---

## Reference Resolution

### Pronoun / demonstrative resolution
| User says | Resolve to |
|-----------|-----------|
| "那款" / "刚才那个" | `last_product` |
| "它" / "这个" | last mentioned entity |
| "再来一个" | same query type, different item |
| "还有别的吗？" | expand results from last query |
| "便宜一点的" | re-run recommendation with lower budget |

### Clarification triggers
Ask one clarifying question when:
- User asks for a recommendation without enough info (no budget, no recipient, no occasion)
- Inventory query lacks a variant (size/color) that matters
- Policy query is ambiguous ("可以退吗" — what situation?)

**Clarification template:**
> "请问[missing info]，这样我能给您更精准的推荐～"

Never ask more than one clarifying question per turn.

---

## Common Multi-Turn Flows

### Flow 1: Progressive Recommendation
```
User: 有没有适合送妈妈的礼物？
Agent: [asks budget if not stated] 请问预算大概多少？
User: 500以内
Agent: [returns 3 recommendations]
User: 第二个我喜欢，有没有礼盒包装？
Agent: [checks last_product = item 2, looks up packaging variant]
User: 好的，那个有L码吗？
Agent: [checks L size for item 2]
```

### Flow 2: Policy Deep Dive
```
User: 买了可以退吗？
Agent: [clarifies] 是想了解哪种情况下退货呢？比如不喜欢、质量问题，还是尺寸不合适？
User: 尺寸不合适
Agent: [returns size-exchange policy specifically]
User: 换货要多久？
Agent: [references last_policy_topic = exchange, answers timeline]
```

### Flow 3: Comparison
```
User: A款和B款有什么区别？
Agent: [fetches both from KB, builds comparison table]
      面料：A款全棉 | B款棉麻混纺
      价格：A款¥299 | B款¥359
      适合：A款日常休闲 | B款通勤场合
User: 哪个更值？
Agent: [gives recommendation with reasoning, not just data]
```

---

## Graceful Topic Transitions

When user suddenly switches topic:
> User was asking about a jacket → suddenly asks about return policy
- Don't carry over irrelevant context
- Reset `last_product` only if it's clearly unrelated
- Keep `stated_preferences` (budget, recipient) — they may still apply

When user signals they're done:
> "好的谢谢" / "明白了" / "没问题了"
- Give a brief closing: "不客气！有任何问题随时找我 😊"
- Don't proactively suggest more topics — let the user lead

---

## Handling Ambiguity

### Ambiguous product reference
> User: "那双鞋怎么洗？" (no shoe mentioned previously)

Options:
1. If store has few SKUs: list all shoe types and ask which
2. If store has many SKUs: ask for the product name or SKU
3. If context has a shoe recently: assume and confirm

Template: "您是指[product name]吗？还是有其他款式？"

### Ambiguous policy scope
> "买了多久可以退？"

Always clarify scenario:
- 7-day no-reason return (不喜欢)
- Quality issue return (质量问题) — often longer window
- Exchange for different size (换码)

Each has different rules. Don't blend them into one vague answer.
