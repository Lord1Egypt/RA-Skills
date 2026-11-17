## Description:

Provides information about planned Shopify management through Agiexa and supports an opt-in waitlist signup; Shopify management tools are not available in this release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devkrutik](https://clawhub.ai/user/devkrutik)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants and store teams use it to learn about Agiexa's planned Shopify management features and, if they choose, join its waitlist. This release does not provide live Shopify management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Shopify management capabilities and the service's security protections are not implemented or independently verified in this release.

Mitigation: Describe this release as a preview and do not represent it as able to perform Shopify actions.

Risk: Waitlist signup sends the user's email, role, and any optional URL or message to Agiexa.

Mitigation: Submit only after explicit permission and confirm the user-provided signup details before sending.

## Reference(s):

- [Agiexa Shopify integration](https://agiexa.com/integrations/shopify)
- [Agiexa integrations](https://agiexa.com/integrations)
- [Shopify tools preview](references/tools.md)
- [Shopify triggers preview](references/triggers.md)
- [Shopify use cases](references/use-cases.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Conversational text; JSON waitlist submission only after explicit opt-in]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Waitlist signup uses user-confirmed details and requires explicit permission.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
