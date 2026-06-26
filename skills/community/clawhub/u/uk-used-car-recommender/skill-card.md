## Description: <br>
Your smart used-car buying advisor for the UK market. Recommends second-hand cars based on budget, reliability, mileage, service history, depreciation, and running costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hifinan](https://clawhub.ai/user/hifinan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get UK used-car buying guidance, including model recommendations, live listing research, running-cost checks, MOT and HPI due diligence, and photo-based screening support. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches external car sites and may fetch listing images, which can expose user search criteria or location preferences to those services. <br>
Mitigation: Install dependencies in a virtual environment, use only the location precision the user is comfortable sharing, and disclose external listing or image lookups before running them. <br>
Risk: Listing, photo, MOT, HPI, service-history, and seller information can be incomplete, stale, or misleading. <br>
Mitigation: Treat AI analysis as screening help only and independently verify MOT records, HPI status, service history, seller identity, vehicle condition, and paperwork before purchase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hifinan/uk-used-car-recommender) <br>
- [Data-Driven Recommendation Guide](docs/DATA_DRIVEN_RECOMMENDATION.md) <br>
- [Gumtree CLI Search Guide](docs/GUMTREE_SEARCH.md) <br>
- [AutoTrader Integration Guide](docs/AUTOTRADER_INTEGRATION.md) <br>
- [UK Used Car Market Reference](docs/UK_MARKET_REFERENCE.md) <br>
- [Used Car Image Analysis Guide](docs/IMAGE_ANALYSIS_GUIDE.md) <br>
- [AutoTrader UK](https://www.autotrader.co.uk/) <br>
- [AutoTrader Connect API](https://developers.autotrader.co.uk/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown with structured recommendation cards, comparison tables, listing summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market-search results and listing-photo screening observations when the required search tools and network access are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
