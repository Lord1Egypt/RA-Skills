## Description:

Routes Volcengine product requests through pricing, purchase or provisioning, and unsubscribe workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent can request Volcengine product pricing, place a confirmed purchase, or review and confirm an eligible unsubscribe. The skill provides action-specific guidance and transaction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Purchases and potentially destructive cancellations can create charges or affect cloud resources.

Mitigation: Use narrowly scoped billing permissions, review the full command and impact summary, and require explicit user approval before execution.

Risk: Unsubscribing can permanently erase data, and the workflow cannot enumerate associated resources.

Mitigation: Proceed with associated-resource cancellation only when the user understands the affected group and explicitly confirms the choice.

Risk: Pricing estimates can be misleading if quantities or units are misunderstood.

Mitigation: Verify quantities and units with the user, use returned pricing values, and label quotes as estimates subject to actual usage billing.

Risk: Optional dependent skills may require installation.

Mitigation: Review optional dependencies and obtain user authorization before installation.

## Reference(s):

- [Volcengine Sale on ClawHub](https://clawhub.ai/volc-sdk-team/skills/volcengine-sale)
- [Volcengine Pricing](https://www.volcengine.com/pricing)
- [OpenAPI Unsubscribe Supported Products](https://www.volcengine.com/docs/6269/1166376)
- [Volcengine Unsubscribe Rules](https://www.volcengine.com/docs/6269/81013)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, JSON]

**Output Format:** [Customer-facing text and Markdown, with shell commands or structured JSON transaction details when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific pricing, order or instance details, unsubscribe outcomes, and safety guidance]

## Skill Version(s):

1.1.0 (source: frontmatter; server release 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
