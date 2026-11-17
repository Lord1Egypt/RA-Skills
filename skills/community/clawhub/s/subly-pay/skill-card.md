## Description:

Fetches paywalled HTTP 402 resources by automatically settling x402 Solana USDC payments from an agent wallet's Kamino vault yield, and helps manage the related Subly vault and owner approval flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yukikm](https://clawhub.ai/user/yukikm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch paid x402 resources, manage a Subly-funded payment vault, and route owner approvals for deposits or higher-value payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically spend from a crypto wallet using a downloaded client that is not pinned to a reviewed version.

Mitigation: Use a dedicated, low-balance wallet; keep the payment cap low; confirm every paid URL and price; and prefer a pinned or otherwise verified version of `@subly_fi/pay` before wallet-affecting commands.

Risk: Payment and deposit flows can move funds or require owner approvals.

Mitigation: Do not raise caps without user confirmation, paste approval links exactly as printed, and verify setup or approval status before claiming that an approval occurred.

Risk: The configured keypair path points to private wallet material.

Mitigation: Never read, print, or transmit the keypair file contents; share only public receipts or public wallet information when needed.

## Reference(s):

- [Subly payment protocol](https://github.com/SublyFi/subly-payment-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and SUBLY_DEMO_AGENT_KEYPAIR_PATH; payment commands can affect a Solana wallet and should use low caps.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
