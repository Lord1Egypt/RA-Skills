---
name: retail-knowledge
description: >
  Product knowledge Q&A and policy lookup for retail digital employees.
  Answers customer and staff questions about products, store policies, promotions,
  FAQs, and store information using the configured knowledge base.
  Use when someone asks about: product details, specs, suitability, ingredients,
  return/exchange policy, warranty, promotions, discounts, store hours, membership,
  or any store-specific question. Triggers on: 产品信息, 商品详情, 退换货政策,
  保修政策, 活动优惠, 营业时间, 会员积分, 店铺信息, product info, store policy,
  retail knowledge, what do you sell, do you have, can I return.
metadata:
  openclaw:
    emoji: 📖
---

# Retail Knowledge — Q&A Engine

## Overview

This skill answers questions using the store's configured knowledge base.
It is the foundational skill for all retail digital employee roles.

**Depends on:** Knowledge base populated via `retail-agent-setup` Step 03.
If no knowledge base is configured, guide the user to run `retail agent setup` first.

---

## Query Routing

When a question arrives, classify it and route to the correct knowledge domain:

| Query Type | Keywords | Knowledge Domain |
|------------|----------|-----------------|
| Product info | 产品/商品/成分/规格/面料/尺寸/功效 | `products` |
| Policy | 退货/换货/退款/保修/三包/质保 | `policies` |
| Promotion | 活动/优惠/折扣/满减/赠品/促销 | `promotions` |
| FAQ | 怎么/如何/可以/能否/多久 | `faqs` |
| Store info | 地址/营业时间/几点/电话/停车 | `store_info` |
| Membership | 积分/会员/等级/VIP/余额 | `membership` |
| Recommendation | 推荐/适合/送礼/比较/哪个好 | → hand off to `product-recommender` skill |
| Inventory | 有没有/还有/库存/现货 | → hand off to `inventory-query` skill |
| Complaint | 坏了/质量问题/投诉/要退 | → hand off to `complaint-handler` skill |

---

## Answer Construction Rules

### Rule 1: Always ground answers in the knowledge base
Never invent product specs, policy terms, or promotion details.
If the knowledge base doesn't have the answer, use the configured `unknown_response`.

### Rule 2: Be specific
Bad: "我们有退货政策"
Good: "购买后7天内，商品未使用且保留吊牌，可申请无理由退货。退款将在3个工作日内到账。"

### Rule 3: Cite conditions when relevant
For policies and promotions, always mention key conditions and exceptions.
Example: "满300减50，不与其他优惠叠加，促销商品除外。"

### Rule 4: Match persona tone
Apply the configured `persona_config` (name, tone, address form, emoji usage).
**Reference:** [answer-style-guide.md](references/answer-style-guide.md)

### Rule 5: Handle unknowns gracefully
If no matching knowledge base entry exists:
1. Say so honestly (use configured `unknown_response`)
2. Offer an alternative: escalate, or suggest the user contact staff
3. Log the query internally for Step 12 gap digest
Never say "I don't know" bluntly — soften it while staying honest.

---

## Multi-Turn Conversation

Maintain context across turns within a session:
- Remember what product was mentioned earlier ("那款" / "刚才说的那个")
- Remember stated preferences ("她喜欢素色" → filter subsequent answers)
- If user backtracks or changes topic, reset context gracefully

**Reference:** [conversation-patterns.md](references/conversation-patterns.md)

---

## Knowledge Base Structure

Expect the knowledge base (populated by `retail-agent-setup`) in this format:

```json
{
  "products": [ { "sku": "...", "name": "...", "description": "...", ... } ],
  "policy_entries": [ { "policy_id": "...", "title": "...", "full_text": "...", ... } ],
  "promotions": [ { "promo_id": "...", "title": "...", "rules": "...", ... } ],
  "faqs": [ { "faq_id": "...", "question": "...", "answer": "...", ... } ],
  "store_info": { "name": "...", "address": "...", "hours": "...", "phone": "..." },
  "membership": { "levels": [...], "points_rules": "...", "query_method": "..." }
}
```

**Reference:** [kb-schema.md](references/kb-schema.md) — full schema with field descriptions.

---

## Fallback Behavior

If the knowledge base is empty or missing a domain:

| Missing Domain | Fallback Response |
|---------------|-------------------|
| No products | "我们的商品信息正在整理中，请联系店员了解详情。" |
| No policies | "退换货政策请联系门店工作人员确认。" |
| No promotions | "目前暂无特别优惠活动，欢迎关注我们的公众号获取最新信息。" |
| No store info | Escalate to configured L1 contact |

---

## Script: Knowledge Base Search

Use `scripts/kb_search.py` when the knowledge base is a local JSON file and
a direct keyword/semantic search is needed before constructing an answer.

**Reference:** [search-strategy.md](references/search-strategy.md) — when to use exact
match vs. fuzzy match vs. LLM synthesis.
