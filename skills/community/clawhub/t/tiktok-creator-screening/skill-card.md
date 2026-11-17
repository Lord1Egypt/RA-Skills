## Description:

通过关键词搜索、达人公开作品和视频评论，帮助智能体研究 TikTok 创作者并整理有数据依据的合作候选名单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

面向 TikTok 创作者、MCN、品牌和市场研究团队，帮助智能体检索公开视频、创作者作品和评论，再据可用数据筛选合作对象、分析竞品内容或整理舆情。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 搜索词和 TikTok 目标会发送给 GUAIKEI，API 使用可能产生费用；服务方的隐私和计费说明未经独立核实。

Mitigation: 仅在接受数据共享和潜在费用时使用，先查看服务方当前条款，并控制结果数量。

Risk: API Token 属于凭证，启用本地日志后可能保留返回的数据。

Mitigation: 妥善保管 Token，仅在需要留存本地副本时启用日志。

Risk: 公开的达人和评论数据可能包含用户标识；对外分享或商业使用前可能需要授权。

Mitigation: 未经授权时仅供个人或团队内部分析；对外分享前确认权限并隐藏用户标识。

## Reference(s):

- [GUAIKEI service and API access](https://www.guaikei.com)
- [ClawHub skill listing](https://clawhub.ai/why20261/skills/tiktok-creator-screening)
- [Usage options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [包含视频搜索、达人公开作品或视频评论结果的结构化 JSON 信封]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [智能体根据返回的公开数据进行达人筛选和分析；结果取决于可用字段，不提供单独的粉丝总数对象或视频下载。]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
