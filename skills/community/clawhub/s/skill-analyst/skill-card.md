## Description:

Analyze and evaluate OpenClaw skills before installing or publishing by comparing similar skills, checking feature overlap, supporting optional security review, and producing install or publish recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiabupt](https://clawhub.ai/user/lixiabupt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to evaluate whether an OpenClaw skill is worth installing or ready to publish. It compares candidates against installed and ClawHub skills, summarizes overlap and risks, and ends with a clear recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger wording could activate during generic install or publish questions.

Mitigation: Confirm that the user wants an OpenClaw skill comparison or publication review before inspecting local skill directories or querying ClawHub.

Risk: Security review may be unavailable when the optional skill-vetter dependency is not installed.

Mitigation: Report security review as skipped and recommend an external review before relying on the install or publish verdict.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lixiabupt/skills/skill-analyst)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, concise findings, and a verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClawHub CLI commands to inspect comparable skills; optional security review is reported as skipped when skill-vetter is unavailable.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
