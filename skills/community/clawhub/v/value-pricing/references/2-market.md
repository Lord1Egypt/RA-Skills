# Market references and alternatives

Use this phase when comparable market evidence can inform the decision. A market reference describes observed offers and terms; it is not necessarily a transaction price, a measure of customer value, or a causal premium.

## Collect comparable evidence

Start with alternatives named by the user and expand only as useful to the decision. Record the source, observed date, geography, audience, included scope, unit, billing period, conditions, discounts, and whether the price is public, quote-based, or unavailable. Keep different offer types separate when they cannot be compared meaningfully.

For structured analysis, define a custom taxonomy only when the offers share comparable attributes. Those can describe capabilities, service scope, quality, delivery, access, capacity, or commercial terms. Record unknown or unclear separately from absent. Avoid coding a vendor's silence as proof that it does not offer something.

Use the CSV templates as blank schemas. Do not invent competitor prices, controls, attributes, or terms. Respect access conditions and site policies; use manual or supplied evidence when automated collection is inappropriate.

## Choose an analysis suited to coverage

- With a small or heterogeneous set, provide a sourced descriptive comparison and explain the limits.
- With sufficiently comparable offers, consider price-per-unit summaries or hedonic analysis. Check sample coverage, attribute prevalence, collinearity, and support before interpreting coefficients.
- Treat regression coefficients as associations unless the research design identifies causality. Co-occurring attributes and strategic pricing can confound apparent premiums.
- Do not extrapolate beyond observed offer combinations without a clear warning. Use in-support comparables and sensitivity checks.

The included `hedonic.py`, `value_metric.py`, coding, and agreement scripts support specific structured market analyses. Their input schemas must be configured for the study. They are optional and should be skipped when comparability or evidence is inadequate.

## Report

State which offers were included and excluded, how terms were normalized, what was missing, and how representative the evidence is. Separate observed prices from estimates. Report uncertainty and extrapolation risk; do not convert an association into an attribute's causal value.
