## Description:

Use when the user asks to wire XRPL x402 pay-per-call or prepaid credits, hand off a stuck 402/settle flow to a human, draft an agent SOP for Ripple/t54-style facilitators, or package last-mile docs for XRPL agent payments without building a backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkarlsson00-spec](https://clawhub.ai/user/hkarlsson00-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to prepare XRPL x402 payment handoffs for pay-per-call or prepaid API access, including stuck verify/settle flows, spend ceilings, and human escalation. It produces a disciplined handoff block rather than custody logic or backend implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mainnet XRPL payments can move funds irreversibly if the facilitator, seller, amount, network, or recipient is wrong.

Mitigation: Verify those details independently, require explicit human approval for mainnet, and keep low per-call and per-session spend ceilings.

Risk: Wallet seeds or private keys could be exposed if copied into chat or generated output.

Mitigation: Keep seeds out of chat, use environment or KMS storage, and stop when seed exposure is suspected.

Risk: Retrying a failed verify/settle flow incorrectly can double-pay the same challenge.

Mitigation: On tx-not-found lag, wait briefly and retry the same X-PAYMENT header instead of submitting another payment.

## Reference(s):

- [Listing blurb](references/listing-blurb.md)
- [Protocol skill example facilitator](https://api.xrplfi.com/skill.md)
- [XRPL x402 catalog](https://api.xrplfi.com/catalog)
- [OSS facilitator/SDK](https://github.com/tekvyy/x402-xrpl)
- [t54-style XRPL x402 facilitator docs](https://xrpl-x402.t54.ai/)
- [XRPL agent wallet skills](https://xrpl.org/docs/agents/getting-started-with-agentic-transactions)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown structured handoff block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes network, facilitator, seller or origin URL, scheme, action, transaction or channel identifier, spend, handoff owner, prohibited actions, and next human step.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
