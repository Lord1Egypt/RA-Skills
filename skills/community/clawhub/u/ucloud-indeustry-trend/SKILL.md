---
name: ucloud-indeustry-trend
description: UCloud industry trend radar for tracking the latest 30-60 day changes, new customer demand, new business models, solution shifts, high-value financings, and notable teams across AI, cloud, semiconductor, overseas expansion, quant, and data center industries. Use when Codex needs to judge whether an industry solution deck is still current, produce an industry-by-industry trend brief with dated sources, refresh pre-sales messaging, identify which companies and teams are newly worth tracking, or update a solution package based on recent market movement.
---

# Industry Trend Radar

## Overview

Research recent market movement for one or more industries, then turn that research into a concise, dated brief that is directly usable for pre-sales, solution refresh, strategy review, or internal enablement.

Always treat this as a live research task. For any request about "latest", "recent", "this month", or "the past 1-2 months", browse the web and anchor the answer to exact dates.

## Workflow

1. Normalize the industry list.
Use the user's original wording when presenting results, but map each item to the closest entry in [references/industry-map.md](references/industry-map.md) so the search terms and watch points are consistent.

2. Fix the observation window.
Default to the latest 60 days unless the user gives a different window. State the exact start date and end date in the output.

3. Search broadly, then narrow.
Start with recent news and official sources for each industry. Prefer primary or high-authority evidence such as:
- official company blogs and product release notes
- earnings calls and investor materials
- regulators, exchanges, and policy announcements
- major cloud, chip, AI, robotics, or e-commerce platforms
- well-established industry media and research houses
- financing announcements, investor newsrooms, and startup databases when the user wants company momentum signals

4. Separate facts from inference.
For each industry, distinguish:
- what changed
- why it matters
- what it likely means for customer demand, buying criteria, or solution packaging

If a point is inferred from multiple signals rather than stated directly by a source, label it clearly as an inference.

5. Focus on commercial impact.
Do not stop at trend description. Translate each industry update into:
- likely new customer demand
- likely new buying or delivery models
- what should change in a solution deck, proposal, pricing story, or positioning

6. Add company momentum signals.
For each industry, check whether the past 30-60 days include one or more high-value financings or especially important teams worth tracking.

Use the rules in [references/funding-and-team-signals.md](references/funding-and-team-signals.md) to decide:
- which financings are commercially meaningful
- which teams or companies are worth naming even without a financing event
- how to explain why that company now matters for strategy, competition, channel, or customer demand

If there is no meaningful financing or standout team in the observation window, say so explicitly instead of padding the answer.

7. Keep the answer high signal.
For each industry, prefer 3-5 meaningful changes over a long list of weak headlines. Merge duplicate signals into one conclusion when they point to the same shift.

## Research Rules

- Always browse for temporally unstable topics.
- Use exact dates such as `2026-03-01 to 2026-04-23`, not relative phrases alone.
- Use both Chinese and English search terms when the industry is global or export-related.
- Prefer sources published inside the observation window, but allow slightly older background sources when needed to explain why a new change matters.
- Include source links in the final answer.
- Flag low-confidence industries when the signal volume is thin.
- If the user asks for many industries at once, keep the writeup compact and prioritize changes that affect solution strategy, demand, procurement, deployment, compliance, pricing, go-to-market, financing, or key company momentum.

## Output Shape

Use the structure in [references/output-template.md](references/output-template.md).

At minimum, each industry section should include:
- one-paragraph judgment
- recent changes or trends
- new customer demand signals
- new model, channel, procurement, or delivery changes
- one high-value financing if one exists
- one or more notable teams or companies worth tracking
- impact on solution packaging or pre-sales messaging
- dated sources

## What To Emphasize By Default

Unless the user asks for a different lens, bias the analysis toward:
- pre-sales and solution refresh
- what changed in the last 30-60 days
- evidence that affects budget, urgency, or buying criteria
- productization, deployment, compliance, or ROI expectations
- financings and teams that signal where capital, talent, and customer momentum are concentrating
- whether the old industry narrative is now stale

## Industry Set For This Team

The default industry set currently includes:
- AI基模
- AI行模-投顾金融
- AI agent
- AI机器人
- AI智能硬件
- AI应用
- 出海-加速器
- 出海-IP代理
- 出海-互联网
- 出海-安防
- 出海-跨境电商
- 量化
- 芯片
- 集团云、私有云
- 智算云
- 数据中心

Use the mappings in [references/industry-map.md](references/industry-map.md) for aliases, search hints, and watch points.

## Response Style

- Write in Chinese unless the user asks otherwise.
- Be decisive and commercial, not academic.
- Surface contradictions when the market signal is mixed.
- End with a short `方案更新建议` block when the task is tied to sales, pre-sales, or行业方案.
