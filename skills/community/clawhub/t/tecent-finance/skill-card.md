## Description: <br>
Get stock prices, quotes, and compare stocks using Tencent Finance API with no API key required, supporting US stocks, China A-Shares, Hong Kong stocks, and major cryptocurrencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pz325](https://clawhub.ai/user/pz325) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to check market prices, request detailed quotes, compare tickers, and search stock or cryptocurrency symbols through Tencent Finance-backed CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Making or symlinking the tfin executable globally can expose users to the wrong executable if the source path is not verified. <br>
Mitigation: Confirm that tfin comes from the expected skill artifact before running chmod or creating a global symlink. <br>
Risk: Ticker searches and watchlist-like queries may be sent to Tencent Finance when commands are executed. <br>
Mitigation: Avoid using the skill for private watchlists or sensitive ticker query patterns if external market-data requests are a concern. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; command execution may query Tencent Finance for requested ticker symbols.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
