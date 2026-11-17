## Description:

Autonomous Shopify purchasing using Stripe Link for payment and Playwright for browser checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdliriano](https://clawhub.ai/user/sdliriano)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to search for Shopify products, request user approval for a Stripe Link spend request, and run a browser-based checkout workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill can perform real autonomous purchases and exposes payment and personal data during checkout.

Mitigation: Use a human approval step immediately before payment that verifies the merchant, item, total, shipping address, and payment method.

Risk: Checkout automation can send live card or personal data to an unverified destination.

Mitigation: Independently verify the checkout destination before providing payment or personal data.

Risk: Browser automation dependencies and sandbox changes can increase operational risk.

Mitigation: Install pinned dependencies safely and restore browser sandboxing or run the checkout flow in an isolated environment.

## Reference(s):

- [Shopify Link Checkout Skill](https://clawhub.ai/sdliriano/skills/shopify-link-checkout)
- [Installing Chromium Dependencies Without Root](references/chromium-deps.md)
- [Stripe Link for Agents](https://link.com/agents)
- [Shopify Agentic Commerce](https://shopify.dev/docs/agents)
- [Link Skill Reference](https://link.com/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript automation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces purchase workflow guidance and command invocations that can initiate real checkout automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
