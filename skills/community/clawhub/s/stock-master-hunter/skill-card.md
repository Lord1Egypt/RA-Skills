## Description:

World-first AI Skill fusing Elliott Wave Theory, volume-price dynamics, trend-cycle analysis, and 100-bagger fundamental screening. Captures breakout entry points and identifies 10x/100x potential stocks. Integrates IMA knowledge base, real-time market data, and backtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and investment analysts use this skill to turn an LLM agent into a stock-analysis assistant that combines technical analysis, 100-bagger screening, live market-data retrieval, and backtesting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to persist IMA API credentials for knowledge-base integrations.

Mitigation: Use platform-managed or environment-scoped secrets instead of persistent local credential files, and limit credentials to the minimum required scope.

Risk: The skill can update its own reference files and changelog during knowledge-base synchronization.

Mitigation: Require explicit user confirmation before sync operations and review generated reference-file or changelog changes before continuing to use the skill.

Risk: Market-data and investment-analysis outputs can be incomplete or misleading if live data is unavailable or stale.

Mitigation: Prefer current, user-approved market-data connectors; disclose data limitations in outputs; and keep the skill's own investment-risk disclaimer visible in generated analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjkj999999/skills/stock-master-hunter)
- [IMA agent interface](https://ima.qq.com/agent-interface)
- [IMA knowledge search API](https://ima.qq.com/openapi/wiki/v1/search_knowledge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, structured text diagrams, inline shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request or reference live market data, fundamentals, Fibonacci calculations, IMA knowledge-base search results, and user-provided historical data.]

## Skill Version(s):

2.1.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
