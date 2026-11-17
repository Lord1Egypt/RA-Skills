## Description:

Amazon SP-API skill for OpenClaw agents. Fetch orders, check FBA inventory, manage listings and pricing. Works with any marketplace and seller account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

External developers and commerce automation teams use this skill to connect agents to Amazon SP-API workflows for checking authentication, fetching orders, reviewing FBA inventory, and managing listing prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses reusable Amazon seller credentials.

Mitigation: Store the credential file outside source control with owner-only permissions, use a dedicated workspace, and grant the Amazon app only the roles needed.

Risk: Order, inventory, and listing outputs may contain sensitive commerce data.

Mitigation: Treat terminal output and exported JSON files as sensitive and limit sharing, retention, and workspace access.

Risk: Listing price updates can change live marketplace offers.

Mitigation: Run price update commands only after confirming the intended SKU, marketplace, currency, and price.

Risk: Runtime behavior depends on the amazon-sp-api package.

Mitigation: Pin and lock the dependency before installing or deploying the skill.

## Reference(s):

- [Amazon SP-API Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids)
- [Seller Central Develop Apps](https://sellercentral.amazon.com/apps/develop)
- [ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skills/skill-amazon-spapi)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; scripts emit terminal text and optional JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an Amazon SP-API credential file supplied outside the skill.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
