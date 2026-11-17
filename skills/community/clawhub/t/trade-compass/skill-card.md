## Description:

Global landed cost calculator for traders shipping to the US. Combines live USITC tariffs, Section 232/301/AD-CVD duties, real-time exchange rates (ECB), ocean freight costs, UFLPA compliance, and customs entry fees into a single per-unit cost. Supports 18+ origin countries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoningliu1-lang](https://clawhub.ai/user/zhaoningliu1-lang)

### License/Terms of Use:

MIT

## Use Case:

External traders, importers, ecommerce operators, and their agents use this skill to estimate US landed cost per unit from HTS code, origin country, local cost of goods, freight, exchange rates, customs entry costs, and compliance warnings. Outputs should be treated as decision support and verified with a licensed customs broker or qualified trade counsel before making import decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade-cost, tariff, and compliance results may be incomplete, stale, or unsuitable as final customs advice.

Mitigation: Use the outputs as business and legal decision support only, and verify obligations with a licensed customs broker or qualified trade counsel.

Risk: The skill can use optional Freightos or exchange-rate API keys and external data services.

Mitigation: Review the linked backend source and provide optional API keys only when comfortable with those providers and their terms.

## Reference(s):

- [Trade Compass ClawHub Page](https://clawhub.ai/zhaoningliu1-lang/skills/trade-compass)
- [Backend Source](https://github.com/zhaoningliu1-lang/tariff-watch)
- [ExchangeRate-API](https://www.exchangerate-api.com/)
- [Freightos API](https://www.freightos.com/api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, JSON, Guidance]

**Output Format:** [Markdown summaries with API request examples and JSON-derived tariff, freight, exchange-rate, compliance, and landed-cost breakdowns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local FastAPI backend on http://localhost:8000; optional Freightos and exchange-rate API keys can improve data coverage.]

## Skill Version(s):

3.2.0 (source: release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
