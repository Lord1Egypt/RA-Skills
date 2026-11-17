## Description:

Helps QA teams estimate testing effort and schedules using complexity, historical baselines, and risk adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and project managers use this skill to estimate testing person-hours, staffing, and schedules from requirements, test strategy, and available historical data. It breaks effort into activities and reports assumptions, confidence, and risk buffers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested npx installation command runs a separate package outside this read-only skill.

Mitigation: Verify the package and source before running the installation command.

Risk: Release plans or staffing inputs may contain confidential information.

Mitigation: Avoid sharing sensitive inputs unless the agent environment and its tool permissions are appropriate.

Risk: Effort estimates may not account for missing requirements or changed project conditions.

Mitigation: Check scope, historical baselines, assumptions, and risk buffers with the project manager before changing a schedule.

## Reference(s):

- [Test effort estimation methods](references/estimation-methods.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown estimation report with effort tables and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an EST-XXXX identifier, activity breakdown, confidence assessment, and risk buffer.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
