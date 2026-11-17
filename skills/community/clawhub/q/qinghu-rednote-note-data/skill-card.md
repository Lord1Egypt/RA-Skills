## Description:

按小红书笔记链接查询标题、正文、图片以及点赞、收藏和评论等数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员和研究人员可按小红书笔记链接获取笔记内容和互动数据，用于查看或分析单篇笔记。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can install or upgrade local software and change the environment.

Mitigation: Use an environment with qhkit and Node already provisioned; explicitly approve any installation or upgrade.

Risk: Credential setup can store an API token locally.

Mitigation: Explicitly approve credential setup and handle the token through a trusted secret-management process.

Risk: Data lookups incur credits and the final charge can vary with result size.

Mitigation: Check the current estimate and obtain user consent before paid calls; report the actual credits charged.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-rednote-note-data)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise text or Markdown summaries; file output for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the platform and relevant sample details; discloses credits charged for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
