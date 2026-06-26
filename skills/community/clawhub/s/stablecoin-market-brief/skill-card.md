## Description: <br>
Gets real-time stablecoin market overviews from Barker, including total and yield-bearing market cap, asset and chain distribution, and market-wide APY statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to fetch and summarize current stablecoin market size, TVL distribution, chain distribution, and APY trends from Barker's public API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Barker's public API for crypto-market data. <br>
Mitigation: Install and use it only where outbound requests to Barker are acceptable. <br>
Risk: Stablecoin market summaries may be mistaken for financial advice. <br>
Mitigation: Treat responses as third-party crypto-market information and review them before acting on investment or treasury decisions. <br>
Risk: A generic market-overview query may activate this skill when another market analysis was intended. <br>
Mitigation: Confirm that the user is asking about stablecoins before relying on the generated brief. <br>


## Reference(s): <br>
- [Stablecoin Market Brief on ClawHub](https://clawhub.ai/zuoyeweb3/stablecoin-market-brief) <br>
- [Barker](https://barker.money) <br>
- [Barker Stablecoin Market API](https://api.barker.money/api/public/v1/stablecoin-market) <br>
- [Barker Stablecoin APY Trend API](https://api.barker.money/api/public/v1/stablecoin-apy-trend?days=90) <br>
- [Barker Public API Base](https://api.barker.money/api/public/v1) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with market figures, ranked distributions, APY trend commentary, and source attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Barker API responses; no credentials or privileged actions are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
