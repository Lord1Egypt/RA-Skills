## Description:

按 B 站 UP 主主页链接查询投稿视频及播放、点赞、投币、收藏、转发和评论数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、运营人员和分析师可查询 B 站 UP 主投稿视频及互动数据，以了解近期作品表现。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update qhkit and Node on the local machine.

Mitigation: Review or perform setup yourself and pin package versions where possible.

Risk: Using the skill requires a Qinghu API token in local configuration or the environment.

Mitigation: Configure the token yourself and keep it private.

Risk: Video lookups are paid, and larger results may cost more credits.

Mitigation: Check the current estimate and obtain approval before retrieval, especially for bulk requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-bilibili-creator-videos)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary with optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports data scope and credits consumed when a paid lookup is made.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
