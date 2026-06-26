# XHS Writing Coach — Strategy Notes (living document)

This file is **the long-term “know-how” memory** for the skill.
Update it whenever we learn something new about what works (and what gets repetitive).

## 0) Problem we observed

Our generated posts became repetitive because we over-fit to one stable structure:
- title → hook → 3 methods → CTA

This is a *generator*, not a *writing strategy engine*.

Goal: make the system choose **topic + angle + narrative archetype + hook mechanics** so daily posts are not stuck in a single pattern.

---

## 1) What makes XHS posts “feel viral” (working model)

Not “better writing” in general—more often it is:

1) **Angle beats structure**
   - Same hot topic can be rewritten from: engineer/product/worker/ethics/cost/"I got burned".

2) **First screen wins**
   - First 2–3 lines must contain:
     - a named hot keyword (e.g., GPT‑5.3 / Qwen / TikTok E2E / Meta glasses)
     - a conflict or payoff
     - a promise of what the reader gets (checklist / decision rule / pitfall)

3) **Information gap & tension**
   - Titles that win usually create an info gap ("别再..." / "真正变的是..." / "代价是...").

4) **Comment-entry is not generic CTA**
   - Better than "你怎么看": A/B choices, self-test, fill-in-the-blank, or "vote the pain".

---

## 2) Breakthrough: generate angles first

Before writing, produce an **Angle Bank** (8–12 candidates) and choose one.

Angle templates:
- Engineer: latency/cost/rollback/observability/regression tests
- Product: interaction loop changes, new defaults, feature frequency
- Governance: accountability, boundaries, supply-chain clauses
- Worker: job reshaping, skills, anxiety, coping
- Contrarian: the real change is not the headline
- Personal burn story: "I got burned, so now I do X"

Selection heuristic:
- Prefer angles with **clear conflict** and **specific actionability**.

---

## 3) Narrative archetype router (rotate to avoid repetition)

Instead of always "3 methods", choose one archetype daily.

Recommended archetypes (8):
1) Postmortem (I messed up → cost → prevention)
2) Myth-busting (people think X → truth Y → how to verify)
3) Take a side (A vs B → 3 reasons → you choose)
4) Decision checklist (3–5 rules + why)
5) Compare review (X vs Y + who fits)
6) Workflow tutorial (step-by-step)
7) Emotional resonance (anxiety → reframing → tiny action)
8) Trend forecast (next 1–3 months + what to prepare)

Anti-repeat rule:
- Keep a 7-day history; avoid same archetype for the next 2–3 days.

---

## 4) Title engine (not random)

Generate ~10 titles and score them.

Scoring axes (simple heuristics):
- Keyword front-loading (<=13 chars)
- Info gap strength
- Conflict strength
- Audience targeting ("如果你是...")
- Specificity (numbers, constraints)

Keep top 3, pick best match to the chosen archetype.

---

## 5) Hot topic grounding workflow (Tavily)

We use Tavily (not Brave). Keep links/citations when possible.

Search queries that work:
- "小红书 爆款笔记 拆解 标题 结构 开头 钩子"
- "小红书 运营 选题 热点 借势 评论区 引导"
- "site:zhihu.com 小红书 爆款 标题 公式 开头 三秒"

Notes:
- Some results are SEO-heavy; prefer reputable marketing/PM sites (e.g., woshipm, digitaling, niaogebiji) and use them as directional heuristics, not gospel.

---

## 6) Style mixer (tone knobs)

Default tone for Hervé:
- engineer-hardcore + product thinking + light sarcasm

Available knobs:
- more sarcastic
- more calm/neutral
- more emotional
- more tutorial

---

## 7) Output constraints (current contract)

- Title <= 20 chars, keyword early
- Body 300–600 chars, short sentences, 2–3 lines per paragraph
- Tags 5–8, **no #AI生成内容** (user requested removal)
- CTA must be structured (A/B, self-test, fill-in-the-blank)
- Provide 1 reference link

---

## 8) Next iteration ideas (backlog)

- Build a "comment-question generator" per topic, pick 1 conflict question to drive the post.
- Keep a rolling "forbidden phrases" list to reduce stylistic repetition.
- Add a simple novelty metric: n-gram overlap vs last 7 posts.
