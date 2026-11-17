## Description:

Make x402 payments, pay for APIs, sell services, and handle 402 Payment Required responses with USDC on Base and other EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[primer-dev](https://clawhub.ai/user/primer-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to discover x402 payment requirements, confirm payment amounts, pay for protected APIs, check wallet balances, and configure services that charge through x402.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unpinned external packages that manage wallets or authorize payments.

Mitigation: Verify the package source and version before installation, prefer pinned versions, and run setup in an isolated environment when practical.

Risk: The skill can guide agents through transactions using private keys and stablecoin balances.

Mitigation: Use a dedicated low-balance wallet, keep private keys out of logs and chat, and confirm the destination and amount before every payment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/primer-dev/skills/xclaw02)
- [x402 protocol](https://x402.org)
- [Primer x402](https://primer.systems/x402)
- [xclaw02 npm package](https://npmjs.com/package/xclaw02)
- [xclaw02 PyPI package](https://pypi.org/project/xclaw02)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose payment, wallet, package-installation, and service-configuration actions that require user confirmation before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
