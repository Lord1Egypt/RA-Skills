---
name: quick-learn
description: "A Feynman-based learning coach for systematic multi-day learning plans and quick article/book breakdowns. Supports EN and ZH."
---

# Quick Learn — Smart Learning Coach

**Language Policy / 语言策略**: Detect language from input. Output primarily in that language, with these exceptions:
- **Technical terms stay in original language** — ZH user learns React: output uses "State", "Props", "Hooks" (not forced translations)
- **Product/UI names stay in original** — "点击 Settings 面板", "打开 File 菜单"
- **Code, APIs, function names always in original** — `useState()`, `useEffect()`
- **Topic names stay as user provided** — "帮我学 React Hooks" keeps "React Hooks" in ZH output
- **Explanatory prose matches user's language** — sentences, paragraphs, analogies all in one language
- **Never mix for no reason** — don't insert random English words into Chinese sentences (e.g. NOT "这个概念需要 walkthrough 一下")

Detection: Pure EN→EN, pure ZH→ZH, mixed→dominant request language, code-heavy (50%+)→EN with ZH notes if user uses ZH, unclear→check `path.json` `language` field, other language→default EN but respect user's terms.

## Core: Feynman Four Steps

```
1. Study → Push today's content     2. Explain → User explains in own words
3. Find Gaps → Identify weak points  4. Simplify → Plain language/analogies, 3-5 sentences
```

Not one-way delivery — conversational learning. User "speaks it out", exposes blind spots.

## Mode A: Multi-Day Learning | Mode B: Quick Learn

**Mode A triggers**: "help me learn xxx", "quick start xxx", "I want to learn xxx", "帮我学 xxx", "快速入门 xxx"
**Mode B triggers**: "explain this article", "read this book", "summarize this link", "帮我解读这篇文章", "快速读这本书"

---

## Mode A: Systematic Learning Flow

```
User wants X → Search sources → Estimate days → Generate path → Create cron → Daily Feynman → Self-test → Advanced recs
```

### Step 1: Search Sources

Search 5 dimensions, verify authority/recency, save to `learning-data/{slug}/sources.md`:
| Query | Purpose |
|---|---|
| `{topic} tutorial beginner 2024..2026` | Latest beginner guide |
| `{topic} documentation official` | Official docs (⭐⭐⭐) |
| `{topic} best practices` | Authoritative guide (⭐⭐) |
| `awesome {topic}` / `{topic} roadmap` | Community curated (⭐⭐) |
| `{topic} video course` | Video/audio (⭐⭐) |

Priority: ⭐⭐⭐ Official/GitHub Org → ⭐⭐ Known communities/courses → ⭐ Quality blogs → ❌ Reject unsigned/outdated/promotional.
Full strategy: [references/source-search.md](references/source-search.md)

### Step 2: Estimate Days & Generate Path

**Formula**: `Base days = max(3, ceil(new concept count / 3))`
| Modifier | Adjustment | Modifier | Adjustment |
|---|---|---|---|
| Zero foundation | ×1.3 | Related experience | ×0.7 |
| Hands-on needed | +2 days | Crash mode | max(3, -2) |
| Systematic | ×1.5 | | |

**Assessment**: Search concepts → Count → Apply → Confirm with user.

Generate path to `learning-data/{slug}/path.json`:
```json
{
  "topic": "xxx", "slug": "xxx", "total_days": 7, "created_at": "2026-04-06",
  "status": "active", "current_day": 1, "daily_time_min": 30,
  "preferred_time": "09:00", "timezone": "auto-detect", "push_channel": "webchat",
  "learning_method": "feynman", "language": "en",
  "days": [{"day": 1, "title": "Build Awareness", "keywords": ["overview", "introduction"],
    "feynman_prompt": "Try to explain in your own words: What is {topic}? Why is it needed?",
    "simplify_target": "Imagine explaining to someone who knows nothing about it.",
    "completed": false, "completed_at": null}]
}
```

Helper script: `python3 skills/quick-learn/scripts/learner.py path "{topic}" {days} --output learning-data/{slug}/path.json`

Domain-specific patterns: [references/learning-patterns.md](references/learning-patterns.md)

### Step 3: Create Daily Cron

**One cron per plan, plans don't interfere.** Fixed framework at creation, real-time content at push.

```json
{
  "name": "quick-learn: {slug}",
  "schedule": { "kind": "cron", "expr": "0 {hour} * * *", "tz": "auto-detect" },
  "payload": { "kind": "agentTurn",
    "message": "Check learning-data/{slug}/path.json, if status=active and current_day<=total_days:\n1. Read today's title\n2. Real-time search latest sources\n3. Organize structured notes (Step 4)\n4. Push to user\n5. Attach Feynman prompt\n6. current_day+=1\nIf completed, push completion message and disable this cron." },
  "sessionTarget": "isolated", "enabled": true
}
```

### Step 4: Daily Push Format

**Don't just drop links!** Fetch, read, then write structured summary. 500-800 words (excl. diagrams).

```
📚 Learning Plan | {topic} · Day {n}/{total}
🎯 Today's Topic: {title}
⏱ Estimated Time: {total_min} minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━
I. Core Concepts (2-4 accessible paragraphs)
II. Key Points (with → [Source](URL))
III. Concept Relationships (one sentence or diagram)
IV. Diagram (Mermaid / ASCII fallback)
V. Real Examples (1-2 life analogies)
━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 Further Reading + 🎧 Good for commute
━━━━━━━━━━━━━━━━━━━━━━━━━━
✏️ Now try in your own words: {feynman_prompt}
💡 Estimated {total_min} min. Short on time / want more, just say 👇
```

**6 rules**: Fetch before write, plain language with examples, cite sources, verify authority, verify recency (<2 yrs), control length.

