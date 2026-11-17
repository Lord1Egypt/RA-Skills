## Description:

通过海关进出口记录搜索贸易交易与企业，帮助外贸团队发现潜在采购商和供应商。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

外贸团队可按产品、HS 编码、国家及企业筛选海关交易和采购商、供应商，并按需查询企业详情与联系方式。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local API keys may be exposed when inspecting the credential file.

Mitigation: Provide the key through a controlled environment or secret store; do not display the credential file.

Risk: Searches, contact enrichment and recharge-order creation may incur charges.

Mitigation: Check current pricing and account balance, then require explicit confirmation before each paid operation or recharge order.

Risk: Diagnostic reports may send query context to the vendor.

Mitigation: Review the report contents and require explicit confirmation before sending diagnostics.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/upkuajing-customs-trade-company-search-zh)
- [跨境魔方官网](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [API 价格说明](https://www.upkuajing.com/web/openapi/price.html)
- [贸易列表 API 参考](references/trade-list-api.md)
- [公司列表 API 参考](references/company-list-api.md)
- [公司详情 API 参考](references/company-detail-api.md)
- [联系方式 API 参考](references/contact-fetch-api.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown summaries, JSON responses and JSONL exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trade records, company profiles and contact details.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
