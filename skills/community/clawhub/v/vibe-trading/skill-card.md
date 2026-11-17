## Description:

A finance research toolkit for strategy backtesting, factor and options analysis, market data, trade-journal insights, and research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warren618](https://clawhub.ai/user/warren618)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers can use the agent to explore market data, analyze strategies and factors, backtest ideas, review trade journals, and produce research reports or strategy artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved brokerage credentials and confidential research could be exposed if handled carelessly or shared with unapproved model providers.

Mitigation: Protect saved credentials and use an approved model provider before supplying confidential research to swarm workers.

Risk: Session MCP injection or direct trade-writing tools can grant broader tool access than intended.

Mitigation: Keep session MCP injection and direct trade-writing tools disabled unless deliberately authorized; start with research or paper/read-only connections.

Risk: The external Python package was not audited, so instruction-level scan results do not establish runtime enforcement.

Mitigation: Review the package and its runtime controls before relying on them for brokerage or other sensitive workflows.

## Reference(s):

- [Vibe Trading on ClawHub](https://clawhub.ai/warren618/skills/vibe-trading)
- [Publisher profile](https://clawhub.ai/user/warren618)
- [Gildata DataMap](https://www.gildata.com/products/datamap)
- [IBKR public MCP endpoint](https://api.ibkr.com/v1/api/mcp-public)
- [eToro Public API MCP](https://mcp.public-api.etoro.com)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Configuration, Markdown, HTML/PDF reports]

**Output Format:** [Markdown guidance and analysis, strategy code and configuration files, and generated HTML/PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backtest metrics, market research, factor analysis, options calculations, and trade-journal summaries.]

## Skill Version(s):

0.1.19 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
