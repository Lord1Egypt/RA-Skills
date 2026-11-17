## Description:

帮助学生记录学习时间、使用番茄钟保持专注，并识别个人的高效时段和分心规律。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

学生使用此技能记录学习时长、安排并复盘专注时段，以及在积累足够数据后查看自己的高效时段和分心规律。长期保存、提醒和跨技能共享均需分别明确同意。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent profiles and cross-skill sharing involve student data, and the security evidence flags consent as a concern.

Mitigation: Keep profile storage, reminders, and cross-skill sharing disabled until each has separate affirmative consent; follow the documented guardian-consent requirement for younger students and confirm each proposed profile write.

Risk: Security analysis is partial because three local path-like references could not be resolved.

Mitigation: Check that the referenced materials are present and review them before relying on behavior that depends on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-time-focus-coach)
- [Publisher profile: qizhitang](https://clawhub.ai/user/qizhitang)
- [Pomodoro state machine](references/pomodoro-statemachine.md)
- [Focus archive template](references/focus-archives-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown summaries, time plans, and focus recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent profile entries, reminders, and cross-skill sharing are optional and require separate consent.]

## Skill Version(s):

2.12.7 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
