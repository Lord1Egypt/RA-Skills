## Description:

帮助用户检索并分析信创与 IT 信息化领域的招投标、企业和市场数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

面向政府采购、IT 销售与市场分析人员，按需检索招标中标信息，并分析企业、供应商、品牌和采购趋势。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Search criteria are sent to Zhiliaobiaoxun, and paid queries may consume account credits.

Mitigation: Limit queries to the user's requested scope and check the account balance before running paid lookups.

Risk: Automatic registration can share a stable device fingerprint, and saved API keys or temporary login links can expose account access.

Mitigation: Use an existing API key when available; obtain consent before device-based registration and keep keys and login links private.

Risk: The service's privacy and data-retention claims have not been independently verified.

Mitigation: Avoid sending unnecessary sensitive details in search criteria.

## Reference(s):

- [招投标搜索 API](references/api-search.md)
- [企业分析 API](references/api-company.md)
- [市场分析 API](references/api-market.md)
- [企业登记与资质 API](references/api-registry.md)
- [账户 API](references/api-account.md)
- [自动注册说明](references/auto-register.md)
- [知了标讯技能文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [技能发布页](https://clawhub.ai/zhiliaobiaoxun/skills/xinchuang-it-procurement-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries, tables, and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected filters and available source data.]

## Skill Version(s):

1.0.10 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
