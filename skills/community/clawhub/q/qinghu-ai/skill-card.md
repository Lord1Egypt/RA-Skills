## Description:

为电商工作流调用青虎 AI 的图像与视频创作、媒体编辑和电商数据查询能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营与内容创作者可用它生成和编辑商品图、广告视频及分镜，也可查询商品、达人、关键词和市场数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Software installation or upgrades can change the environment.

Mitigation: Require approval for installs, upgrades, elevated access, and shell profile edits; use a reviewed package version in an isolated environment.

Risk: Some estimates may upload media before paid generation is confirmed.

Mitigation: Get approval for media uploads before requesting estimates and minimize discovery queries.

Risk: Sharing an API key in chat can expose credentials.

Mitigation: Configure the API key locally rather than sharing it in chat.

Risk: Package code and publisher ownership could not be independently verified.

Mitigation: Review the package and publisher before installation; prefer a reviewed version in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-ai)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Files, Text, JSON data]

**Output Format:** [Images, videos, scripts, text, and structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media assets and task results; some services may use credits.]

## Skill Version(s):

0.1.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
