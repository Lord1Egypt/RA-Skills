## Description:

Analyzes OpenClaw skills before installation or publication by comparing similar ClawHub and installed skills, reviewing overlap and security signals, and producing a clear recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiabupt](https://clawhub.ai/user/lixiabupt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to decide whether a skill is worth installing or ready to publish. It produces structured comparisons, risk notes, improvement suggestions, and explicit install or publish recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local OpenClaw skill descriptions and run ClawHub lookup commands during install or publish evaluations.

Mitigation: Invoke it with an explicit target skill and review the proposed lookup or scan steps before acting on an install or publish recommendation.

Risk: Analysis results can be incomplete if the ClawHub CLI is unavailable or if optional security review tooling is not installed.

Mitigation: Confirm that `clawhub` is available and treat skipped security review sections as unresolved before installation or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiabupt/skills/skill-analyst-zh)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language reports with concise, actionable conclusions.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
