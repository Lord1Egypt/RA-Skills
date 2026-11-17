## Description:

Search, bargain, order, and pay for pet supplies on Vigilath.com - an AI-powered pet commerce platform with multi-round price negotiation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gt-oliver](https://clawhub.ai/user/gt-oliver)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to search Vigilath.com pet supplies, negotiate eligible prices, place orders, manage addresses, and complete payment with a Vigilath account token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create and pay for orders with account points without a required final confirmation.

Mitigation: Require the agent to show and confirm the exact products, quantities, total price, shipping address, and payment method before every order and before every payment.

Risk: Autonomous shopping and instant points payment can spend account value if enabled without limits.

Mitigation: Avoid autonomous shopping and points payment unless explicit spending limits and pre-approval rules are in place.

Risk: The skill depends on a Vigilath account token that authorizes shopping actions.

Mitigation: Install only for agents that are intended to use a Vigilath account token, and treat VIGILATH_TOKEN as a sensitive credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gt-oliver/skills/vigilath-shopping)
- [Vigilath service](https://www.vigilath.com)
- [Vigilath agent discovery](https://www.vigilath.com/.well-known/agent.json)
- [Vigilath LLM summary](https://www.vigilath.com/llms.txt)
- [Vigilath full API documentation](https://www.vigilath.com/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a VIGILATH_TOKEN account token; API responses include product, bargain, order, payment, and address data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
