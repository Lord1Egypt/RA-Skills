## Description:

基于腾讯会议(tmeet)培训会议的录制转写，把冗长转写稿整理为带章节结构、要点提炼与自测题的培训手册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golgys0621](https://clawhub.ai/user/golgys0621)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, training leads, and onboarding teams use this skill to convert Tencent Meeting or user-provided training transcripts into reusable Markdown handbooks with chapters, key points, and self-check questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training transcripts may contain confidential or personal information.

Mitigation: Use only authorized transcripts and ensure tmeet or local file access complies with internal data policies.

Risk: Generated handbooks and self-check questions may be incomplete or unsuitable for formal assessment.

Mitigation: Review and edit handbooks and quiz questions before formal training or evaluation.

Risk: The workflow and source materials are Chinese-language oriented.

Mitigation: Install and use the skill only when the agent operator is comfortable reviewing Chinese-language training content.

## Reference(s):

- [培训手册模板](references/training_template.md)
- [ClawHub skill release](https://clawhub.ai/golgys0621/skills/training-notes-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown training handbook with a table of contents, chapter key points, and self-check questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated handbooks and quiz questions should be reviewed before formal training or assessment use.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
