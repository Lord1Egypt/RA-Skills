## Description:

Wraps ThemePica public financial data APIs for theme investment analysis, market hotspot rankings, ETF and fund narratives, and index data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyri](https://clawhub.ai/user/yyri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to call ThemePica public finance APIs for market themes, hotspot rankings, ETF, fund, and index narratives, and related market research context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested tickers, keywords, dates, and other query parameters to ThemePica's API with an APPCODE credential.

Mitigation: Use only data suitable for sharing with ThemePica, prefer THEMEPICA_APPCODE over storing a real key in mcp_config.json, and rotate credentials if they are exposed.

Risk: Financial narratives, rankings, signal labels, and market data can be incomplete, stale, or unsuitable as standalone investment advice.

Mitigation: Treat outputs as research data and analysis inputs, review them with qualified judgment, and avoid automated trading or client recommendations without additional controls.

## Reference(s):

- [ThemePica homepage](https://www.themepica.com)
- [ThemePica production API endpoint](https://data.api.themepica.com)
- [Theme API reference](references/themes.md)
- [Board API reference](references/board.md)
- [Hotspot API reference](references/hotspot.md)
- [Fund API reference](references/fund.md)
- [Index API reference](references/index.md)
- [ETF API reference](references/etf.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples plus JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a ThemePica APPCODE; responses depend on requested tickers, keywords, dates, pagination, and API availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
