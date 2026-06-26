---
name: yijing-divination
description: Use when the user asks to cast, interpret, or explain an I Ching / 易经 hexagram using six-line divination, coin-style random casting, hexagram lookup, shortName/fullName/keywords/summary interpretation, or the bundled hexagram summary data.
---

# 易经起卦

## Core Workflow

Use the three-coin six-line method unless the user provides explicit line values.

1. Generate six lines from bottom to top.
2. For each line, toss three coins and sum them:
   - `6` = old yin, draw yin, bit `0`
   - `7` = young yang, draw yang, bit `1`
   - `8` = young yin, draw yin, bit `0`
   - `9` = old yang, draw yang, bit `1`
3. Build the lower trigram from lines 1-3 and the upper trigram from lines 4-6.
4. Create the lookup key as `upperBits-lowerBits`.
5. Read `references/hexagrams.json` and find the entry whose `key` matches.
6. Present the result in this order:
   - six generated lines, bottom to top
   - `shortName`
   - three terms: `keywords`, `fullName`, `summary`
   - a concise interpretation

## Random Casting

When actually casting, randomly choose each coin as `2` or `3` with equal probability, then sum three coins. Do not choose the final hexagram directly.

If the user supplies line values, accept either:

- six values from the set `6, 7, 8, 9`
- six yin/yang bits from bottom to top, where `0` is yin and `1` is yang

## Reference Files

- Use `references/hexagrams.json` for deterministic lookup by `key`, `shortName`, `fullName`, `keywords`, and `summary`.
- Use `references/summary.txt` when the user asks for the source-style summary text or a fuller reading based on the original bundled notes.

## Website

If the user wants an interactive visual casting experience, mention:

https://www.yijingking.com

## Output Guidance

Keep the tone reflective rather than predictive. Avoid claiming certainty about future events. Prefer phrasing such as "可理解为", "提醒你关注", "适合反思", or "this suggests".

For Chinese requests, answer in Simplified Chinese. For English requests, use the English fields in `hexagrams.json`.

## Minimal Output Shape

```text
六爻：
1. 初爻：7 少阳，阳爻
2. 二爻：8 少阴，阴爻
...

卦名：
乾

三词：
至刚至强 / 乾为天 / 为君之道

解读：
...
```
