## Description:

按合集 ID 查询微信视频号合集内的视频列表，并支持游标翻页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员和开发者可查询指定微信视频号合集中的视频，并按游标获取后续页面。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may install or upgrade Node.js and qhkit on the host.

Mitigation: Review the installation steps and preinstall qhkit yourself if preferred.

Risk: An account token may be stored on the host or supplied through an environment variable.

Mitigation: Use a least-privilege token and confirm the intended cn or intl account environment before use.

Risk: Fetching video lists incurs Qinghu credits and pagination can require multiple calls.

Mitigation: Review the estimate and approve the expected paid calls before retrieval.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary or exported table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated video records; reports credits used for paid calls.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
