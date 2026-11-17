## Description:

Multi-agent stock trading signal analysis framework with a two-round debate process that analyzes a stock ticker and produces a BUY, SELL, or HOLD recommendation with rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate stock research agents that gather fundamentals, market data, news, and sentiment, then synthesize a debate-backed investment report. The output is decision-support material and should not be treated as personal financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated BUY, SELL, or HOLD recommendations may be mistaken for personal financial advice.

Mitigation: Treat reports as decision-support only; review assumptions, cited sources, and saved reports before relying on the output.

Risk: The skill uses Tushare and web-search services and requires sensitive API tokens.

Mitigation: Install dependencies in an isolated environment and keep API tokens in environment variables only.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laigen/skills/stock-trading-agents-light)
- [Tushare Pro Registration](https://tushare.pro/register)
- [Fundamental Analyst Prompt](references/fundamental-analyst.md)
- [Market Analyst Prompt](references/market-analyst.md)
- [News Analyst Prompt](references/news-analyst.md)
- [Social Media Analyst Prompt](references/social-analyst.md)
- [Bull Researcher Prompt](references/bull-researcher.md)
- [Bear Researcher Prompt](references/bear-researcher.md)
- [Research Manager Prompt](references/research-manager.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown investment report with supporting analyst reports, debate history, and local report file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes BUY, SELL, or HOLD recommendation; writes reports to ~/.openclaw/workspace/memory/reports/trading-agents-*.md]

## Skill Version(s):

2.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
