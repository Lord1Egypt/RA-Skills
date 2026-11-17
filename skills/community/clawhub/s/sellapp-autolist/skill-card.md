## Description:

Auto-creates public digital product listings on SellApp from a predefined catalog using the SellApp v2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Storefront operators and developers can use this skill to list a predefined digital product catalog on SellApp, check existing listings, and create missing public products through the SellApp API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically create public SellApp product listings on a real storefront.

Mitigation: Run it only against an intended account, inspect and edit the catalog first, and add confirmation or dry-run behavior before production use.

Risk: The automation uses a SellApp API key and can act with the permissions granted to that key.

Mitigation: Prefer a limited-scope or test API key, store it as a secret, and rotate it if exposure is suspected.

Risk: The predefined catalog may publish products, prices, file URLs, or claims that do not match the operator's actual offerings.

Mitigation: Review all product names, descriptions, prices, visibility settings, and fulfillment links before enabling the listing workflow.

## Reference(s):

- [SellApp API documentation](https://sell.app/docs/api)
- [ClawHub skill listing](https://clawhub.ai/ssidharhubble/skills/sellapp-autolist)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, the requests library, and a SELLAPP_API_KEY environment secret.]

## Skill Version(s):

1.0.14 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
