## Description:

Paid demo skill for StablePay on Solana using USDC. Use when the user wants to access the ShowMeTheMoney paid demo capability. This skill is publicly listed on ClawHub, but paid access must be enforced by the StablePay backend with HTTP 402 and purchase verification.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[bubblevan](https://clawhub.ai/user/bubblevan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to access a paid ShowMeTheMoney demo through StablePay on Solana using USDC. The paid capability should only continue after the backend confirms purchase verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact a third-party payment and execution backend during installation or use.

Mitigation: Review before installing and only use the skill if contacting wenfu.cc and StablePay is acceptable.

Risk: The skill uses an unresolved merchant identity for a real-money Solana Mainnet payment flow.

Mitigation: Do not proceed with payment unless the merchant identity, amount, currency, network, and recipient are clearly resolved and confirmed outside the placeholder configuration.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bubblevan/skills/showmethemoney-skill)
- [Execute endpoint](https://wenfu.cc/showmethemoney)
- [StablePay purchase verification endpoint](https://api.stablepay.co/verify?skill=did:solana:REPLACE_WITH_YOUR_SKILL_DID&agent={AGENT_DID})

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or plain text response with payment status guidance and backend result when purchase is verified]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a verified StablePay purchase before returning paid capability results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
