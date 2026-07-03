## Description: <br>
Multi-market intelligent stock selection for A-share, Hong Kong, US stocks, ETFs, and funds using AKShare-backed data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axjing](https://clawhub.ai/user/axjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for stock analysis, market scans, portfolio construction, factor screening, strategy signals, fund screening, backtesting, and investment diagnostics. It supports script-driven workflows that can return terminal text, JSON, or Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch public market data over the network, use Python finance packages such as AKShare, maintain a local cache, and write report files. <br>
Mitigation: Install and run it only in an approved environment, review generated files before relying on them, and confirm that network access and local caching fit the user's policy. <br>
Risk: Stock signals, rankings, and diagnostics can be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as research support, verify factor definitions and regional assumptions, and do not use the skill as personalized investment advice. <br>
Risk: Public market data sources can be delayed, rate-limited, or unavailable, which can affect scans and backtests. <br>
Mitigation: Check data freshness, disclose limitations in the final answer, and use cached or partial results only with clear caveats. <br>


## Reference(s): <br>
- [Source repository](https://github.com/axjing/stockaskill) <br>
- [AKShare official documentation](https://akshare.akfamily.xyz) <br>
- [AKShare GitHub repository](https://github.com/akfamily/akshare) <br>
- [AKShare PyPI package](https://pypi.org/project/akshare) <br>
- [Factor System](references/factors.md) <br>
- [Strategy System](references/strategies.md) <br>
- [Risk & Compliance](references/risk-and-compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports under ./reports and use local SQLite caching for market data.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
