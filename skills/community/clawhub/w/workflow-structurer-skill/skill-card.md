## Description:

Interactive workflow structuring assistant that guides users step-by-step to transform vague process descriptions into structured, executable workflow documents with inputs, outputs, responsibilities, risks, validation criteria, and rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csh995426531](https://clawhub.ai/user/csh995426531)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn an unclear process description into a structured workflow document. It progressively clarifies the goal, step skeleton, inputs, outputs, responsibilities, risks, validation criteria, rules, and final handoff summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for operational process details, which may include sensitive business or personal information.

Mitigation: Share only details needed to document the workflow, and omit or generalize sensitive information where possible.

Risk: Broad process-related prompts may activate the skill even when a user only wants a quick answer.

Mitigation: Confirm the user's workflow-structuring goal before collecting step details or producing structured documentation.

## Reference(s):

- [Step Definition Template](references/step-template.md)
- [ClawHub Skill Page](https://clawhub.ai/csh995426531/skills/workflow-structurer-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown workflow documentation and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive question-and-answer flow; matches the user's language and asks for confirmation before advancing between workflow steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
