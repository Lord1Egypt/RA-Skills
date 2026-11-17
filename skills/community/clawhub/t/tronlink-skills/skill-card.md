## Description:

AI Agent skills for TronLink wallet management, token queries, market data, DEX swap quotes, Energy and Bandwidth resource management, and TRX staking information on the TRON network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbsyaya](https://clawhub.ai/user/bbsyaya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill set to have an agent query and explain TRON wallet balances, TRC-20 holdings, token metadata, market data, swap quotes, resource costs, and staking information. The documented workflows focus on read-only TRON data access and command guidance rather than transaction signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the release installs and exposes a broader persistent TRON tool suite than the wallet-focused description implies.

Mitigation: Review the artifact before installing and prefer running specific wallet commands locally from a reviewed copy; avoid global MCP or agent integrations unless the full TRON suite should be available across sessions and projects.

Risk: The security review says configured API keys can leak to non-TronGrid services.

Mitigation: Do not set TRONGRID_API_KEY or TRONSCAN_API_KEY until credential handling is fixed; use unauthenticated read-only queries where acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbsyaya/skills/tronlink-skills)
- [TronGrid](https://trongrid.io)
- [TRON Resource Model](docs/resource-model.md)
- [TRON Staking Guide](docs/staking-guide.md)
- [Claude Integration Guide](docs/claude-integration-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance covers wallet, token, market, swap quote, resource, and staking queries; documentation describes the operations as read-only.]

## Skill Version(s):

1.0.1 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
