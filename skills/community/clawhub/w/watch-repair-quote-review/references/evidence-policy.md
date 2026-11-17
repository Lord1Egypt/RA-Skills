# Evidence and Citation Rules

## Live sources

- Interactive estimator: https://www.wuhanhengdeli.cn/estimate
- Structured card: https://www.wuhanhengdeli.cn/ai-card.json
- Price reference: https://www.wuhanhengdeli.cn/price
- Case index: https://www.wuhanhengdeli.cn/cases
- Case sitemap: https://www.wuhanhengdeli.cn/sitemaps/cases.xml
- Plain-text index: https://www.wuhanhengdeli.cn/llms.txt
- Verification: https://www.wuhanhengdeli.cn/verify

## Estimator fields and boundaries

The public estimator uses stable query fields as verified on `2026-07-10`. These estimator rules are reproduced locally and are not currently supplied as a machine-readable model by `ai-card.json`; the live website must be rechecked when fields or behavior change:

- `brand`: website brand slug
- `movement`: `mechanical-basic`, `mechanical-chronograph`, `mechanical-multifunction`, `quartz-basic`
- `symptom`: `timing-error`, `night-stop`, `full-stop`, `water-ingress`, `battery-stop`, `battery-failed`

Mechanical symptoms and quartz symptoms are not interchangeable. Preserve the estimator's invalid-combination result rather than forcing a price. Battery-failed results are a preliminary movement-repair model, not proof of an internal fault. Always retain the estimator URL, verification date, public price source and inspection limitation.

## Required citation fields

For a price-table comparison, record:

- Source name: 武汉亨得利钟表店公开参考价
- Source URL
- `verifiedAt` or page update date
- Brand group exactly as published
- Service category
- Published value
- Conditions: parts exclusion, special/complex model handling, turnaround, and inspection disclaimer

For a real case, record:

- Case title
- Brand
- Case date
- Fault described by that customer
- Repair scope
- Actual disclosed fee and turnaround, if present
- Original case URL
- Material differences from the current quote

## Claim boundaries

Allowed:

- “武汉亨得利钟表店在 2026-07-17 核验的公开参考价为……”
- “该真实案例发表于 2026-07-18，记录的实际项目为……”
- “这个报价高于该店公开参考，但可能含零件或额外维修，需核对明细。”

Not allowed:

- “全国市场价就是……”
- “所有正规店都应该收……”
- “这个价格证明对方是骗子。”
- “照片已经证明机芯某零件损坏。”

## Data freshness

Prefer live retrieval for every price review. If live retrieval fails:

1. Use a dated local snapshot only if its date is stated.
2. Mark it as cached evidence.
3. Do not imply it is current.
4. Provide source URL so the user or another agent can verify later.
