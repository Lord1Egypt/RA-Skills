## Description:

Tariff Watch Clean helps traders estimate U.S. landed cost by combining live USITC tariff lookups, duty overlays, exchange rates, freight costs, compliance checks, and customs entry costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoningliu1-lang](https://clawhub.ai/user/zhaoningliu1-lang)

### License/Terms of Use:

MIT

## Use Case:

External traders, importers, ecommerce operators, and developers use this skill to estimate U.S. landed costs for products shipped from global origins into the United States. It supports tariff, freight, exchange-rate, customs-entry, and compliance-aware cost analysis before sourcing or pricing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tariff, trade-law, exchange-rate, and freight data are time-sensitive and may differ from official determinations or current market conditions.

Mitigation: Treat outputs as estimates and verify obligations with CBP sources, a licensed customs broker, or qualified trade counsel before making import or pricing decisions.

Risk: The skill requires a separate local backend and can fetch data from external tariff, exchange-rate, and freight sources.

Mitigation: Review the backend source and dependencies before running it, and only install it in an environment where external data access is acceptable.

Risk: Optional premium providers require API keys, and some free exchange-rate or freight values may be simulated or calibrated.

Mitigation: Use limited-scope API keys where possible, check response data-source indicators, and enable premium providers when exact provider-backed rates are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaoningliu1-lang/skills/tariff-watch)
- [Project Homepage](https://github.com/zhaoningliu1-lang/tariff-watch)
- [USITC HTS Search](https://hts.usitc.gov/)
- [Frankfurter Exchange Rates](https://www.frankfurter.app/)
- [ExchangeRate-API](https://www.exchangerate-api.com/)
- [Freightos API](https://www.freightos.com/api/)
- [Commerce AD/CVD Reference](https://enforcement.trade.gov/antidumping/antidumping.html)
- [CBP UFLPA Entity List](https://www.cbp.gov/trade/forced-labor/UFLPA)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP endpoint examples, shell commands, and concise trade-cost guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local FastAPI backend at http://localhost:8000; optional API keys enable premium exchange-rate and freight providers.]

## Skill Version(s):

3.2.0 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
