# Slice Deck Schema

Use this reference when writing or validating a Slice deck (any of the 13 themes — `paper-slide` / `editorial-mag` / `bold-poster` / `notion-card` / `brutalist` / `glass-dark` / `editorial-stencil` / `broadsheet` / `blueprint` / `daisy-pastel` / `showa-catalog` / `photo-feature` / `atmospheric`).

The deck shape is **theme-agnostic**: same JSON renders in any theme. Pick the theme based on platform / mood, not content. See `themes.md` for theme picker.

## Shape

```json
{
  "theme": "paper-slide",
  "header": "shared top sticker text, <= 22 Chinese chars",
  "seriesTitle": "series name, no brackets, <= 10 Chinese chars",
  "seriesTagline": "bottom italic promise, <= 22 Chinese chars",
  "cards": [
    {
      "kind": "title",
      "title": ["line 1 <= 14 Chinese chars", "line 2 <= 14 Chinese chars"],
      "narration": "opening voiceover"
    },
    {
      "kind": "body",
      "caption": "one-line punchy caption",
      "figureKeyword": "canonical keyword",
      "narration": "spoken explanation",
      "imageUrl": "https://… (optional, photo-feature / atmospheric only)"
    }
  ]
}
```

### `imageUrl` (optional body-card field)

Public HTTPS URL of a photograph used as the card's backdrop. Read by the `photo-feature` and `atmospheric` themes; ignored by every other theme.

- If omitted on a `photo-feature` / `atmospheric` card, the renderer falls back to an SVG stub — usable but visually weak. The full per-card photo-upload plumbing (cloud-render side) is still in progress; until it ships, prefer `paper-slide` / `editorial-mag` when you cannot supply a photograph.
- Other themes treat `imageUrl` as no-op. Safe to include; the validator does not strip it.

For Remotion render props, the worker/local script converts this to:

```json
{
  "cards": [
    {
      "slide": {
        "kind": "body",
        "header": "...",
        "title": [],
        "caption": "...",
        "figureKeyword": "target",
        "seriesTitle": "...",
        "seriesTagline": "...",
        "voiceoverSrc": "paper-slide-experiments/demo/1.mp3"
      },
      "durationSec": 5.2
    }
  ]
}
```

## Keyword Map

Prefer canonical values. Free-form Chinese may work in some local setups, but canonical values make the deck portable and testable.

The LLM does not search the web for visuals in the normal PaperSlide flow. It chooses a controlled `figureKeyword`; the renderer maps that keyword to a local SVG scene, stick-figure pose, or icon. This keeps output deterministic, open-source friendly, and safe to render in CI.

### Scene Keywords

Use these first when the card needs a richer, more literal visual.

| Keyword | Use for |
|---|---|
| `problem-framing` | problem definition, real demand, goals, target |
| `evidence-board` | data, research method, proof, metrics |
| `customer-pain` | customer/user pain, audience needs |
| `timeline-review` | timeline, incident review, retrospective |
| `owner-deadline` | owner, responsibility, delivery date |
| `risk-guardrail` | risk, warning, limitation, guardrail |
| `cashflow-ledger` | cash flow, budget, pricing, value |
| `team-alignment` | team coordination, collaboration, alignment |
| `before-after` | visible change, product update, comparison |
| `learning-loop` | learning, output, feedback loop, reuse |
| `decision-fork` | choice, tradeoff, next step |
| `growth-system` | growth system, scale, repeatable operating model |

### Figure And Icon Keywords

Use these when a simple visual accent is enough.

| Keyword | Use for |
|---|---|
| `climbing` | growth, journey, long-term progress |
| `thinking` | decisions, reflection, judgment |
| `stuck` | blockers, failure, bottlenecks |
| `running` | execution, speed, action |
| `celebrating` | success, result, victory |
| `briefcase` | manager, leadership, business |
| `users` | teams, audience, users, responsibility |
| `target` | goals, focus, problem framing |
| `trending-up` | growth, improvement, metrics |
| `dollar-sign` | money, budget, pricing |
| `clock` | deadline, time, cadence |
| `message-circle` | communication, feedback, conversation |
| `flame` | warning, risk, urgency |
| `lightbulb` | idea, insight, product change |
| `chart-bar` | research methods, data, evidence |
| `rocket` | momentum, launch, motivation |
| `bell` | reminder, alert, attention |

## Scenario Recipes

### Research / Paper Digest

- Hook: "读一篇论文，先抓这3个问题"
- Body: problem → method → limitation
- Good keywords: `problem-framing`, `evidence-board`, `risk-guardrail`

### Product Update

- Hook: "产品更新文案，先回答这3件事"
- Body: user pain → visible change → next action
- Good keywords: `customer-pain`, `before-after`, `decision-fork`

### Meeting Closeout

- Hook: "一场有效会议，结尾必须有3样东西"
- Body: owner → deadline → risk
- Good keywords: `owner-deadline`, `timeline-review`, `risk-guardrail`

### Career / Management

- Hook: contrast or hidden rule
- Body: principle → mistake → action
- Good keywords: `problem-framing`, `timeline-review`, `team-alignment`, `learning-loop`

### Incident Review

- Hook: "事故复盘，别急着追责"
- Body: timeline → root cause → mechanism owner → warning
- Good keywords: `timeline-review`, `risk-guardrail`, `owner-deadline`, `evidence-board`

### Sales Enablement

- Hook: "销售话术，别先讲功能"
- Body: customer pain → proof → pricing/value → next step
- Good keywords: `customer-pain`, `evidence-board`, `cashflow-ledger`, `decision-fork`

### Founder / Startup Lesson

- Hook: "创业早期，别急着扩张"
- Body: real demand → cash flow → team pace → system before growth
- Good keywords: `problem-framing`, `cashflow-ledger`, `team-alignment`, `growth-system`

### Learning Loop

- Hook: "学新东西，别只收藏"
- Body: question → output → feedback → next action
- Good keywords: `problem-framing`, `learning-loop`, `risk-guardrail`, `decision-fork`

## Prompt Pattern

Ask the model for strict JSON only:

```text
把下面内容拆成 PaperSlide 竖屏知识短视频脚本。输出严格 JSON，不要 Markdown。
要求：1 张 title 卡 + 3 张 body 卡；caption 短、有冲击，不带标点；
narration 口语化；figureKeyword 从 canonical keyword 表里选，且相邻不重复。

内容：
---
...
---
```

## Common Failures

| Failure | Fix |
|---|---|
| Caption overflows | Shorten to one idea; remove modifiers. |
| All visuals look the same | Force unique adjacent `figureKeyword`. |
| Video feels like PPT | Use spoken narration, not bullet summaries. |
| Product/research content feels generic | Anchor body cards to user pain, method, evidence, risk, or next action. |
| Open-source package too heavy | Exclude generated media; keep only instructions and small references. |
