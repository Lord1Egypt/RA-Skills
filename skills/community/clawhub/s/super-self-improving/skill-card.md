## Description:

Super Self Improving helps agents track multimodal memory, feedback loops, meta-learning, confidence calibration, token usage, and scheduling optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to document patterns for memory, feedback collection, error analysis, confidence calibration, token monitoring, and agent scheduling optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory and feedback records may retain preferences, errors, metrics, or inferred behavior across sessions.

Mitigation: Avoid providing secrets or sensitive personal/business data, and periodically inspect or delete ~/.super-self-improving/.

Risk: Inferred feedback, memory export, or agent scheduling behavior could affect future agent decisions if implemented without oversight.

Mitigation: Require user confirmation before applying inferred feedback, exporting memory, or taking scheduling actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombfuock/skills/super-self-improving)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with example shell commands and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable source file is bundled in the artifact.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