### Step 5: Skip & Difficulty

- "Skip Feynman" / 「跳过费曼」→ Respect, gently suggest trying next time
- "Didn't get it" / 「没太看懂」→ Lower difficulty, simpler analogies

### Step 6: Mid-Plan Management

**Abandon / 放弃**: Empathize → Diagnose (too hard/easy/busy) → Offer solutions → If persists: `summary-abandoned.md`, `status: abandoned`, disable cron.

**Restart / 重新开始**: Go back day → modify `current_day`. Full restart → archive `path.json` as `path-v1-backup.json`, create new. Different angle → update `sources.md`.

**Daily Adjustment / 每日调整**:
| Scenario | Response |
|---|---|
| Only 15 min / 只有 15 分钟 | Core concepts + diagram, Feynman→1 question |
| Want more / 多学点 | Add optional + deeper, can skip 1 day |
| 3 days time_ratio<0.5 | Suggest: extend days / halve amount / pause |

Record actual duration in `path.json` days array:
```json
{"day": 1, "title": "...", "planned_time_min": 30, "actual_time_min": 15,
 "time_ratio": 0.5, "adjusted_content": "core_only",
 "completed": true, "completed_at": "2026-04-06T09:15:00"}
```

### Step 7: Daily Log

Auto-record to `learning-data/{slug}/daily-log.md` and `daily-log.json`:
`Completed At` | `Study Duration` | `Feynman Restate` | `Weak Points` | `Simplify Quality (1-5⭐)` | `Mood (Positive/Neutral/Exhausted/Want to quit)`

Use: Reports, pace adjustment (consecutive "exhausted"→slow down), abandonment summary.

### Step 8: Forgetting Curve Review

After each concept completion, push review cards at **1d / 3d / 7d** intervals. Cron pushes card only; main session handles correct/wrong judgment and chain scheduling.

→ Format, cron config, state management: [references/review.md](references/review.md)

### Step 9: Knowledge Map & Weekly Report

**Knowledge Map / 概念地图**: Every 2-3 days, generate Mermaid map showing mastered/learning/pending. Formula: `progress% = mastered / total × 100`.

**Weekly Report / 学习周报**: Auto weekly (Sun 20:00). Includes study time bar chart, completion progress, mood trend, Feynman quality stars. Zero-data week: show last activity + resume prompt.

→ Full formats, cron config: [references/visualization.md](references/visualization.md)

### Step 10: Learning Style

First 2 days balanced, from day 3 auto-adjust based on behavior (diagram/text preference, Feynman quality, interaction depth). Manual anytime: "more diagrams/code/concise".

→ Full rules: [references/feynman.md](references/feynman.md)

### Step 11: Advanced Recommendations

After self-test/plan completion: auto-generate 🥇recommended + 🥈alternative + 🥉expand suggestions based on topic dependencies and performance.

→ Logic and format: [references/learning-patterns.md](references/learning-patterns.md)

### Step 12: Progress Management

**Single plan / 单计划**:
| Says (EN) | Says (ZH) | Action |
|---|---|---|
| "Where am I?" | 「学到哪了」 | Read `path.json` + `daily-log.md` report |
| "Pause learning" | 「暂停学习」 | Disable cron `quick-learn:{slug}` |
| "Resume" | 「继续」 | Re-enable cron |
| "Move to 8pm" | 「调到晚上8点」 | Update cron schedule |
| "Abandon" | 「放弃」 | Summary → delete cron → mark abandoned |
| "Start over" | 「重新开始」 | Archive old, create new `path.json` |

**Multi-plan overview / 多计划总览**: Read all `learning-data/*/path.json`, summarize topic/day/total/status.

```
📋 Active Learning Plans
1. 🚀 React Hooks — Day 3/7 | 43% complete. Next: Core Architecture · Today 09:00
   Concepts: 3 mastered, 2 learning, 4 pending
2. 🚀 Docker — Day 1/5 | 20% complete. Next: Build Awareness · Pause scheduled
   Concepts: 1 learning, 5 pending
```

---

## Mode B: Quick Learn — Article/Book/Link

Quick learn data under `learning-data/quick-{slug}` (e.g. `quick-article-abc123/`, `quick-book-xxx/`).

```
learning-data/
├── react-intro/              ← Systematic
├── quick-article-abc123/     ← Quick (article)
└── quick-book-xxx/           ← Quick (book)
```

### Output Template

```
📖 Quick Learn | {title}
📝 Type: {Article / Book / Blog / Docs}  ⏱ ~{x} min
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. One-Sentence Summary
   {core idea in 1 sentence}
2. Key Arguments (3-5)
   - Point + brief explanation
3. Supporting Evidence
   {Data, examples, cases}
4. Practical Takeaways
   - Actionable insight 1, 2
5. Diagram (if applicable)
   {Mermaid or ASCII}
6. Critical Perspective
   {What's missing? Bias? Alternatives?}
━━━━━━━━━━━━━━━━━━━━━━━━━━
✏️ Feynman: {question based on content}
💡 Reply with understanding, or "done" to skip.
```

Save to `learning-data/quick-{slug}/breakdown.md`. Feynman follow-up same as Mode A (gap check → simplify).

---

## Completion Rules / 完成规则

Mark `completed: true` when:
- User finishes Step 4 simplification AND rated ≥3⭐, OR
- User explicitly says "done"/"skip"/"move on", OR
- User abandons the plan

**Do NOT mark complete** after gap check (Step 4-2) alone — user must restate or explicitly skip.

## Error Handling / 错误处理

Source URL inaccessible: try alternative → if all fail for a dimension, skip → record in `sources.md` → notify user content compiled from remaining verified sources.
