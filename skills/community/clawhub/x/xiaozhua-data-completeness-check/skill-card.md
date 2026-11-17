## Description:

Checks whether delayed Power BI-style data has finished backfilling by comparing a late-night baseline against morning values for key metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirowangl-ops](https://clawhub.ai/user/mirowangl-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Business operations and reporting teams use this skill to decide whether delayed T+1 data appears complete before sending recurring reports. It guides agents to compare a sentinel metric at two time points and apply local threshold checks before escalating uncertain results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business-specific threshold examples may not indicate completeness for other datasets, products, weekends, holidays, or reporting periods.

Mitigation: Replace the example benchmark values with locally validated ranges for the target sentinel metrics before relying on the guidance.

Risk: The skill includes a named confirmation contact and Chinese-language operating guidance that may not match the installer's reporting workflow.

Mitigation: Localize the instructions and update the escalation contact before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirowangl-ops/skills/xiaozhua-data-completeness-check)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown checklist and decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Business-specific benchmark values and escalation contacts should be adjusted before operational use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
