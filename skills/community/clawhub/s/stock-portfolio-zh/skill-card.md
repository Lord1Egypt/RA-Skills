## Description: <br>
Creates and manages stock and crypto portfolios with AISA live pricing and profit/loss tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, update, list, rename, delete, and review local investment portfolios, including current value and profit/loss estimates from AISA live price lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio names, tickers, quantities, and cost basis are stored in a local JSON file. <br>
Mitigation: Use an appropriate local state directory, protect the file with normal filesystem permissions, and avoid entering sensitive account or credential data. <br>
Risk: Ticker symbols are sent to AISA when fetching live prices. <br>
Mitigation: Only request prices for tickers you are comfortable sharing with the configured AISA endpoint. <br>
Risk: AISA_BASE_URL can redirect price requests to a different endpoint. <br>
Mitigation: Keep AISA_BASE_URL unset unless you intentionally trust the alternate endpoint. <br>
Risk: Live prices are informational and may be incomplete or unsuitable for trading decisions. <br>
Mitigation: Treat returned prices and profit/loss estimates as informational, not trading-grade financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-portfolio-zh) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output; local portfolio state is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; stores portfolio names, tickers, quantities, and cost basis in a local JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
