## Description:

帮助用户批量采集公开小红书笔记的点赞、收藏、评论和分享数，并导出 CSV。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

社媒运营、投放和分析人员可批量查询公开小红书笔记的互动指标，用于结案统计、活动监测和内容分析。使用前需要账号登录和带 xsec_token 的笔记链接；成功采集会消耗点数。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 默认服务地址使用明文 HTTP，账号令牌和带 xsec_token 的笔记链接可能在传输中暴露。

Mitigation: 使用具备正常证书验证的 HTTPS 服务地址；无法切换时避免在不可信网络上使用。

Risk: 首次使用时可能自动导入另一项本地小红书工具保存的凭证，并在本地保存可复用令牌。

Mitigation: 使用前核对账号和本地凭证来源，保护配置文件，并在不再需要时登出或移除令牌。

Risk: 成功采集会消耗点数，强制重提可能再次计费。

Mitigation: 提交前核对链接和剩余点数，避免无意使用强制重提。

## Reference(s):

- [ClawHub skill listing: 小红书互动数采集](https://clawhub.ai/cuiyunhai/skills/xhs-dpt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [互动指标表格或 CSV 文件；命令行结果为 JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按笔记返回点赞、收藏、评论、分享数及任务状态；未采集到的指标为空字符串，不等于零。]

## Skill Version(s):

2.0.1 (source: release evidence, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
