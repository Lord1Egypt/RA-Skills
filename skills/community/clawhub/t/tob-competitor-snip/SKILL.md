---
name: tob-competitor-snip
description: When a client mentions a competitor, quickly generate a differentiation comparison + counter-talking points card. Pure rules engine — no external dependencies.
priority: high
source: experience-backed
tags: [tob, sales, competitor, presales]
metadata:
  openclaw:
    requires:
      bins: [node]
---

# 🔪 tob-competitor-snip — Competitor Snip Assistant

> Client mentions a competitor? 30 seconds to a counter card.

## When to Use

Use when:
- Client says "X company has Y feature"
- Client says "X is 30% cheaper than you"
- Client asks for a feature-by-feature comparison
- You're preparing a proposal and need to understand competitive landscape

## Usage

### Interactive Mode
```bash
node {baseDir}/src/generator.js
```

### Quick Mode
```bash
node {baseDir}/src/generator.js --competitor "Some Vendor" --concern "cheaper price"
```

### Full Mode
```bash
node {baseDir}/src/generator.js --competitor "Some Vendor" --industry "retail" --concern "they support multi-turn dialogue"
```

## Output: 4-Module Card

### Module 1: Competitor Profile
- Name, known strengths/weaknesses (based on experience rules)
- If no record: "暂无交手记录" (no交手 record yet)

### Module 2: Differentiation Comparison
| Dimension | Competitor | Us | Client Value |
|-----------|-----------|----|-------------|

Dimensions: feature depth, industry know-how, delivery speed, after-sales, TCO, extensibility

### Module 3: Counter Talking Points
- **Price war**: reframe from "first-year price" to "3-year TCO"
- **Feature comparison**: reframe from "feature count" to "real adoption rate"
- **Brand trust**: reframe from "brand size" to "customer renewal rate"

### Module 4: Case References
- Industry-agnostic case patterns
- Never fabricate specific client names or data

## Scenario Rules

| Trigger Keywords | Scenario | Rule Set |
|-----------------|----------|----------|
| 便宜/低价/价格/报价/成本/预算 | Price War | TCO reframe framework |
| 功能/多轮/工单/对话/自动化/AI | Feature Gap | Adoption rate reframe |
| 品牌/大公司/上市/规模 | Brand Trust | Renewal rate reframe |
| (none matched) | General | POC suggestion framework |

## Field Principles

1. **Acknowledge, then pivot** — Never dismiss the competitor
2. **Reframe the question** — Turn their concern into a risk
3. **Cases, not conclusions** — Use patterns, not fabricated specifics
4. **Price = TCO** — First-year quote ≠ 3-year cost
5. **No fabrication** — When no experience, say so and offer a POC framework

## Post-Use

After a real competitive engagement:
- Record the actual outcome (win/loss) for future reference
- Feed lessons learned back into your knowledge base
