# trip-planner — benchmark (iteration-1)

Method: 2 Chinese test cases, each run **with-skill** vs **baseline (no skill)**, bounded live web
search, agents told not to ask interactive questions (state assumptions instead). Both configs were
asked to save a standalone HTML so output-format is controlled — the real-world lift over "no skill"
is larger, since without the skill a user often gets prose/markdown rather than HTML at all.

| eval | config | auto-checks | check_html.py | tokens | time | size |
|---|---|---|---|---|---|---|
| chengdu (银发+亲子) | with_skill | **10/10** | pass | 105.1k | 6.7 min | 59.6 KB |
| chengdu | baseline | 5/10 | FAIL (2) | 51.0k | 4.4 min | 30.5 KB |
| xian (+高铁查询) | with_skill | **10/10** | pass | 102.5k | 6.8 min | 63.5 KB |
| xian | baseline | 5/10 | FAIL (2) | 44.2k | 2.9 min | 18.0 KB |

## Discriminating vs non-discriminating checks

- **Discriminating (skill wins):** themed hero header, embedded Leaflet/OSM map, map coordinates,
  POI four-field cards (到达/停留/票价/营业时间), rain Plan B. Baseline produced **none** of these in
  either case (no map at all).
- **Non-discriminating (both pass):** transport card, budget table, pre-departure checklist, honesty
  markers (以…为准 / 12306), advance-booking note. A competent baseline already does these for a decent
  itinerary — so the skill's unique lift is concentrated in the **standardized visual structure +
  map + themed header + guaranteed checker-clean HTML**, not in "remembering to include a budget".

## Qualitative

- chengdu with_skill: `theme-forest deco-glow` header, ≤2 主要点/day, panda base early Day 2, indoor
  Plan B per outdoor day, senior-friendly low-walking routing. Honest about unverified flight nos.
- xian with_skill: `theme-desert deco-glow` header; 北京西→西安北 高铁 as a transport card (G87
  07:00→11:21 ¥577.5起) **plus a full schedule table**, query-only, `以12306为准` on unverified fares;
  兵马俑 own day with 必订 callout; 回民街 clustered with city-center stops for dinner.

## Cost note

with_skill ≈ 2× tokens and time vs baseline — the price of live research + the full structured build.

## iteration-3 (2026-06-12) — Step-5 fix validation

After the v0.2 change (un-droppable 住宿备选 + extended checker), one full re-run of the chengdu
eval with the updated SKILL.md passed the extended checker **first try**: 3 `.hotel` cards with
评论体检 notes, honestly-labeled price estimates ("web_search 估价 · 未浏览器核实"), per-day budget
subtotals matching the day-meta chips. Replay of the new checker over all 6 historical artifacts:
the 4 with_skill outputs flip to FAIL exactly on the missing hotel section (the bug it was built to
catch), with zero false positives on budget/checklist; both baselines fail 3 checks.
Artifact: `examples/成都4日游行程.html` (this repo).
