## Description:

Reads grading standards, assignment requirements, or evaluation rubrics, analyzes gaps in a current draft, and produces a prioritized improvement plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Students, instructors, researchers, and other writers use this skill to compare a draft against a rubric or scoring standard, identify missing high-value criteria, and plan revisions in priority order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local macOS clipboard contents on request, which may expose unrelated sensitive text if the clipboard contains passwords, tokens, private messages, or confidential material.

Mitigation: Before invocation, replace the clipboard contents with only the rubric, assignment, or draft text intended for analysis.

Risk: The helper command depends on Node.js and macOS pbpaste, so it may fail or return no text in other environments.

Mitigation: Confirm Node.js and pbpaste are available before use, or provide the rubric text directly to the agent instead of using the clipboard helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/rubric-gap-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with clipboard text bounded by plain-text markers when the helper command is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and macOS pbpaste for clipboard reading.]

## Skill Version(s):

1.0.0 (source: release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
