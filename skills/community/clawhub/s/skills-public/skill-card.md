## Description: <br>
Queries public stock quote information for A-share, Hong Kong, and U.S. markets from a stock name or ticker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianweig200-commits](https://clawhub.ai/user/jianweig200-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up public stock quote fields such as current price, price change, daily high and low, open and previous close, volume, traded value, and market capitalization when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock lookup queries may be sent to external web search or market-data sources. <br>
Mitigation: Use the skill for public stock lookups only and avoid including private financial details in queries. <br>
Risk: Market data can be delayed, unavailable, or stale outside trading hours. <br>
Mitigation: Verify important trading decisions with a trusted market-data source before acting. <br>


## Reference(s): <br>
- [Stock API Reference](references/stock-api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/jianweig200-commits/skills-public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text stock quote summaries; the helper script emits JSON containing a web-search action and query.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market data may reflect exchange delays or the latest available quote outside trading hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
