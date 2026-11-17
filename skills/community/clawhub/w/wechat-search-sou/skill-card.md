## Description:

按关键词只读检索微信公开文章和视频，并返回结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

面向内容研究者和运营人员，用于按关键词查找微信文章或视频，辅助选题、热点监测和竞品分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全扫描为中等置信度 benign；部分组件仅完成部分检查，且扫描报告检测到未声明工具范围的环境访问。

Mitigation: 安装前检查技能文件，并将运行权限限制为完成搜索所需的范围；按技能说明通过环境变量提供令牌，不要将令牌放入命令参数。

Risk: 搜索关键词会发送至第三方 Guaikei API。

Mitigation: 避免提交包含机密或敏感信息的搜索关键词。

## Reference(s):

- [微信搜索参数说明](references/options.md)
- [Guaikei API 服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [结构化 JSON 搜索结果及简洁的自然语言摘要]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [用户需提供关键词并选择文章或视频搜索；可选排序、时间或时长筛选。只返回公开搜索数据，不提供图片搜索、正文抓取或账号登录。]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
