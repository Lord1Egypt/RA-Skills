## Description:

实时财经数据查询技能 - 支持A股、港股、美股、黄金、原油、VIX、美债等

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqiang243](https://clawhub.ai/user/xiaoqiang243)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query current market data for Chinese A-shares, Hong Kong shares, U.S. stocks, commodities, indexes, foreign exchange, and U.S. Treasury yields from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker queries are sent to third-party finance services.

Mitigation: Use the skill only when sharing requested finance symbols with Sina Finance or Yahoo Finance is acceptable.

Risk: Sina-backed data is fetched over an unencrypted HTTP endpoint.

Mitigation: Treat returned prices as informational and verify important trading or business decisions against trusted market data sources.

Risk: The optional `yfinance` dependency must be installed for Yahoo Finance-backed symbols.

Mitigation: Install `yfinance` from a trusted source in a virtual environment rather than globally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoqiang243/skills/realtime-finance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted text with inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns live quote summaries and error or dependency messages in Chinese.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
