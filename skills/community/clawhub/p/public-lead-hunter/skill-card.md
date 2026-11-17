## Description:

通过关键词、账号或作品链接检索抖音公开内容与热点，并输出供选题、竞品、舆情和获客分析使用的结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

运营、增长、销售与内容分析团队可用它查找公开视频、创作者、作品、评论和热榜，并整理选题、竞品、舆情、需求或潜在客户信号。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or IDs may be sent to the third-party service.

Mitigation: Disclose this before running a query and submit only terms and public links the user intends to share.

Risk: ClawScan flags the release for review with medium confidence, and its analysis covered only part of the artifact.

Mitigation: Review the full skill before installation, including its account-search and post-detail functions; treat the scan as a review signal, not proof of malicious intent.

## Reference(s):

- [使用说明](SKILL.md)
- [输出契约](references/contract.md)
- [参数说明](references/options.md)
- [错误处理](references/errors.md)
- [需求挖掘指南](references/demand-mining.md)
- [获客指南](references/customer-acquisition.md)
- [GuaiKei 服务与 API 入口](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown tables, Guidance]

**Output Format:** [结构化 JSON，以及简洁中文摘要或表格]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [结果数量和对象形态随命令而变；报告只提取关键字段。]

## Skill Version(s):

1.5.0 (source: frontmatter, changelog, package.json; released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
