## Description:

Use for gasless non-custodial EVM market, limit, TWAP, stop-loss, take-profit, delayed-start swaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eranp-orbs](https://clawhub.ai/user/eranp-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn swap intent into normalized params, EIP-712 typed data, approval guidance, signatures, relay submissions, order queries, and exact-match cancellation for supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help prepare and submit real token swap orders.

Mitigation: Review every chain, token, amount, limit, deadline, recipient, allowance, and relay destination before approving, signing, or submitting.

Risk: Changed order fields can make a previous signature unsafe or invalid for the current intent.

Mitigation: Do not reuse signatures after changing order fields; sign only the exact populated typed data intended for submission.

Risk: Token approval can authorize spend of the input token.

Mitigation: Use the default exact approval for input.maxAmount unless the user explicitly chooses a standing approval for repeat use.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [Params](references/params.md)
- [Template, Sign, And Submit](references/sign.md)
- [Lifecycle](references/lifecycle.md)
- [Examples](references/examples.md)
- [RePermit Template](assets/repermit.template.json)
- [Common Token Addressbook](assets/token-addressbook.md)
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)
- [Supported Chains Configuration](https://github.com/orbs-network/spot/blob/master/config.json)
- [Order Submission Relay](https://agents-sink.orbs.network/orders/new)
- [Order Query Relay](https://agents-sink.orbs.network/orders)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces locally populated order parameters, EIP-712 typed-data guidance, approval instructions, signed relay payload guidance, query commands, and cancellation steps.]

## Skill Version(s):

2.5.5 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
