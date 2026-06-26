# Output schema

## Normalized item

```json
{
  "circle_name": "AI投研圈",
  "item_id": "optional-stable-id",
  "url": "https://...",
  "published_at": "2026-03-08T09:00:00+08:00",
  "author": "作者名",
  "title_or_hook": "这篇内容的标题或首句",
  "content_preview": "100-300字预览",
  "content_type": "analysis|qa|resource|notice|event|chat|other",
  "engagement_hint": {
    "likes": 0,
    "comments": 0
  },
  "signals": ["original-analysis", "tool-release", "deadline"],
  "priority": "high|medium|low",
  "why_it_matters": "一句话解释价值",
  "suggested_action": "open-now|read-later|skip"
}
```

## Ranking hints

Raise priority when the item contains:
- original观点、框架、策略、模型更新
- 数据集、代码、工具、模板、资源包
- 明确截止时间、活动、招募、政策变化
- 行业重大事件的高质量解读

Lower priority when the item is:
- 问候、闲聊、灌水
- 明显重复
- 无新信息的转发

## Rendered digest sections

1. Header
2. Executive summary
3. Top picks
4. Grouped updates by circle
5. Recommended reading order
6. Optional skip list

## Good digest properties

- Fast to scan in under 2 minutes
- Explicit about why an item deserves a click
- Honest about uncertainty
- Preserves links so the user can jump into the original post
