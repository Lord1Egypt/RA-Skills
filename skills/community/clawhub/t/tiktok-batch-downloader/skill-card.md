## Description:

为 AI 助手提供 TikTok 公开内容的关键词搜索、创作者作品和视频评论查询，并返回结构化 JSON；不提供视频文件下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

创作者、营销与研究人员以及开发者可让 AI 助手查询 TikTok 公开搜索结果、创作者作品或视频评论，并将结构化数据用于选题调研、竞品观察和评论分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 技能名称与发布摘要提到批量下载，但文档说明命令查询公开视频数据、作品和评论，不下载视频文件。

Mitigation: 使用前确认只需要公开数据查询；不要依赖它生成本地视频文件。

Risk: 查询会将关键词或 TikTok 链接发送到 Guaikei 服务，并需要 API 访问令牌。

Mitigation: 仅提交适合发送给该服务的公开查询内容，并妥善保管 GUAIKEI_API_TOKEN。

Risk: 安全评估置信度为中等，部分组件仅经过部分分析。

Mitigation: 在依赖结果前核对返回内容，并在部署时审阅技能及其查询范围。

## Reference(s):

- [参数与结果说明](artifact/references/options.md)
- [更新日志](artifact/references/changelog.md)
- [技能发布页](https://clawhub.ai/why20261/skills/tiktok-batch-downloader)
- [Guaikei 服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [包含结构化结果数组的 JSON 信封]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按搜索、作品或评论命令返回公开数据；不生成视频文件。]

## Skill Version(s):

1.1.2 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
