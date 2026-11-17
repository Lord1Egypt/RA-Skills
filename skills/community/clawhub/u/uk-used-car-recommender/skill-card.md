## Description:

A UK used-car buying advisor that recommends second-hand cars using budget, reliability, mileage, service history, depreciation, running costs, and live listing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hifinan](https://clawhub.ai/user/hifinan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research UK used-car options, compare budget-fit models, inspect listing evidence, and plan due diligence before buying.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Live listing searches may disclose budget, vehicle preferences, city, or postcode to marketplace websites.

Mitigation: Use the minimum location precision needed, avoid sharing unnecessary personal details, and disclose that searches contact external marketplaces.

Risk: Python dependencies and optional scraper packages can change or introduce supply-chain risk.

Mitigation: Install in an isolated Python environment and review or pin dependencies before running package installation commands.

Risk: Image-based condition checks, market hotness scores, and sales-speed estimates can be incomplete or wrong.

Mitigation: Treat these outputs as advisory and verify important details with MOT history, HPI checks, seller records, and in-person inspection.

Risk: Live marketplace data can be stale, incomplete, or affected by site changes.

Mitigation: Cross-check recommendations against current listings and confirm vehicle details directly with the seller before making buying decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hifinan/skills/uk-used-car-recommender)
- [Data Driven Recommendation Guide](docs/DATA_DRIVEN_RECOMMENDATION.md)
- [AutoTrader Integration Guide](docs/AUTOTRADER_INTEGRATION.md)
- [Gumtree Search Guide](docs/GUMTREE_SEARCH.md)
- [UK Market Reference](docs/UK_MARKET_REFERENCE.md)
- [Workflow Guide](docs/WORKFLOW_GUIDE.md)
- [Image Analysis Guide](docs/IMAGE_ANALYSIS_GUIDE.md)
- [AutoTrader UK](https://www.autotrader.co.uk/)
- [AutoTrader Connect API](https://developers.autotrader.co.uk/api)
- [autotrader_scraper](https://github.com/suhailidrees/autotrader_scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown recommendations, comparison tables, listing summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live marketplace links, advisory risk warnings, and photo-condition observations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
