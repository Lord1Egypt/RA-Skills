## Description:

Consult the tool-models agent for model selection, cost estimation, capability queries, and provider comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to query current model availability, capabilities, provider limits, and costs before selecting models or changing model configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model recommendations may become outdated or reflect only currently accessible provider data.

Mitigation: Query the tool-models helper at decision time and review recommendations before applying production or cost-sensitive changes.

Risk: Provider limits and pricing can affect cost estimates and deployment fit.

Mitigation: Compare provider-specific limits and costs before committing to high-volume or recurring workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanford/skills/skilled-models-advisor)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with command examples and structured model comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on current model database access and provider data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
