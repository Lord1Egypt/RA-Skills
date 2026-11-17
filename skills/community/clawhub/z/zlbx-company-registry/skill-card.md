## Description:

查询企业工商登记，并按需查询股东、分支、投资、变更、年报、建筑资质、证书和信用评级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要核验中国企业信息的用户，按指定范围查询工商登记、股东、分支机构、对外投资、变更及相关年报、资质和评级信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful data queries may incur provider charges.

Mitigation: Query only the requested information and explain the stated point cost before optional paid lookups or additional pages.

Risk: The API key and signed login links could expose account access if shared.

Mitigation: Keep the saved API key and signed links private; use configured credentials to avoid automatic-registration data collection.

Risk: Automatic registration sends a persistent device hash, and provider backend and data-retention claims are not verified by this review.

Mitigation: Obtain user consent before automatic registration and treat returned company information as provider-supplied data.

## Reference(s):

- [Company Registry API Quick Reference](references/api-quick.md)
- [Automatic Registration and API Key Guide](references/auto-register.md)
- [Company Registry Documentation](https://ai.zhiliaobiaoxun.com/docs/skill/company-registry)
- [ClawHub Skill Page](https://clawhub.ai/bailianai/skills/zlbx-company-registry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query-specific company data; successful data queries may consume 3 points per call or page.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
