## Description:

查询江苏招标与中标公告、企业工商与投标记录，并支持商机、竞争对手和市场分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

采购与投标团队可用它检索招标和中标项目、分析企业及市场，并按需查询江苏数据；江苏是默认地区，用户也可指定其他地区。

### Deployment Geography for Use:

China (Jiangsu is the default search region)

## Known Risks and Mitigations:

Risk: Automatic trial registration sends a persistent hardware-derived identifier, and the packaged registration guidance has conflicting instructions.

Mitigation: Prefer a manually configured API key. Use automatic registration only after explaining the identifier collection and receiving consent; stop on authentication errors rather than switching accounts or registering again.

Risk: Search terms are sent to the service and searches may consume account credits; saved keys and login links are sensitive.

Mitigation: Limit searches to the user's request, check account balance when useful, and keep API keys and login links private.

## Reference(s):

- [标讯技能页面](https://clawhub.ai/bailianai/skills/tender-jiangsu)
- [知了标讯产品主页](https://ai.zhiliaobiaoxun.com/?ch=s151)
- [技能使用文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [api-search.md](artifact/references/api-search.md)
- [api-company.md](artifact/references/api-company.md)
- [api-registry.md](artifact/references/api-registry.md)
- [api-market.md](artifact/references/api-market.md)
- [api-account.md](artifact/references/api-account.md)
- [auto-register.md](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Chinese-language Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and analysis reflect the requested filters; no files are produced.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
