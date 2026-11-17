## Description:

Guides an agent through preparing, approving, and verifying Whop products, prices, payment links, and sales pages, with playbooks for launch, growth, and support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[major-agv](https://clawhub.ai/user/major-agv)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and business owners use this skill with an agent to plan and launch a Whop store, draft offers and sales materials, and check account changes after explicit approval. It also provides guidance for promotion, affiliates, and customer support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent actions can change a live Whop business, including products, prices, and payment links.

Mitigation: Confirm the selected business and exact change, require owner approval before each write, and read saved settings back afterward.

Risk: Account credentials or persistent CLI access may be exposed or misused.

Mitigation: Use official Whop sign-in, never share passwords or keys in chat, and protect the CLI credential store.

Risk: The optional publisher partner signup link may earn the publisher a commission.

Mitigation: Disclose the relationship, offer the link only when a new account is needed, and let the user choose whether to use it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/major-agv/skills/whop-quick-scaler-launcher)
- [Publisher-listed project homepage (not verified as release provenance)](https://github.com/MAJOR-AGV/whop-quick-scaler-launcher)
- [Whop MCP documentation](https://docs.whop.com/mcp)
- [Whop CLI documentation](https://docs.whop.com/cli/overview)
- [Offer and pricing guide](artifact/references/offer-and-pricing.md)
- [Whop field traps](artifact/references/field-traps.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with setup steps, draft copy, commands, and verification receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Previews and approval checkpoints precede account writes; saved settings are read back and reported.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
