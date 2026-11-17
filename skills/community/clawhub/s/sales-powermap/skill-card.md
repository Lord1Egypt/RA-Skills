## Description:

Sales Power Map is an intelligent B2B sales assistant that turns fuzzy sales intent into target-account research, decision-maker mapping, Power Map relationship diagrams, and actionable account plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinin2005](https://clawhub.ai/user/yinin2005)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B sales teams and business-development users use this skill to identify potential target accounts, research company leadership and decision paths, map relevant stakeholders, and prepare account-entry plans. It is intended for user-directed sales research rather than autonomous outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect or infer individual emails and contact channels during sales research.

Mitigation: Require explicit user approval before collecting or inferring personal contact details, and follow applicable privacy, compliance, and outreach rules.

Risk: Broad activation from vague sales prompts may start account research with limited confirmation.

Mitigation: Confirm the product, target company or customer segment, and research scope before performing web research or producing contact recommendations.

Risk: Generated reports may include inferred stakeholder roles, reporting lines, or sales recommendations that are incomplete or outdated.

Mitigation: Review generated Power Maps and account plans against current public sources before using them for business decisions.

Risk: Shell or file operations could affect files outside the intended report output path.

Mitigation: Constrain shell and file operations to generated report artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinin2005/skills/sales-powermap)
- [ClawHub publisher profile](https://clawhub.ai/user/yinin2005)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports with tables, Mermaid diagram code, contact summaries, recommended sales paths, and optional generated image or PDF artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include inferred company/person details, contact channels, and outreach recommendations when explicitly directed by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
