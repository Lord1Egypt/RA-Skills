# Lead Scoring - Mentality-Weighted Evaluation System

## Purpose

Score any lead from 0-100 using combined intelligence from all four mentalities. Use this when evaluating scraped leads, inbound inquiries, or deciding which prospect to prioritize.

## Scoring Categories

### 1. TERRAIN SCORE (Sun Tzu) - 25 points max

How defended is this prospect?

| Condition | Points |
|---|---|
| No website at all | 25 |
| Website exists but terrible (no mobile, broken, outdated) | 20 |
| Website exists, mediocre, clearly DIY | 15 |
| Website exists, decent but no AI/automation | 10 |
| Website exists, built by agency, looks professional | 5 |
| Website is strong, active agency relationship, satisfied | 0 |

### 2. ECONOMICS SCORE (Hormozi) - 25 points max

Is this lead worth the effort economically?

| Condition | Points |
|---|---|
| Business has visible revenue (busy location, staff, inventory) | 10 |
| Located in profitable sector (medical, legal, horeca, vastgoed) | 5 |
| No visible competitor already serving them | 5 |
| Can be served with existing templates/demos (low delivery cost) | 5 |

Subtract points:
| Condition | Deduct |
|---|---|
| Startup or pre-revenue | -10 |
| Sector with very low margins (non-profit, hobbyist) | -5 |
| Would require heavy custom work with no template | -5 |

### 3. RESPONSIVENESS SCORE (Dan Kennedy) - 25 points max

How likely is this lead to act?

| Condition | Points |
|---|---|
| They reached out to YOU (inbound) | 25 |
| They posted asking for help publicly (Facebook, forum) | 20 |
| They recently opened/rebranded (visible activity) | 15 |
| They have social media but post inconsistently | 10 |
| Cold lead, no signals of active need | 5 |
| Already rejected or ghosted before | 0 |

### 4. SPRINT ALIGNMENT SCORE (12 Week Year) - 25 points max

Does this lead fit the current execution plan?

| Condition | Points |
|---|---|
| Fits a current 12-week goal perfectly | 25 |
| Same sector as an active demo site | 20 |
| Same region, can be served with existing assets | 15 |
| Different sector but reachable with current tools | 10 |
| Requires building new demo/assets from scratch | 5 |
| Completely outside current focus | 0 |

## Total Score Interpretation

| Score | Action |
|---|---|
| 80-100 | DROP EVERYTHING. Contact within 24 hours. This is a high-value, undefended, responsive, aligned lead. |
| 60-79 | HIGH PRIORITY. Add to this week's outreach plan. Contact within 48 hours. |
| 40-59 | QUEUE. Add to pipeline, contact when bandwidth allows. Don't chase actively. |
| 20-39 | NURTURE. Add to long-term email/content list. Don't spend active time. |
| 0-19 | SKIP. Not worth the effort right now. Revisit only if circumstances change. |

## Quick Score Template

```
LEAD SCORE: [business name]
============================
Terrain (Sun Tzu):        __/25  [reason]
Economics (Hormozi):      __/25  [reason]
Responsiveness (Kennedy): __/25  [reason]
Sprint Alignment (12WY):  __/25  [reason]

TOTAL:                    __/100

ACTION: [DROP EVERYTHING / HIGH PRIORITY / QUEUE / NURTURE / SKIP]
NEXT STEP: [specific action + deadline]
```

## Batch Scoring

When scoring multiple leads (e.g., from a scraper output), sort by total score descending. Work top-down. Stop when weekly outreach capacity is filled. Remaining leads stay in queue for next week.

For automated scoring via API or scraper integration, map each condition to a boolean check where possible:
- Terrain: check if website exists (HTTP status), check Google PageSpeed score
- Economics: sector lookup from business category
- Responsiveness: check for recent social media activity, check if inbound
- Sprint alignment: match sector against current sprint goal list
