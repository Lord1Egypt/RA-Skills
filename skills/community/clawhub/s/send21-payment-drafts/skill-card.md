## Description:

Create non-custodial payment drafts for agents while humans sign and broadcast from their own wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[send21io](https://clawhub.ai/user/send21io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare non-custodial payment drafts for human wallet review, local signing, and broadcast. It is for payment workflows where the agent may assemble draft details but must not control funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-prepared payment draft details could be approved without checking recipient, asset, network, amount, memo, wallet outputs, or fees.

Mitigation: Require the human signer to review every payment field, wallet output, and fee before signing or broadcasting from their own wallet.

Risk: Sharing seed phrases, private keys, wallet exports, or signing secrets with an agent or service can compromise funds.

Mitigation: Do not provide signing secrets to the agent or service; keep signing local in the user's own wallet.

Risk: Unsupported or ambiguous asset and network combinations can produce incorrect draft instructions.

Mitigation: Stop and ask for a supported asset and network combination instead of guessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/send21io/skills/send21-payment-drafts)
- [send21](https://send21.io)
- [send21 demo](https://send21.io/demo)
- [send21 MCP](https://send21.io/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text payment draft details for human review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts can include recipient, amount, asset, network, memo, expiry, or rate details; humans must verify wallet outputs and fees before signing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
