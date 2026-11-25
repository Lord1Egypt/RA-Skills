# Sub-agent research brief

Spawn one sub-agent per thesis, all in the same turn so they run in parallel.
Give each the brief below, filled in. Sub-agents do not see the main
conversation, so the brief must stand alone.

Suggested limits: about 10 minutes and a report of 800 to 2,000 words. Longer
reports are allowed for structural theses but must start with the summary
table.

```
You are researching one trading thesis for a research report. You are not
giving personal financial advice.

THESIS: <one sentence>
HORIZON: <tactical | medium | structural>
EVIDENCE SO FAR: <3-5 dated bullets from the macro scan>
COUNTER-EVIDENCE SO FAR: <2+ dated bullets>
WHAT WOULD KILL IT: <event / level>
USER CONSTRAINTS: <markets the user can trade, instruments allowed or
excluded (e.g. no options, no leverage), base currency>
TODAY: <date, timezone>

Do:
1. Test the thesis. Look for data that contradicts it as hard as data that
   supports it. If the thesis looks wrong, say so plainly; that is a useful
   result.
2. Find 3-6 candidate instruments (stocks, ETFs, hedges). For each: what it
   is, why it expresses the thesis, liquidity, current price with timestamp
   and source, valuation vs. peers, upcoming catalysts with dates.
3. For each candidate propose an invalidation level (stop) and the reasoning
   behind it, a target range, and a time stop.
4. List binary events inside the horizon (earnings, data, policy meetings).
5. Name the instrument that would profit if the thesis is wrong.

Return, in this order:
- SUMMARY TABLE: instrument | role (core/variant/hedge) | price @ time | stop |
  target | horizon | key catalyst | confidence 1-5
- VERDICT on the thesis: holds / weakened / broken, with the two strongest
  reasons each way
- DETAIL per instrument
- RISKS and the event calendar
- SOURCES with dates. Mark anything older than 7 days as stale.
```

When reports come back, the main agent:
- checks every price and date the synthesis will rely on (one quick lookup
  each), because sub-agent numbers can be wrong or stale;
- drops instruments that fail the risk rules in `SKILL.md`;
- keeps the sub-agent's "thesis is wrong" findings visible in the synthesis.
