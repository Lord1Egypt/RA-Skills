## Description:

A股多智能体 AI 投研分析工具 uses 15 AI analysts to analyze China A-share stocks across technical, fundamental, sentiment, smart-money, macroeconomic, and game-theory perspectives, producing structured buy, sell, or hold recommendations with risk assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinmountain](https://clawhub.ai/user/kylinmountain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment researchers use this skill to request deep analysis of Shanghai and Shenzhen A-share stocks by symbol or Chinese company name. The skill submits stock-analysis jobs to the TradingAgents API and returns structured decisions, confidence, target and stop-loss prices, key metrics, and risk items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send stock-analysis requests and a bearer token to a configurable backend API endpoint.

Mitigation: Use the default HTTPS endpoint or an HTTPS self-hosted endpoint, avoid plain HTTP except loopback-only local testing with disposable credentials, and rotate the TradingAgents token if exposed.

Risk: The skill produces investment-analysis recommendations that may be incorrect, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as decision support, require user confirmation before submitting jobs, and review recommendations with independent financial judgment before acting.

Risk: Users may include personal account details, actual positions, or other sensitive financial information in prompts even though the skill only needs stock-analysis parameters.

Mitigation: Ask users to provide only stock symbols, trade dates, and analysis horizons; do not include account data, holdings, or other sensitive personal information.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kylinmountain/skills/tradingagents-analysis)
- [TradingAgents application homepage](https://app.510168.xyz)
- [TradingAgents-AShare self-hosting documentation](https://github.com/KylinMountain/TradingAgents-AShare)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis jobs usually take 1 to 5 minutes; batch mode submits multiple symbols and returns a JSON result summary for completed jobs.]

## Skill Version(s):

0.6.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
