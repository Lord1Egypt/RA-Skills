## Description:

TrollBridge guides agents through pay-per-call crypto market intelligence, token safety screens, and scam checks using USDC payments via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-tijerina](https://clawhub.ai/user/eric-tijerina)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to request paid crypto market data and heuristic token, contract, and scam screens before making decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls may charge unexpected amounts if prices or recipients change.

Mitigation: Review each HTTP 402 quote, including amount and recipient, before signing a payment.

Risk: Heuristic safety screens and audit-related outputs may miss threats or overstate safety.

Mitigation: Treat verdicts as screening signals, not guarantees or substitutes for independent review.

Risk: The stale backup file includes an MCP install command that could fetch unpinned code.

Mitigation: Do not follow the backup-file install command unless the source is pinned and trusted.

## Reference(s):

- [TrollBridge on ClawHub](https://clawhub.ai/eric-tijerina/skills/trollbridge)
- [TrollBridge API](https://mini-tollbooth.onrender.com)
- [x402 payment documentation](https://x402.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with HTTP request examples; API responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid requests require a quoted USDC payment; free health and tool-directory endpoints are available.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
