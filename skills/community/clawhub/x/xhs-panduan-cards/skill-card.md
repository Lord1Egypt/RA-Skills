## Description:

将公务员行测判断推理真题整理为五题练习，生成十张题目与解析卡片及小红书发布文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-shuanglin](https://clawhub.ai/user/wang-shuanglin)

### License/Terms of Use:

MIT-0

## Use Case:

面向公务员考试备考者，将已核验的判断推理真题编排为每日五题练习，并制作适合小红书发布的题目卡、解析卡和配套文案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect question sources or answers could mislead learners.

Mitigation: Verify each question against its original paper or an official answer and review the reasoning before publishing.

Risk: Reruns replace matching generated images in the output location.

Mitigation: Use a dedicated project folder and check the output location before rendering again.

Risk: Missing Pillow support or Chinese fonts can prevent rendering or reduce readability.

Mitigation: Provide Python with Pillow and Chinese fonts, then inspect the generated preview before publishing.

## Reference(s):

- [ClawHub release](https://clawhub.ai/wang-shuanglin/skills/xhs-panduan-cards)
- [Publisher profile](https://clawhub.ai/user/wang-shuanglin)

## Skill Output:

**Output Type(s):** [Images, Markdown, Text, Code]

**Output Format:** [PNG study cards, JSON question sets, and Markdown publishing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each set contains five questions, ten 1080×1440 portrait cards alternating questions and explanations, plus post copy and an answer summary.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata, artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
