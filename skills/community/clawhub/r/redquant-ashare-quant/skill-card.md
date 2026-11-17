## Description:

面向中国A股研究场景的只读投研技能，提供行情、财务、行业、新闻、策略概览与量化选股查询；仅输出研究信息与风险提示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamsyb](https://clawhub.ai/user/williamsyb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to query China A-share market data, financial statements, industry context, news, strategy overviews, and quantitative stock-screening results through a read-only RedQuant hosted MCP service. Outputs are research information with risk notices, not trading execution or personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may be sent to the RedQuant hosted MCP endpoint.

Mitigation: Confirm the endpoint is trusted before installation and avoid sending sensitive identity, credential, or account information.

Risk: Financial research outputs may be mistaken for trading instructions or personalized investment advice.

Mitigation: Use outputs as research only, keep risk disclaimers visible, and do not use the skill to execute trades or make account-level decisions.

Risk: Strategy subscription and product-description content can influence commercial decisions.

Mitigation: Present strategy information neutrally, avoid return promises, and limit strategy details to user-facing safe profiles rather than internal parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamsyb/skills/redquant-ashare-quant)
- [MCP connection guide](references/mcp-connection-guide.md)
- [RedQuant MCP tool catalog](references/tool-catalog.md)
- [Usage examples](examples/usage-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured analysis, tables, risk notices, and optional MCP configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research responses are grounded in read-only MCP tool results; public web search may be used only as a clearly labeled supplemental source.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
