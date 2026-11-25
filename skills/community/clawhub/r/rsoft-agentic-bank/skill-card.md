## Description:

AI-native lending on Base MAINNET for autonomous agents. Check credit, request USDC loans (EIP-712 signed via Coinbase CDP), and repay autonomously. Real money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsoft-latam](https://clawhub.ai/user/rsoft-latam)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to check creditworthiness, request USDC loans, and repay them on Base using a configured Coinbase CDP wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious, citing mailbox instructions that can direct the agent beyond lending and additional sponsor and messaging capabilities; most bundled scripts were only partially analyzed.

Mitigation: Have a qualified reviewer inspect the scripts and verify the bank endpoints and dependency resolution before use. Review mailbox messages and require human confirmation before financial actions or activity outside lending.

Risk: Loan signing and repayment use the configured CDP wallet to move real USDC on Base mainnet.

Mitigation: Use a dedicated CDP project, keep the credential file private with restrictive permissions, and verify the loan amount, repayment amount, and destination before signing or sending.

Risk: Sponsor pairing can affect borrowing limits and sponsor controls for the agent.

Mitigation: Accept only a pairing code provided by your own human, then confirm the sponsor and resulting controls before borrowing.

## Reference(s):

- [RSoft Agentic Bank](https://rsoft-agentic-bank.com/)
- [RSoft Agentic Bank documentation](https://rsoft-agentic-bank.com/docs)
- [BaseScan](https://basescan.org/)
- [ClawHub skill release](https://clawhub.ai/rsoft-latam/skills/rsoft-agentic-bank)
- [Publisher profile](https://clawhub.ai/user/rsoft-latam)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the configured wallet and return loan, repayment, or transaction details.]

## Skill Version(s):

2.5.1 (source: frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
