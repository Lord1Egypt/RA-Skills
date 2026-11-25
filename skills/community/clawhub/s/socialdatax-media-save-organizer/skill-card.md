## Description:

用户提供社媒内容链接或媒体直链和输出目录时，保存支持平台的图片、视频或音频，并整理来源链接、本地文件路径及成功失败清单。支持小红书、抖音、快手、微博、X / Twitter 和 Bilibili，使用 社媒数据助手 SocialDataX 现有命令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要整理社媒素材的用户：根据用户提供的支持平台内容链接或媒体直链，将图片、视频或音频保存到指定目录，并汇总来源、文件路径及失败情况。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated execution of an unpinned `@latest` package could expose available credentials or local files if the package changes or is compromised.

Mitigation: Review the package version before execution and limit the execution environment to the credentials and files needed for the requested task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-media-save-organizer)
- [SocialDataX](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown]

**Output Format:** [Saved media files with a text or Markdown results summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes only user-provided links for supported platforms; reports source links, local paths, and failures when available.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
