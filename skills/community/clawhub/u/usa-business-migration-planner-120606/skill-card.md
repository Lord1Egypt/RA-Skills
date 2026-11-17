## Description:

Guides agents through a repeatable coding workflow for clarifying a request, planning implementation, producing an artifact or code change, and validating the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and technical users use this skill to turn coding-related requests into a structured plan, checklist, analysis, code change, or verification note. It should not be treated as U.S. business migration planning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is mislabeled as a USA business migration planner while its behavior is a generic coding-workflow helper.

Mitigation: Review task fit before use and rename or narrow the skill before relying on it for business migration work.

Risk: Broad implicit invocation can cause the skill to be triggered under the wrong purpose.

Mitigation: Disable or restrict implicit invocation unless the deployment intentionally wants a coding workflow helper.

Risk: Generated plans, code, commands, or configuration may be incorrect or incomplete.

Mitigation: Review proposed outputs and run the included validation or test commands before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/usa-business-migration-planner-120606)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's immediate request and should include assumptions, limits, and validation notes when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
