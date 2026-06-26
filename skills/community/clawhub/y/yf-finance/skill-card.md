## Description: <br>
Fetch real-time and historical financial data from Yahoo Finance using yf-cli for quotes, historical prices, company financials, earnings calendars, analyst recommendations, options chains, dividends, market screeners, and financial news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erhwenkuo](https://clawhub.ai/user/erhwenkuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to ask an agent for public market data and to have the agent run yf-cli commands for quotes, histories, financial statements, earnings, ownership, options, screeners, and news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the external yf-cli package through uv and make network requests for public financial data. <br>
Mitigation: Install only in environments where uv-based tool installation and public financial-data network access are acceptable. <br>
Risk: Returned market data may be delayed, incomplete, unavailable, or unsuitable for financial decision-making. <br>
Mitigation: Treat command output as informational market data, not financial advice, and verify important values against authoritative sources before acting. <br>
Risk: Strict supply-chain environments may require additional review of the external yf-cli package. <br>
Mitigation: Review the external yf-cli package source and dependency chain before deployment in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erhwenkuo/yf-finance) <br>
- [Command reference](references/commands.md) <br>
- [Output formats](references/output-formats.md) <br>
- [Worked examples](assets/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional table, JSON, or CSV command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require network access to retrieve public financial data and may install yf-cli through uv when the command is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
