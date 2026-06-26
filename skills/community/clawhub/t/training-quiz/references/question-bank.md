# Question Bank Templates

## Question Types

### Type 1: Factual Recall (记忆题)
Tests: product specs, policy terms, exact numbers.

Template:
```
这款[产品名]的[属性名]是什么？
预期答案：[从KB的对应字段直接取]
```

Examples:
- "SK-II神仙水的容量规格有哪些？" → answer from variants
- "7天无理由退货的适用条件是什么？" → answer from policy_entries.conditions
- "当前满减活动的门槛金额是多少？" → answer from promotions.rules

Scoring: exact/near-exact = correct; vague = partial; wrong = incorrect

---

### Type 2: Multiple Choice (选择题)
Tests: distinguishing correct info from plausible-but-wrong distractors.

Template:
```
[产品名]的售价是多少？
A. ¥[correct_price]
B. ¥[correct_price + 50]
C. ¥[correct_price - 80]
D. ¥[similar_product_price]
```

Distractor generation rules:
- Option A: correct answer (shuffle position randomly)
- Option B: ±10–20% of correct value
- Option C: ±25–40% of correct value
- Option D: use value from a similar product in KB

For policy questions:
- Correct: actual policy condition
- Distractors: common misconceptions (e.g., "购买当天不能退" when policy says 7 days)

---

### Type 3: Scenario (情景题)
Tests: applying knowledge to customer conversations.

Template:
```
情景：一位顾客说"[customer_message]"
你会怎么回应？
```

Good scenario seeds (fill with real KB data):
- "这款适合我妈妈用吗？她皮肤比较干" → tests product knowledge + recommendation
- "我买了5天，不喜欢想退货" → tests return policy
- "你们现在有什么活动？我要买3件" → tests promotion calculation
- "这个有没有XL码？" → tests inventory awareness
- "这两款哪个性价比更高？" → tests comparison skill

Scoring: rubric-based (see below)

---

### Type 4: Policy Drill (政策题)
Tests: correct application of store policies.

Template:
```
判断题：以下说法是否正确？
"[policy_statement]"
```

Correct statements: direct quotes from policy_entries.conditions
Incorrect statements: modified versions with wrong dates, amounts, or conditions

Example:
- ✅ "购买7天内未使用商品可以无理由退货"
- ❌ "购买15天内可以无理由退货" (wrong — it's 7 days)
- ❌ "已拆封商品也可以无理由退货" (wrong — conditions not met)

---

## Scenario Scoring Rubric

| Score | Criteria |
|-------|---------|
| Full (3 pts) | Correct info + appropriate tone + actionable response |
| Partial (2 pts) | Correct info but awkward tone or missing next step |
| Partial (1 pt) | Partially correct; misses key policy detail |
| Zero (0 pts) | Wrong info, fabricated, or unhelpful |

---

## Difficulty Levels

| Level | Criteria | Use case |
|-------|---------|---------|
| Easy | Single-fact recall; answer directly in KB | New hire, first week |
| Medium | Requires applying a rule to a scenario | After 1-2 weeks |
| Hard | Multi-step reasoning; policy edge cases | Experienced staff |

Auto-assign difficulty:
- Questions from `name`/`price` fields → Easy
- Questions from `description` + `policy conditions` → Medium
- Questions from `exceptions` + scenario combinations → Hard

---

## Session Question Mix (default 10 questions)

| Type | Count | Difficulty |
|------|-------|-----------|
| Factual recall | 3 | Easy–Medium |
| Multiple choice | 3 | Medium |
| Scenario | 3 | Medium–Hard |
| Policy drill | 1 | Medium |
