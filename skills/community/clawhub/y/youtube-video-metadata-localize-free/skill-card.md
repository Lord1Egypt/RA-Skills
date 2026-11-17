## Description:

使用用户指定的 Easy WebBridge 浏览器环境读取一个已授权的公开视频页面，为中文受众整理原题和简介要点，产出中文标题、简介草稿、逐条来源链接与缺项说明。适用于上线前本地化审阅；简介不可见或原主张含糊时保留原词，不改写后台内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向需要为中文受众审阅公开视频元数据的创作者和内容团队。根据一个已授权、公开可见的 YouTube 视频整理中文标题与简介草稿，并为事实附上来源、标记无法确认的内容。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions differ on who selects a browser profile and when a new environment may be created.

Mitigation: Use one explicitly selected browserId throughout the task; confirm authorization and obtain separate approval before creating an environment or installing software.

## Reference(s):

- [EasyBR AI 操作总指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)
- [Easy WebBridge](https://github.com/aiispower/easy-webbridge)
- [Easy WebBridge Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR 下载页](https://www.ebrower.com/down.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Source links, Guidance]

**Output Format:** [JSON or Markdown with original title and visible description points, Chinese draft, source URLs, and missing_items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one video per run; keeps uncertain claims marked for review and does not change backend content.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
