## Description:

根据用户提供的社交媒体内容链接或媒体直链，将支持平台的图片、视频或音频保存到指定目录，并整理来源、路径及成功或失败结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要保存和整理社交媒体素材的用户；根据用户明确提供的链接下载支持平台的图片、视频或音频，并交付来源与本地文件路径清单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an automatically installed, changeable CLI package, which creates supply-chain risk when credentials are available to the execution environment; the security scan was partial.

Mitigation: Review and pin a known CLI release before execution, limit credentials to those needed for the task, and account for the scan's incomplete coverage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-media-save-organizer)
- [SocialDataX API key information](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown]

**Output Format:** [Saved media files with a concise text or Markdown results list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The results list records the provided source link, local path, media type, outcome, and failure reason when available.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
