## Description:

Generates structured Chinese weekly reports from work updates, highlighting completed work, measurable results, risks, and next week's plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epsilon-rhk](https://clawhub.ai/user/epsilon-rhk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers use this skill to turn scattered work notes into concise Chinese weekly reports that can be sent to stakeholders. It emphasizes outcomes, quantified results, risks, support needs, and next-week plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous progress-summary requests may be formatted as formal Chinese weekly reports.

Mitigation: Override the style explicitly or avoid invoking the skill for requests that need brief summaries or English output.

Risk: Incomplete source information can leave placeholders in the generated report.

Mitigation: Review the report before sending and replace any "待补充" placeholders with confirmed details.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown weekly report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders such as "待补充" when required information is missing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
