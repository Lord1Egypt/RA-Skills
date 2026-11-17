## Description:

Skill Risk Auditor audits third-party skills before installation across nine risk areas and explains severity in plain language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxf203](https://clawhub.ai/user/yxf203)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill before installing externally sourced skills to review package contents, identify risk areas, and receive a plain-language risk assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to read every file in a candidate skill package, which may expose sensitive content if pointed at the wrong directory.

Mitigation: Run it only against skill packages you intend to review and keep the review scope limited to the candidate package directory.

Risk: The skill produces advisory risk reports that may include incorrect or overly broad findings when a candidate package is ambiguous.

Mitigation: Use the report as review guidance and have a human verify significant findings before installing the target skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxf203/skills/skill-risk-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown risk assessment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rates nine risk areas with severity indicators and plain-language explanations.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
