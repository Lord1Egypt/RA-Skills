## Description: <br>
Real-time financial data API for AI agents. Stocks, crypto, forex, ETFs. 120+ endpoints. Alternative to Alpha Vantage, CoinGecko. Works with Claude, Cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and finance-focused agent users use this skill to query PRISM for asset resolution, market prices, market overviews, token security checks, DeFi data, wallet balances, and cross-market intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance questions, market symbols, wallet addresses, and contract addresses may be sent to the external PRISM API provider. <br>
Mitigation: Use the skill only with a trusted PRISM provider, avoid submitting sensitive wallet addresses, and use a PRISM-specific API key. <br>
Risk: Broad prompts such as "what's trending" may activate this finance skill when the user's intent is ambiguous. <br>
Mitigation: Ask a clarifying question before invoking PRISM when the prompt does not clearly request finance or market data. <br>


## Reference(s): <br>
- [Strykr Prism on ClawHub](https://clawhub.ai/NextFrontierBuilds/strykr-prism) <br>
- [PRISM API base URL](https://strykr-prism.up.railway.app) <br>
- [Publisher profile](https://clawhub.ai/user/NextFrontierBuilds) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and concise natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external PRISM API endpoint and format returned finance data for the user.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
