## Description: <br>
面向中国A股研究场景的只读投研技能，提供行情、财务、行业、新闻、策略概览与量化选股查询；仅输出研究信息与风险提示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamsyb](https://clawhub.ai/user/williamsyb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill for read-only China A-share research, including market data, financial statements, sector context, news, strategy overviews, and quantitative stock screening. Outputs are research information with risk reminders, not trading instructions or personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a hosted RedQuant MCP endpoint. <br>
Mitigation: Install only when the configured hosted endpoint is trusted by the user, platform, or maintainer. <br>
Risk: Financial research output may be mistaken for buy, sell, or hold advice. <br>
Mitigation: Treat outputs as research information, include risk reminders, and avoid providing brokerage credentials, passwords, identity documents, or other sensitive personal data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamsyb/redquant-ashare-quant) <br>
- [MCP connection guide](artifact/references/mcp-connection-guide.md) <br>
- [RedQuant MCP tool catalog](artifact/references/tool-catalog.md) <br>
- [Usage examples](artifact/examples/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown responses with structured analysis, tool-derived data summaries, and risk disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only research output; no trade execution, fund movement, credential collection, or platform state changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
