## Description: <br>
Global landed-cost calculator for traders shipping to the United States, combining tariff layers, exchange rates, ocean freight costs, compliance checks, and customs entry costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoningliu1-lang](https://clawhub.ai/user/zhaoningliu1-lang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External traders, import operators, and agents use this skill to estimate US landed costs from HTS codes, origin countries, cost of goods, shipping details, FX rates, tariff overlays, and customs fees. Outputs are informational and should be verified with a licensed customs broker or qualified trade counsel before business decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate local backend. <br>
Mitigation: Review the referenced backend repository before installing and run the service in an isolated environment. <br>
Risk: Optional FX and Freightos API keys may be provided to the backend. <br>
Mitigation: Provide only the API keys intended for this service and avoid sharing unrelated credentials. <br>
Risk: The backend can persist FX and shipping history in a local data directory. <br>
Mitigation: Keep the configured data directory away from sensitive files and use a dedicated path when possible. <br>
Risk: Tariff, AD/CVD, compliance, and landed-cost outputs may be incomplete or change over time. <br>
Mitigation: Treat outputs as informational and verify obligations with a licensed customs broker or qualified trade counsel before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoningliu1-lang/tariff-watch) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaoningliu1-lang) <br>
- [Backend Source Repository](https://github.com/zhaoningliu1-lang/tariff-watch) <br>
- [USITC HTS Schedule](https://hts.usitc.gov/) <br>
- [Frankfurter ECB Exchange Rates](https://www.frankfurter.app/) <br>
- [Commerce AD/CVD Reference](https://enforcement.trade.gov/antidumping/antidumping.html) <br>
- [CBP UFLPA Reference](https://www.cbp.gov/trade/forced-labor/UFLPA) <br>
- [ExchangeRate API](https://www.exchangerate-api.com/) <br>
- [Freightos API](https://www.freightos.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with endpoint calls, shell commands, and structured tariff or landed-cost summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON snippets from the local API; outputs are advisory and depend on backend data freshness.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
