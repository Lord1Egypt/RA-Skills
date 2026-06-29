---
name: wechat-digest
description: "Extract, summarize, and synthesize WeChat public account articles into structured knowledge cards"
---

# WeChat Digest

Deep extraction and synthesis of WeChat public account (微信公众号) articles. Removes noise, extracts core arguments, and generates multi-format summaries. Cross-article synthesis for thematic reading.

## Workflow

1. **Extract content** — Fetch and parse WeChat articles from URL, shared text, or archived HTML.
2. **Denoise** — Strip ads, "follow us" banners, bottom menus, related-article footers, and social sharing widgets.
3. **Structured extraction** — Pull core arguments, key data points, quotes, case studies, and article outline.
4. **Summarize** — Generate three variants:
   - **One-liner** — Extreme brevity for scanning.
   - **3-paragraph** — Executive summary.
   - **Knowledge card** — Structured facts, figures, and takeaways.
5. **Cross-article synthesis** — Given multiple articles on one topic, merge, de-duplicate, and highlight consensus vs. disagreement.
6. **Export formats** — Knowledge cards, Markdown notes, or mind map outline (OPML/Indent).
7. **Reading list** — Suggest related articles based on topic tags.
8. **Output** — Structured notes to stdout or file.

## Sample Prompts

- `wechat-digest digest --url https://mp.weixin.qq.com/s/xxx`
- `wechat-digest digest --urls https://mp.weixin.qq.com/s/a https://mp.weixin.qq.com/s/b --synthesize`
- `wechat-digest digest --url https://mp.weixin.qq.com/s/xxx --format knowledge-card`
- `wechat-digest batch --file urls.txt --outdir ./notes`

## Safety

- WeChat links are fetched directly; no third-party aggregation service.
- Respects article copyright — output is summary/extract only, not full-text republishing.
- No login/cookie required for public articles; paywalled articles are skipped with a notice.
