# Step 06 — Knowledge Base Validation

## Goal
Test the knowledge base built in Step 03 with real questions the agent will face.
Identify gaps. Reach a score of 80+ before proceeding.

---

## Auto-Generated Test Suite

Use `scripts/gen_test_cases.py` to generate 10 test questions tailored to the store's vertical and role.

The script takes `vertical` and `role_id` as inputs and outputs a test set covering 5 categories:

| Category | # of Questions | Tests |
|----------|----------------|-------|
| Product knowledge | 3 | Descriptions, specs, suitability |
| Inventory | 2 | Stock levels, variant availability |
| Policy | 2 | Returns, warranties, promotions |
| Recommendation | 2 | Budget-based, occasion-based, recipient-based |
| Edge cases | 1 | Out-of-scope, sensitive, or trick questions |

---

## Sample Test Questions by Vertical

### Apparel / Footwear
1. "这款连衣裙有没有L码藏青色？"
2. "适合正式场合穿的鞋子有哪些？预算800以内"
3. "买了三天的衣服洗了之后褪色，能退吗？"
4. "送给妈妈的礼物，她平时穿M码，喜欢素色，推荐什么？"
5. "你们的羊绒产品是真羊绒吗？怎么鉴别？"

### Beauty / Skincare
1. "这款精华液适合油性皮肤吗？"
2. "我对酒精过敏，这个产品有酒精成分吗？"
3. "买了一个月的护肤品还没拆封，可以退吗？"
4. "30岁开始抗老，你们有什么推荐？预算500"
5. "这个面膜可以天天敷吗？"

### Consumer Electronics
1. "这款蓝牙耳机的续航时间多久？"
2. "我要买一台适合学生用的笔记本，预算4000左右，推荐什么？"
3. "买了两周的手机突然黑屏了，怎么处理？"
4. "这个充电宝可以带上飞机吗？"
5. "你们的耳机和官方旗舰店的一样吗？"

### General (fallback)
1. "你们有什么新品？"
2. "现在有什么优惠活动？"
3. "如果我买了不合适，可以退货吗？"
4. "能帮我推荐一个适合送朋友的礼物吗，500元以内"
5. "你们几点关门？"

---

## Scoring Rubric

For each test question, rate the agent's response:

| Score | Criteria |
|-------|---------|
| 10 | Accurate, complete, natural. Answers the question fully without hallucination |
| 7 | Mostly accurate but missing a detail (e.g., gives product but not the variant) |
| 4 | Partially answers but misses key info or is too vague |
| 1 | Incorrect answer or clearly fabricated |
| 0 | "I don't know" or no relevant answer |

Total score = (sum of 10 answers) / 100 × 100

---

## Gap Classification

After scoring, classify failures:

| Failure Type | Root Cause | Fix |
|-------------|-----------|-----|
| Product unknown | SKU not in catalog | Import more product data |
| Wrong variant info | Variants not structured | Re-run `parse_products.py` with variant flag |
| Policy unclear | Policy doc not imported | Upload policy document |
| Stale inventory | Sync lag | Check data source freshness |
| Wrong promotion | Promo not imported or expired | Update promotions |
| Hallucinated answer | LLM making things up | Add explicit "I don't know" guardrail |

---

## Gap Fix Workflow

1. Show the user which questions failed and why
2. For each failure, provide the specific fix action
3. After fixes, re-run the test suite
4. Repeat until score ≥ 80

**Example gap fix prompt:**
> "Question 3 failed: I don't have your return policy. Can you paste it here or upload a document?"

---

## Guardrail Configuration

After validation, configure the "I don't know" behavior:

```json
{
  "unknown_response": "非常抱歉，我暂时没有关于这个问题的信息。我已经记录下来，后续会更新。您也可以联系我们的工作人员获得帮助。",
  "log_unknown_queries": true,
  "alert_on_repeated_unknown": true,
  "repeated_threshold": 3
}
```

This ensures the agent never fabricates answers and logs knowledge gaps for Step 12 improvement cycles.
