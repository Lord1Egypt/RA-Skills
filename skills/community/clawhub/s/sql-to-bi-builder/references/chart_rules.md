# Chart Rules

## Default Mapping
- No dimension + at least one metric: `kpi`
- Time dimension + metric(s): `line`
- One categorical dimension + one metric: `bar`
- One categorical dimension + multiple metrics: `grouped_bar`
- Multiple dimensions or low confidence: `table`

## Overrides
- If metadata `chart` is not `auto`, use metadata value directly.
- If no metric is detected, force `table`.

## Confidence Hints
Increase confidence when:
- time alias is explicit (`dt`, `date`, `day`, `week`, `month`)
- aggregate functions are explicit (`SUM`, `COUNT`, `AVG`, `MAX`, `MIN`)

Decrease confidence when:
- multiple non-time dimensions and many expressions
- window functions dominate select list
- union-heavy SQL blocks
