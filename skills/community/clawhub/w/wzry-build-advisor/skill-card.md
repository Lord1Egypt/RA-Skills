## Description:

王者荣耀出装与节奏建议。当用户说在玩某个英雄、对面有难搞/克制自己的英雄、报当前装备并问怎么出装、出什么克制对面，或问野怪/BUFF/暴君主宰刷新时间与节奏时使用。基于本地装备、英雄与野区数据给出下一件装备、成装路线和资源节奏。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzfly](https://clawhub.ai/user/yzfly)

### License/Terms of Use:

MIT

## Use Case:

External 王者荣耀 players and game-advice agents use this skill to get concise Chinese-language equipment, counter-build, final build, and jungle-resource timing guidance during live play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game data such as jungle timers and item behavior can drift across 王者荣耀 seasons.

Mitigation: Check timing-sensitive advice against the current in-game season and current patch notes before relying on it in play.

Risk: The skill is optimized for Chinese-language 王者荣耀 users.

Mitigation: Use it in Chinese-language workflows or translate and review outputs before presenting them to non-Chinese users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yzfly/skills/wzry-build-advisor)
- [王者荣耀图鉴](https://code.jiangshu.ai/wzry-atlas/)
- [出装克制规则](artifact/references/counter-rules.md)
- [王者荣耀装备大全](artifact/references/equipment.md)
- [王者荣耀英雄速查](artifact/references/heroes.md)
- [王者荣耀峡谷野区速查](artifact/references/jungle.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Concise Chinese Markdown with labeled recommendation lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include next-item advice, two to three follow-up items, a final six-item build, and up to two jungle or counter-play reminders; no files or shell commands are produced.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
