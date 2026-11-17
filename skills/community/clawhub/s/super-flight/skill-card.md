## Description:

Compares one-way flight prices across up to seven dates using fly.ai search results, persona-based travel constraints, route history, and explainable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxchao](https://clawhub.ai/user/zhangxchao)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to compare candidate one-way flights across nearby dates, apply family, business, student, senior, or honeymoon constraints, and explain why selected options are recommended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores route, persona, preference, and booking-outcome history locally.

Mitigation: Review retained travel data before sharing the skill workspace, and clear or disable history and preferences when persistence is not desired.

Risk: The skill asks users to install an unpinned global third-party CLI.

Mitigation: Prefer a pinned or local CLI installation and treat the fly.ai API key as sensitive configuration.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/zhangxchao/skills/super-flight)
- [search-flight CLI Reference](references/search-flight.md)
- [fly.ai Open Platform](https://flyai.open.fliggy.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, inline shell commands, and booking links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should be grounded in fly.ai response data, persona filters, and local route history; prices are shown as from-prices.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
