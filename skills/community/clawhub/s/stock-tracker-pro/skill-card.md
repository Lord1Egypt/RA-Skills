## Description: <br>
Stock Tracker Pro helps agents manage a stock watchlist, retrieve Yahoo Finance quote data, and show recent company news for requested symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongbhuang](https://clawhub.ai/user/hongbhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can ask an agent to add or remove ticker symbols, list a local watchlist, or fetch current quote details and recent news for a stock. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols and company names queried through the skill may be sent to Yahoo Finance and a separate local Tavily/search helper for news lookup. <br>
Mitigation: Install only if those external lookups are acceptable, and review the Tavily/search helper separately before relying on news results. <br>
Risk: The local stock watchlist is stored as JSON in the skill directory. <br>
Mitigation: Avoid adding sensitive or private watchlist entries unless local file storage is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [Stock Tracker Pro on ClawHub](https://clawhub.ai/hongbhuang/stock-tracker-pro) <br>
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/) <br>
- [Yahoo Finance quote endpoint](https://query1.finance.yahoo.com/v7/finance/quote) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stock symbols are passed as command arguments, and the watchlist is stored as JSON in the skill directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
