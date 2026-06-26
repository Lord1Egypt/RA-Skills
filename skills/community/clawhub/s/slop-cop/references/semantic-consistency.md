# Semantic Consistency Checks

Slop-cop must validate that copy, charts, numbers, and visual direction tell the same story.

## Mandatory checks

- If copy says a metric is **trending down**, the visible line/bar/arrow must move down in the relevant direction.
- If copy says a metric is **trending up**, the visible line/bar/arrow must move up in the relevant direction.
- If copy claims improvement (lower CPL, higher ROAS, more calls), the dashboard/KPI visual must support that claim.
- If a label names a metric (CPL, ROAS, booked calls), the adjacent number/graph must plausibly match that metric.
- If a chart line is flat or slightly opposite of the claim, flag it. Do not excuse it as decorative if the copy uses it as evidence.
- If the graph has ambiguous axes or no direction labels, require either clearer visual direction or less specific copy.

## Verdict rules

- Copy contradicts visible data direction: `KILL` for shipping creative.
- Data visual is decorative but labeled as evidence: `FIX` by changing the graph or changing copy.
- Ambiguous data visual with generic copy: `FIX` if it could mislead; otherwise note as weak.

## Example hard kill

Visible card says: "Cost per lead trending down." The plotted line is sideways or slightly upward. Verdict: `KILL` — the visual evidence contradicts the claim.
