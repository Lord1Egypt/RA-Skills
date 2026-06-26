# Sentiment Scoring Guide

## Aspect-Level Sentiment Methodology

### Why Aspect-Level Matters
A single review often contains multiple sentiments about different aspects. Document-level sentiment misses this nuance entirely.

Example: "Love the product quality but shipping took 3 weeks and customer service was unhelpful when I asked about it."
- Product Quality: 5/5 (strongly positive)
- Shipping Speed: 1/5 (strongly negative)
- Customer Service: 2/5 (negative)
- Document-level would score this as "neutral" (3/5) — missing everything useful.

### Scoring Scale

**5 — Strongly Positive (Delight)**
- Emotional language: "love," "amazing," "best ever," "exceeded expectations"
- Unprompted recommendation or repurchase intent
- Comparison favorably to alternatives
- Example: "This is hands down the best moisturizer I've ever used. Already ordered two more."

**4 — Positive (Satisfaction)**
- Affirmative language: "good," "works well," "happy with," "as expected"
- Meets expectations without strong emotion
- Would recommend if asked but doesn't volunteer it
- Example: "Good quality fabric. Fits as described in the size chart."

**3 — Neutral (Mixed or Indifferent)**
- Balanced positive and negative within the same aspect
- Factual description without emotional valence
- "It's fine" or "nothing special" energy
- Example: "The taste is okay. Not great, not terrible."

**2 — Negative (Dissatisfaction)**
- Complaint language: "disappointed," "not worth," "expected better"
- Specific issue identified but not extreme
- Might still use the product but unhappy about this aspect
- Example: "The color faded significantly after just two washes."

**1 — Strongly Negative (Frustration/Anger)**
- Intense emotional language: "terrible," "waste of money," "furious," "scam"
- Demands action (refund, replacement)
- Explicit statement of not repurchasing or warning others
- Example: "Completely useless. Broke on the first day. DO NOT BUY THIS."

### Intensity Signals

**Amplifiers (push score toward extremes):**
- Capitalization: "TERRIBLE shipping" → stronger negative
- Exclamation marks: "Amazing!!!" → stronger positive
- Superlatives: "worst," "best," "most" → extreme
- Repetition: "so so so slow" → stronger negative
- Explicit recommendations: "everyone should buy this" → 5/5

**Dampeners (pull score toward neutral):**
- Hedging language: "kind of," "somewhat," "I guess"
- Conditional praise: "good for the price," "not bad considering"
- Mixed qualifiers: "nice but..." 

### Handling Edge Cases

**Sarcasm and Irony:**
- "Oh great, another package that arrived destroyed" → Score as negative (1-2) based on actual meaning
- Look for contrast between surface language and context

**Conditional Sentiment:**
- "Would be perfect if it had X" → Score the existing aspect as positive (4), flag the gap separately
- "Great except for Y" → Score primary aspect positive, Y aspect negative

**Comparative Sentiment:**
- "Better than Brand X but not as good as Brand Y" → Score as positive (4) with competitive context
- "Switched from Brand X and much happier" → Score as strongly positive (5)

**Star Rating vs. Text Mismatch:**
- When star rating conflicts with text sentiment, trust the text for aspect-level scoring
- A 3-star review with "I love this product but shipping ruined the experience" = Product: 5, Shipping: 1

### Calibration Process

To ensure consistency across a large dataset:
1. Score a calibration set of 20 diverse feedback items independently
2. Compare scores and discuss disagreements
3. Document edge case decisions as precedents
4. Re-calibrate every 500 items or when new themes emerge
5. Spot-check 5% of scored items monthly for drift

### Aggregation Rules

**Theme-level sentiment:**
- Calculate weighted average of all feedback items tagged to that theme
- Weight by recency: feedback from last 30 days weighted 2x vs. 60-90 days
- Report both mean and distribution (a theme with 50% scores at 5 and 50% at 1 is different from 100% at 3)

**Trend calculation:**
- Compare current period average to previous period
- Flag themes where sentiment shifted more than 0.5 points
- Distinguish between sentiment change and volume change (more complaints vs. same complaints but angrier)
