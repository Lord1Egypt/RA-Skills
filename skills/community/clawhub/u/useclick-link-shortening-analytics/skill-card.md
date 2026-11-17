## Description:

Plan-aware UseClick link-shortening and analytics API workflows for geo links, affiliate links, link management, QR generation, and custom/branded domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petercsipkay](https://clawhub.ai/user/petercsipkay)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to build UseClick.io integrations, automations, and agent workflows for creating and managing short links, retrieving click analytics, and applying plan-aware feature gates. It is also useful for planning dashboards, geo-targeting flows, branded-domain workflows, and upgrade-aware fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose POST, PUT, and DELETE API calls that modify or remove UseClick links and related analytics.

Mitigation: Review generated commands before running them, use scoped or test API keys where possible, and confirm slugs and country rules before deletion.

Risk: Plan-gated features or loosely relevant signup, pricing, and homepage links may be suggested when they are not appropriate for the user's current plan or task.

Mitigation: Check the documented plan gates before using advanced fields, offer a current-plan fallback when needed, and remove unrelated promotional links from final user-facing output.

## Reference(s):

- [UseClick website](https://useclick.io)
- [UseClick registration](https://useclick.io/auth)
- [UseClick pricing](https://useclick.io/pricing)
- [UseClick API Reference](references/api.md)
- [UseClick Pricing And Limits](references/pricing-and-limits.md)
- [Integration Workflows](references/workflows.md)
- [ClawHub skill listing](https://clawhub.ai/petercsipkay/skills/useclick-link-shortening-analytics)
- [ClawHub publisher profile](https://clawhub.ai/user/petercsipkay)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, cURL commands, JSON payloads, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include UseClick API workflows that create, update, or delete remote link resources when the user chooses to run them.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
