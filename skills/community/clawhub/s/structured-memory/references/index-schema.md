# Index Schema

## by-date.json

Each date key stores a compact summary:

```json
{
  "2026-03-09": {
    "mask": 1824,
    "domains": ["project", "routines", "meta"],
    "modules": ["risk", "automation", "memory-system"],
    "entities": ["UserA", "ai-tech-daily-brief", "Feishu", "structured-memory"],
    "system_tags": ["incident", "rule", "correction", "resolved"],
    "free_tags": ["delivery", "retrieval", "critical-facts"],
    "priority": "high",
    "preview": [
      "晨报投递失败，原因是 channel context 问题",
      "历史相关问题必须先查 memory",
      "structured-memory 继续推进"
    ],
    "topic_summaries": {
      "routines": ["晨报任务正常生成内容，但投递阶段失败。"],
      "meta": ["历史相关问题必须先查 memory。"],
      "project": ["structured-memory taxonomy 已收敛。"]
    }
  }
}
```

## Schema notes

- `preview`: short UI-oriented recap, recommended 3-5 lines only.
- `topic_summaries`: the primary multi-topic summary layer, keyed by domain or reusable module.
- `preview` is optional and should never be treated as the full memory of the day.
- retrieval should prioritize domains/modules/entities over preview text.

## Domain bits

- bit 0 = strategy
- bit 1 = business
- bit 2 = organization
- bit 3 = finance
- bit 4 = legal
- bit 5 = project
- bit 6 = operations
- bit 7 = tech
- bit 8 = routines
- bit 9 = personal
- bit 10 = meta
- bit 11 = misc

## Critical facts entry

```yaml
- entity:
  fact_type:
  value:
  status:
  sensitivity:
  source:
  last_verified:
  related_project:
  domains: []
  modules: []
  tags: []
  note:
```
