# Trading log schema

Append one JSON object per line.

## Minimum fields

- `date`
- `window`
- `action`
- `ticker`
- `qty`
- `price`
- `reason`
- `thesisInvalidation`
- `exitPlan`

## Recommended extra fields

- `dataStatus` — `complete`, `incomplete`, `estimated`
- `sourceNotes` — short source summary
- `style`
- `cashAfter`
- `equityAfter`
- `positionWeightAfter`
- `ruleCheck`

## Example HOLD

```json
{"date":"2026-03-12","window":"intraday","action":"HOLD","ticker":null,"qty":0,"price":null,"reason":"No clean setup after midday reversal.","thesisInvalidation":null,"exitPlan":null,"dataStatus":"complete","ruleCheck":"pass"}
```

## Example BUY

```json
{"date":"2026-03-12","window":"pre_or_open","action":"BUY","ticker":"NVDA","qty":12,"price":118.4,"reason":"AI infrastructure strength remains intact and setup is cleaner than alternatives.","thesisInvalidation":"Broad AI leadership fails and NVDA loses relative strength.","exitPlan":"Reduce or exit if thesis invalidates or position concentration becomes too high.","dataStatus":"complete","ruleCheck":"pass"}
```
