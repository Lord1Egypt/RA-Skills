## Description:

Use this skill when the user wants a single approved onchain order for a Solana wallet, one explicit forbidden order, a quote-backed execution preview, or a receipt-backed daily debrief powered by OKX OnchainOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Solana wallet use this skill to turn wallet posture and market context into one daily onchain order decision, one explicit forbidden order, and a quote-backed execution preview. If execution is requested, the skill requires final user approval before broadcast and closes with a preview or receipt-backed debrief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides financial decision support for Solana onchain trading and may surface incorrect, stale, or unsuitable order guidance.

Mitigation: Treat the approved order as decision support, verify wallet posture, market context, quotes, routes, and slippage before acting, and decline unclear setups with a watch-only stance.

Risk: A prepared transaction could be broadcast unintentionally if the user does not distinguish preview from execution.

Mitigation: Keep execution details labeled as preview until final approval, and require explicit user approval before using Broadcast / Status.

Risk: Wallet review requires reading a Solana wallet address and portfolio state.

Mitigation: Use only the wallet address needed for the task, never request private keys or seed phrases, and ask for the address when none is provided.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard7463/skills/todays-orders)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown with wallet summary, approved order, forbidden order, execution preview, and debrief sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses quote and receipt data when available; labels execution details as preview until execution is approved and confirmed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
