# Visualization & Reports / 可视化与报告

> Diagrams and reports match user's language for labels and captions. Technical concept names (Components, State, Props) stay in English.

## Mermaid Diagram Types

| Scenario | Type |
|---|---|
| Concept hierarchy / 概念层级 | `graph TD` |
| Data flow / 数据流 | `graph LR` |
| Time sequence / 时间顺序 | `sequenceDiagram` |
| State changes / 状态变化 | `stateDiagram-v2` |
| Comparison / 对比 | `mindmap` |

**Design rules**: One diagram one meaning, 3-7 nodes (split if >7), short node text (<8 chars), always add caption below.

## ASCII Fallback

Use when: platform doesn't render Mermaid, user says "can't see diagram", or diagram is very simple (<5 nodes).

```
┌──────────┐    build     ┌──────────┐    run     ┌──────────┐
│Dockerfile │ ──────────▶ │  Image   │ ──────────▶ │ Container │
└──────────┘              └──────────┘             └──────────┘
```

## Knowledge Map / 概念地图

Generate on Day 3, 5, 7 or every 2-3 days. Maintain `concept_map` in `path.json`:

```json
{
  "concept_map": {
    "Components": { "status": "mastered", "day_learned": 1 },
    "Props": { "status": "learning", "day_learned": 3 },
    "State": { "status": "pending", "day_learned": null }
  }
}
```

| Status | Meaning |
|---|---|
| `mastered` | Feynman simplify passed + self-test correct / 费曼通过 + 自测正确 |
| `learning` | Learned but not fully mastered / 已学但未完全掌握 |
| `pending` | Not yet learned / 还未学到 |

**Push format:**
```
🗺 Knowledge Map | {topic} · {n} days learned / 已学 {n} 天
✅ Mastered ({x}): {list} | 📖 Learning ({y}): {list} | ⏳ Pending ({z}): {list}
💡 Your knowledge framework is {percentage}% built. / 知识框架已建立 {percentage}%
{1-2 sentences encouragement + next direction, in user's language}
```

**Percentage formula**: `progress% = mastered_count / total_concept_count × 100`

## Weekly Report / 学习周报

**Timing**: Auto weekly cron (Sunday 20:00) or manual "give me weekly report" / 「给我周报」

**Format:**
```
📊 Weekly Report | {topic} · Week {n} ({start} - {end})
## Study Time / 学习时长: {x} days, {y} min total, {z} min/day avg
## Completion / 完成率: {a}/{b} this week ({pct}%), cumulative {c}/{total}
## Mastery / 掌握: ✅ {x} mastered, 📖 {y} learning, 🔴 {z} weak ({list})
## Feynman Quality Trend / 费曼质量走势: {1-5 star trend}
## Summary / 总结: {2-3 sentences + suggestions, in user's language}
```

**Zero-data report** (no activity this week):
```
📊 Weekly Report | {topic} · This Week
No study activity this week. / 本周无学习记录。
Last activity: {date} · Day {n}/{total}
Want to resume? Say "resume" / 说「继续」即可重新开始。
```
