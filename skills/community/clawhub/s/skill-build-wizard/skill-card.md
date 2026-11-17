## Description:

End-to-end guided workflow for building production-quality agent skills through pre-flight checks, specification confirmation, coding acceptance, and release preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to guide agent-assisted skill creation from initial workspace checks through design confirmation, implementation review, testing, and release preparation. It is intended for multi-step skill-building work where staged checkpoints and explicit user approvals reduce missed requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pre-check script auto-discovers installed skill paths, which can select an unintended copy when multiple installations are present.

Mitigation: Run scripts from the known installed skill directory or verify the discovered path before execution.

Risk: The workflow coordinates release and publish steps, so skipped confirmation gates could lead to premature publication.

Mitigation: Require the user to review the change summary, acceptance report, preview URL, version, and changelog before replying with the explicit publish confirmation.

Risk: The workflow delegates scaffolding, review, regression testing, audit, and publishing to companion skills.

Mitigation: Verify companion skills are installed from trusted sources before using them in the release flow.

## Reference(s):

- [Pre-flight checks](references/checklist-before-start.md)
- [Coding acceptance](references/checklist-coding.md)
- [Release prep](references/checklist-release.md)
- [skill-creator](https://github.com/anthropics/skills)
- [skill-regression](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-regression)
- [glic-check](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check)
- [skill-release-audit](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-audit)
- [skill-release-plus](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and checklist-driven status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes staged confirmation gates, acceptance criteria, and on-demand checklist references.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
