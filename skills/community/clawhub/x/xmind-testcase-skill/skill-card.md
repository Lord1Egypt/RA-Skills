## Description:

Generates structured XMind test-case mind maps from functional requirement descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manman1104](https://clawhub.ai/user/manman1104)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to turn functional requirements into structured test cases and XMind mind maps for features such as login, registration, checkout, and search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a local testcase.xmind file and may overwrite an existing file with that name.

Mitigation: Run it in a workspace where replacing testcase.xmind is acceptable, or move any existing file before execution.

Risk: Published entry-point metadata appears inconsistent and may prevent reliable execution without packaging correction.

Mitigation: Confirm the configured entry point matches the packaged generator before using the skill in an automated workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manman1104/skills/xmind-testcase-skill)
- [Publisher profile](https://clawhub.ai/user/manman1104)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [XMind file with structured test-case topics and JSON test-case content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes testcase.xmind in the working directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
