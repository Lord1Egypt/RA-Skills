## Description:

查询微信视频号作品详情，支持作品 ID、搜索结果 ID 或分享短链。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents can retrieve details for a WeChat Video Channels post from its object ID, export ID or share link, then summarize the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade qhkit and Node tooling on the local machine.

Mitigation: Review the installation steps and preinstall a vetted qhkit version before use.

Risk: Qinghu API credentials are configured locally for paid lookups.

Mitigation: Review local credential storage and provide only the required API token.

Risk: Lookup calls can consume Qinghu credits.

Mitigation: Confirm the estimated charge and authorize the call before submitting it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-video-data)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Text or Markdown summary; JSON results or an exported file for large responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include retrieved post details and credits charged.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
