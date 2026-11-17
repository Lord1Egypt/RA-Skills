## Description:

Continuous self-improvement through learning from user corrections and task self-evaluation, with learnings stored in persistent memory for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonylnng](https://clawhub.ai/user/tonylnng)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to help an OpenClaw agent record user corrections, self-evaluation lessons, and recent learned patterns. It is intended for environments where persistent correction and lesson memory is expected and reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically store broad task and user-correction history in persistent memory without clear consent or deletion controls.

Mitigation: Use it only where persistent memory is expected, and provide users a clear way to review, edit, and delete stored entries.

Risk: Correction and lesson logs may capture sensitive or personal information if users or agents include it in memory entries.

Mitigation: Review entries before retention where possible, follow the skill's no-secrets rule, and keep each stored lesson narrow and concise.

## Reference(s):

- [Corrections Template](references/corrections-template.md)
- [ClawHub Skill Page](https://clawhub.ai/tonylnng/skills/tonic-self-learn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown log entries and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write correction and lesson entries to persistent memory when memory tools and files are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
