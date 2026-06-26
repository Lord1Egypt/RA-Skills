---
name: review-buying-advisor
description: Analyze a product from name plus platform, read public reviews, and turn evidence into a practical buying recommendation
version: 1.0.0
tags: shopping, reviews, product-research, consumer-protection, ecommerce, china
---

# Review Buying Advisor

Analyze a product from name plus platform, read public reviews, and turn evidence into a practical buying recommendation. Use when the user asks whether a product is worth buying on Tmall, Taobao, JD.com, Pinduoduo, Amazon, Best Buy, or similar platforms; asks for help reading reviews; wants a real user-feedback summary; wants recurring complaints, hidden risks, pros and cons, buying advice, who the product is suitable for, or how to avoid buying mistakes before ordering. Especially relevant for requests like "值不值得买", "帮我看评论", "看看口碑", "有什么坑", "适不适合买", or "帮我避坑".

## Usage Scenarios

### Scenario 1: Standard Product Review Check
**User input:** "帮我看看这款蓝牙耳机的口碑，在京东上，值得买吗？"
**Expected output:** The skill identifies the product and platform, determines review accessibility (Mode 1), samples a representative set of public reviews (positive, negative, mixed, recent), groups signals into themes (sound quality, battery life, comfort, connectivity issues), identifies recurring complaints and their severity, and outputs: Overall Verdict (Recommend / Not Recommended), Best For, Main Positives, Main Risks, Watch Before Buying, Final Advice, and Confidence level.

### Scenario 2: Review-Limited Platform
**User input:** "这个洗发水在小红书上口碑怎么样？"
**Expected output:** The skill attempts to access reviews. If the platform blocks or weakens review content, switches to Mode 2. Outputs: Not enough evidence for a strong recommendation, explains the limitation (platform blocking review access), gives limited conclusion with low confidence, and advises what the buyer should verify independently before purchasing.

### Scenario 3: Buyer's Remorse Prevention
**User input:** "我想买这个扫地机器人，但怕有坑，帮我看看有什么常见问题"
**Expected output:** The skill searches for the product on the platform, samples reviews looking specifically for recurring complaints and failure modes, separates repeated issues from isolated complaints, weighs severity as well as frequency, and outputs: common issues (laser navigation fails after 6 months, water tank leaks), severity assessment (medium - some users report partial refund success), and buyer fit recommendations (best for homes without thick carpets, avoid if you have mostly dark floors).
### Scenario 4: 想买扫地机器人但评价太乱了
**User input:** "我想买个扫地机器人，预算2000以内，在京东看了追觅和石头的小米款，评论区有说好的有说坏的不敢下手。"
**Expected output:** 从海量评价中提取有效信息：追踪追觅和石头在该价位段各型号的差评关键词（如'容易卡住'、'噪音大'、'APP总掉线'）；比较30天内好评率和追评内容；参考抖音/b站up主实测视频的结论。建议在京东自营购买利用7天无理由，并注意哪些店铺支持上门售后。

## Workflow

1. Identify the product.
   - Accept a product name plus platform.
   - Match the likely listing by brand, model, category, and variant cues.
   - If the product is ambiguous, ask one short clarifying question.
   - Do not guess across multiple plausible products or variants.

2. Check review accessibility.
   - Try to access public review content on the specified platform.
   - Decide which mode applies:
     - **Mode 1** if enough public review content is accessible.
     - **Mode 2** if review content is blocked, too weak, or too incomplete.

3. If Mode 1, analyze review evidence.
   - Use a representative sample rather than only the first visible comments.
   - Include positive, negative, mixed, and recent reviews when possible.
   - Prefer specific reviews over generic praise or blame.
   - Downweight generic praise, generic criticism, shipping-only comments, and suspiciously promotional wording.
   - Group signals into useful themes.
   - Separate repeated issues from isolated complaints.
   - Weigh severity as well as frequency.

4. If Mode 2, do not fake completion.
   - State that public review evidence is not sufficiently accessible.
   - Explain the limitation briefly.
   - Give only a limited conclusion when still useful.
   - Do not pretend to have validated real review sentiment.

5. Give the final answer.
   Cover:
   - verdict
   - what evidence was actually available
   - buyer fit when supportable
   - main positives and risks when supportable
   - what to verify before buying
   - confidence

## Output

Use this structure unless the user asks for something else.

### Mode 1 output
Use when public review evidence is available.

#### Overall Verdict
Choose one:
- Recommend
- Recommend with caveats
- Depends on use case
- Not recommended
- Not enough evidence for a strong recommendation

#### Why
2-4 bullets with the strongest evidence.

#### Best For
Who is most likely to be satisfied.

#### Main Positives
Most credible repeated strengths.

#### Main Risks
Most important risks, including repeated issues or severe but less frequent ones.

#### Watch Before Buying
What the buyer should verify before ordering.

#### Final Advice
A direct recommendation in plain language.

#### Confidence
High / Medium / Low, with a brief reason.

### Mode 2 output
Use when public review evidence is not sufficiently accessible.

#### Overall Verdict
Usually:
- Not enough evidence for a strong recommendation
- Depends on use case

#### Why
Explain what was and was not accessible.

#### Current Limitation
State whether the issue is platform blocking, weak public text, ambiguous product matching, or incomplete review visibility.

#### Watch Before Buying
State what remains unverified.

#### Final Advice
Give a cautious conclusion without pretending the reviews were validated.

#### Confidence
Usually Low.

## Quality bar

Do:
- lead with the verdict
- use representative evidence
- explain trade-offs clearly
- say who the product is for
- lower confidence when evidence is weak

Do not:
- summarize without recommending
- rely on only one review slice
- overreact to one dramatic review
- overstate certainty
- invent facts not supported by visible evidence

## Limitation handling

If the product cannot be identified confidently:
- ask one short clarifying question

If the platform does not expose enough public review content:
- switch to Mode 2
- state the limitation briefly
- keep confidence low

If public review evidence is sparse or mixed but still partially usable:
- stay in Mode 1 only if a limited review-based judgment is still supportable
- lower confidence
- narrow the claim

If reviews may mix multiple variants:
- mention that risk
- avoid overly specific claims unless the variant is clear
