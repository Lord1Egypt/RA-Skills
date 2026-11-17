## Description:

按品牌名称查询 Shopee 指定站点最多 720 天的每日产品数、销量、销售额和店铺数趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee 卖家和品牌分析人员按品牌、站点及日期范围查看每日销售趋势，并获取摘要或较大结果的表格文件。

### Deployment Geography for Use:

Shopee sites in Taiwan, Malaysia, Indonesia, Thailand, the Philippines, Singapore, Vietnam, and Brazil

## Known Risks and Mitigations:

Risk: The skill may install Node/npm software or change local configuration without enough user control.

Mitigation: Prefer user-preinstalled, version-pinned qhkit; review and approve installs and local configuration changes first.

Risk: Configuring an API token can expose a credential if handled carelessly.

Mitigation: Let the user supply the token securely, avoid displaying it, and verify the intended service before use.

Risk: Trend queries are paid and their exact cost may be unknown before a call.

Mitigation: Show any available credit estimate, disclose uncertainty, and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-daily-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend summary; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports site and date range; paid calls report credits used.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
