## Description:

中国 A 股/港股只读数据查询与分析技能，将自然语言需求映射到 /stocks/... 数据接口，检索行情、基本面、指数和文本数据，并输出带风险提示的结构化分析结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[roamer-remote](https://clawhub.ai/user/roamer-remote)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query public China A-share and Hong Kong stock data, combine market, fundamental, index, and text signals, and produce research-oriented analysis reports. The skill is for data review and market research only; it does not place trades, promise returns, or provide personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags behavior beyond the stated /stocks-only boundary, including web/forum search and unspecified notification pushing.

Mitigation: Limit use to public stock-data analysis and treat notification pushing as disabled unless the destination is known and the user explicitly requests it.

Risk: Web, news, or forum searches may reveal the stocks or topics a user asks about to external providers.

Mitigation: Avoid entering sensitive watchlists or private strategies when search is enabled, and disclose that external search may be used for text signals.

Risk: The skill requires TAX_API_KEY credentials.

Mitigation: Provide TAX_API_KEY only through the platform environment setting and never paste or request the key in chat.

Risk: Market data may be historical, delayed, incomplete, or insufficient for high-confidence conclusions.

Mitigation: State data limits, cross-check market, fundamental, index, and text signals, and include that outputs are for research rather than investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roamer-remote/skills/stocks-query-base-skill)
- [Publisher profile](https://clawhub.ai/user/roamer-remote)
- [TAX API homepage](https://tax.yyyou.top/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured analysis sections and inline API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAX_API_KEY configured through the platform environment; outputs should include uncertainty and non-investment-advice risk language.]

## Skill Version(s):

0.2.2 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
