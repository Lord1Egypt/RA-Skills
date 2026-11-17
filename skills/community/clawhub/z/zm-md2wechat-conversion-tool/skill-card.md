## Description:

ZM Markdown 转公众号格式工具。用于将 Markdown 转为微信公众号 HTML，检查主题、图片、样式、AI 痕迹处理和草稿创建能力；正式发布需配合 ZM 公众号草稿发布与核验 Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and publishing operators use this skill to route Markdown content through a WeChat Official Account conversion workflow, inspect metadata and readiness, create local previews, and prepare draft or image-post actions when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a mutable external CLI that may receive WeChat credentials and perform account-changing uploads.

Mitigation: Install only from a trusted maintainer path, prefer a pinned and reviewed CLI version, and provide WeChat credentials only for upload or draft actions.

Risk: Credential-bearing commands could process Markdown or images the user did not intend to submit to WeChat.

Mitigation: Validate configuration before draft or image-post actions and avoid running credential-bearing commands on untrusted or unintended content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-md2wechat-conversion-tool)
- [Publisher profile](https://clawhub.ai/user/jerryxn)
- [Skill homepage](https://github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill)
- [Go install module from ClawHub metadata](https://github.com/geekjourneyx/zm-md2wechat-conversion-tool-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in local HTML previews, draft JSON inputs, uploaded media actions, image post actions, or generated image assets when the user explicitly requests those workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
