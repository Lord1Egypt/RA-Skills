## Description:

Validates AI-generated test cases against requirements for factual accuracy, consistency, executability, and traceability before final delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA practitioners and developers use this skill to check generated test cases against source requirements before delivery, flagging unsupported claims, contradictions, unworkable steps, and missing traceability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrectly flagged cases could lead to deletion of valid tests or requirements.

Mitigation: Confirm findings against source requirements and back up originals before deleting or changing cases.

Risk: The companion installation command may execute publisher-supplied code.

Mitigation: Review the package or pinned source and trust the publisher before running the command.

## Reference(s):

- [Validation dimensions](references/validation-dimensions.md)
- [ClawHub skill listing](https://clawhub.ai/kokxi/skills/qa-output-validation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown validation report with pass/fail results, findings, and source traceability]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings refer to existing test case IDs; coverage statements identify their source scope and gaps.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
