## Description:

Cross-chain token swaps, quotes, portfolio and prices across 14 chains via the Suwappu DEX MCP server. Read-only by default; swap execution is opt-in and gated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xsoftboi](https://clawhub.ai/user/0xsoftboi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading agents use this skill to query cross-chain quotes, prices, portfolios, supported chains, supported tokens, and prediction-market data through Suwappu's hosted DEX MCP server. Swap execution is disabled by default and should be enabled only on a dedicated trading agent with explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to a third-party DEX service for portfolio and trading-related requests.

Mitigation: Install only when the user trusts Suwappu for those requests and keep the default read-only MCP setup unless trading is deliberately required.

Risk: Enabling execute_swap can allow fund-moving actions from a previously returned quote.

Mitigation: Enable execute_swap only on a dedicated trading agent with explicit allowlisting and require per-swap user confirmation.

Risk: The Suwappu API key grants access to the hosted MCP integration.

Mitigation: Provide SUWAPPU_API_KEY through an environment variable or secret reference and do not commit it to files.

## Reference(s):

- [Suwappu DEX skill page](https://clawhub.ai/0xsoftboi/skills/suwappu-dex)
- [Suwappu homepage](https://suwappu.bot)
- [Suwappu API documentation](https://api.suwappu.bot/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUWAPPU_API_KEY; read-only setup excludes execute_swap by default.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
