## Description: <br>
Stock Query helps agents retrieve real-time and historical quotes for stocks, ETFs, funds, and market indexes, including optional portfolio watchlist management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asfamilybank](https://clawhub.ai/user/asfamilybank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query stock, ETF, fund, and index prices, inspect historical K-line data, and manage a local watchlist or portfolio CSV on explicit request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call external finance data providers for quote and fund data. <br>
Mitigation: Install only when outbound requests to the disclosed finance providers are acceptable, and verify important market data with authoritative sources before acting on it. <br>
Risk: The local portfolio.csv may contain holdings and reference prices. <br>
Mitigation: Keep portfolio.csv limited to non-secret holdings data; do not store passwords, API keys, brokerage credentials, tokens, or account numbers in it. <br>
Risk: Fund estimates from HTTP-backed sources may be informational rather than final values. <br>
Mitigation: Treat fund estimates as informational and confirm final net asset values through official or brokerage sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asfamilybank/stock-query) <br>
- [Publisher profile](https://clawhub.ai/user/asfamilybank) <br>
- [Repository](https://github.com/asfamilybank/stock-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise text, with shell commands or CSV updates when the user explicitly requests portfolio management.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform outbound finance data lookups and may read or update a local portfolio.csv containing non-secret holdings data.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
