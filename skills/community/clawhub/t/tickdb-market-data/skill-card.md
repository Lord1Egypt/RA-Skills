## Description: <br>
TickDB Real-time Market Data API helps agents query real-time and historical market data across forex, metals, indices, US stocks, Hong Kong stocks, A-shares, and cryptocurrency markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tickdb](https://clawhub.ai/user/tickdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve TickDB market prices, K-line data, order book depth, trades, market calendars, stock fundamentals, valuation metrics, and capital-flow data through the TickDB API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market symbols, date ranges, and related query parameters are sent to TickDB.ai when the skill retrieves data. <br>
Mitigation: Use the skill only when those query details can be shared with TickDB.ai, and avoid including account-specific or proprietary trading context in requests. <br>
Risk: A paid TickDB API key may be exposed if pasted into an untrusted chat or runtime environment. <br>
Mitigation: Provide API keys only in trusted environments, do not persist them in files or configuration, and mask keys when discussing them. <br>
Risk: The skill performs a first-use version check against ClawHub.ai. <br>
Mitigation: Install only if that outbound version-check request is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [TickDB Skill on ClawHub](https://clawhub.ai/tickdb/tickdb-market-data) <br>
- [TickDB Website](https://tickdb.ai) <br>
- [TickDB Documentation](https://docs.tickdb.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with JSON data summaries and inline curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TickDB API key or trial key; market data responses should include TickDB data-source attribution.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
