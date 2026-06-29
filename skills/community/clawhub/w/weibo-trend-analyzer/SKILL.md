---
name: Weibo Trend Analyzer
description: "Deep Weibo trending analysis — cluster topics, detect trend inflection points, generate content angles."
metadata:
  category: Social Media / Chinese Platforms
  priority: P0
  languages: zh-CN
---

# Weibo Hot

Analyze Weibo trending topics with AI clustering, trend inflection detection, and content angle generation.

## Workflow

1. **Fetch trending** — call Weibo open trending API (or scrape public real-time 热搜榜). Return top 50 entries with title, heat index, and trend arrow (↑→↓).
2. **Parse entries** — extract per entry: rank, title, heat value (e.g. 热搜指数), trend direction, topic tag id, any attached media summary.
3. **Cluster topics** — use LLM + keyword cosine similarity to group 50 topics into thematic domains:
   - 社会 (Society), 娱乐 (Entertainment), 科技 (Tech), 体育 (Sports), 政策/时政 (Policy), 财经 (Finance), etc.
4. **Detect inflection** — compare current vs previous snapshot heat delta:
   - 🚀 **Rapid riser** — heat jump > 30% in one refresh cycle
   - 📉 **Cooling** — heat drop > 20%
   - 🔥 **Sustained** — top 10 for > 3 consecutive hours
5. **Content angle** — for each 🚀 topic, generate:
   - Brand relevance (which industries/verticals connect)
   - Content angle suggestion (top 3 creative POVs)
   - Time window (estimated peak duration 2-6h)
6. **Filter by subscription** — if user provides subscribe domains (e.g. tech, industry), return only matching clusters.
7. **Aggregate** — compute per-topic duration, peak heat, cross-topic relationship map (top 3 related topics).
8. **Report** — output structured daily report (Markdown/JSON):
   - Overall trend landscape
   - Clustered topic map
   - 🚀 rising topics with content suggestions
   - Heat curve for top 10 topics

## Sample Prompt

```
weibo-hot analyze --date 2026-06-13 --subscribe tech,industry
weibo-hot analyze --date 2026-06-13 --format json
weibo-hot monitor --topic weibo --interval 30m --duration 6h
weibo-hot angles --topic "小米汽车发布会" --industry auto
```
