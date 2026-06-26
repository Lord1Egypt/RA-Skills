# Output Checklist

## Publish-Ready Response Shape

Use this shape when delivering a full article:

```markdown
推荐标题：...

备选标题：
1. ...
2. ...
3. ...

摘要：
...

正文：

# ...

...
```

If the user only asks for titles, outline, review, or polishing, output only the requested artifact.

## Draft Quality Check

- The article has one central reader promise.
- The title does not promise more than the article proves.
- The opening gives a reason to continue within the first 200 Chinese characters.
- Every section title is understandable without reading the paragraph below it.
- Each section contains at least one concrete observation, example, contrast, or actionable point.
- Paragraphs are short enough for mobile reading.
- Repeated abstract words are reduced: "赋能", "闭环", "颠覆", "升级", "高效", "深度", "价值".
- The ending gives a takeaway, checklist, or next action.
- Publish-ready WeChat drafts include a natural bottom follow CTA unless explicitly omitted.
- Draft-box upload JSON uses `coverImagePath`; any article-internal images are local files under `data/images/`, referenced through `inlineImages` placeholders rather than external `<img>` URLs.
- Body HTML avoids bordered cards, summary boxes, table-like panels, heavy background blocks, and rounded containers unless the user explicitly asks for that visual style.
- Article-internal images are content-led: use none, one, or multiple based on the article's effect, not a fixed template.

## Risk Check

Flag or soften:

- Unsourced statistics, rankings, market share, revenue, user count, and benchmark claims.
- Medical, legal, financial, investment, and policy advice.
- Claims that a competitor is "落后", "失败", "被淘汰", or "没有能力" without strong evidence.
- Promises such as "一定", "保证", "最强", "唯一", "彻底解决".
- Sensitive personal information or internal confidential details.

When evidence is missing, rewrite with safer language:

- "可能说明..."
- "更像是..."
- "从现有信息看..."
- "一个更稳妥的判断是..."
- "这还需要更多数据验证..."

## Polishing Moves

- Replace a generic opening with a scenario or contrast.
- Turn long background paragraphs into a short "问题是什么".
- Replace slogan-like claims with examples.
- Move the strongest judgment closer to the beginning.
- Cut sections that do not support the main promise.
- Change decorative headings into conclusion-style headings.

## Final Review Output

When reviewing a draft, lead with issues:

```markdown
主要问题：
1. ...
2. ...

建议改法：
1. ...
2. ...

可直接替换的版本：
...
```
