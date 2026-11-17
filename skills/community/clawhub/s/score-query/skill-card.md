## Description:

用于查询学生各科目成绩的 OpenClaw 技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bc96](https://clawhub.ai/user/bc96)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, or support agents use this skill to look up a named student's score in one subject or all recorded subjects from a local score database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose student grade data without clear authentication, per-user authorization, or log redaction.

Mitigation: Use only placeholder data until authentication, per-user authorization, and log redaction are added and reviewed for the target environment.

Risk: The release declares an ffmpeg binary requirement that is unrelated to score lookup behavior.

Mitigation: Remove the ffmpeg requirement or document why it is needed before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bc96/skills/score-query)
- [Publisher profile](https://clawhub.ai/user/bc96)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Chinese text response with optional structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, message text, and score data when a matching student and subject are found.]

## Skill Version(s):

0.0.2 (source: release evidence, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
