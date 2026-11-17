## Description:

qieman-mcp helps agents query fund, strategy, announcement, and financial-news data; analyze asset allocation, portfolios, risk backtests, and cash flow; and generate charts or PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joey-lucky](https://clawhub.ai/user/joey-lucky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-application agents use this skill to access the qieman MCP service through qieman-mcp-cli for fund discovery, fund and strategy analysis, portfolio diagnostics, asset allocation analysis, market news lookup, chart rendering, and PDF generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can involve SMS login, API key handling, and personal profile details.

Mitigation: Complete login and SMS verification directly with the provider, avoid sharing SMS codes or API keys in agent chat, and verify the configured API key locally before use.

Risk: The initialization instructions recommend installing an unpinned global qieman-mcp-cli package.

Mitigation: Install a pinned, verified CLI version from a trusted registry before enabling the skill in shared or production environments.

Risk: Financial holdings, income, liabilities, family profile, and portfolio data may be sent to the external qieman MCP service.

Mitigation: Treat submitted financial and household data as shared with that service and avoid sending sensitive data unless the user has approved that disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joey-lucky/skills/qieman-mcp)
- [Initialization workflow](references/初始化工作流.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and links to generated chart or PDF assets when tools return them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external qieman MCP service and may return financial analysis, tabular summaries, rendered chart URLs, or PDF URLs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
