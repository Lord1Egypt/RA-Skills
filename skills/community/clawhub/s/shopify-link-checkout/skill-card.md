## Description: <br>
Autonomous Shopify purchasing using Stripe Link for payment and Playwright for browser checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdliriano](https://clawhub.ai/user/sdliriano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Shopify products, prepare Stripe Link spend requests, and automate checkout for online purchases after the required account, payment, catalog, and browser setup is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says this skill is designed to make real Shopify purchases. <br>
Mitigation: Require human confirmation of merchant, item, quantity, shipping address, total price, and payment method immediately before purchase. <br>
Risk: The security review says the skill handles payment data unsafely. <br>
Mitigation: Avoid passing card numbers, CVC values, or personal data on the command line; use an isolated environment and secure credential handling. <br>
Risk: The security review says the skill includes automation-bypass behavior without enough user-controlled safeguards. <br>
Mitigation: Remove checkout automation that circumvents merchant protections and review the skill carefully before installation or execution. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/sdliriano/shopify-link-checkout) <br>
- [Shopify developer dashboard](https://dev.shopify.com/dashboard) <br>
- [Shopify Agentic Commerce](https://shopify.dev/docs/agents) <br>
- [Stripe Link for Agents](https://link.com/agents) <br>
- [Official Link CLI skill reference](https://link.com/skill.md) <br>
- [Chromium dependency reference](references/chromium-deps.md) <br>
- [Checkout automation script](scripts/shopify-checkout.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API request examples, and a Node.js Playwright checkout script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated Stripe Link CLI, Shopify Catalog API credentials, Playwright with Chromium, buyer contact and shipping details, and explicit payment approval before purchase.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
