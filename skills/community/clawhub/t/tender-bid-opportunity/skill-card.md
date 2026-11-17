## Description:

按业务范围检索和筛选招投标公告、采购意向及拟建项目，提供有来源和筛选依据的商机清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business-development teams with defined product or industry criteria use this skill to shortlist relevant tender opportunities by region, budget, stage, and date, while separating active candidates from early leads and historical awards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender queries and account requests are sent to an external API and data calls may consume provider credits.

Mitigation: Review the provider and expected charges before use; limit queries and confirm before broad or paginated searches.

Risk: Optional auto-registration sends operating-system, architecture, and hashed MAC data to the provider and stores a returned API key locally.

Mitigation: Set ZLBX_API_KEY directly to avoid device registration, or obtain explicit consent before registering and protect the stored key.

Risk: Search results may contain business contact information or out-of-date project status.

Mitigation: Respect masked contacts, avoid bulk contact exports, and verify deadlines and current status against the linked announcement before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bailianai/skills/tender-bid-opportunity)
- [知了标讯 platform](https://ai.zhiliaobiaoxun.com/)
- [Tender search API reference](references/api-search.md)
- [Company analysis API reference](references/api-company.md)
- [Market analysis API reference](references/api-market.md)
- [Account API reference](references/api-account.md)
- [Business registry API reference](references/api-registry.md)
- [Auto-registration and privacy reference](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with a sourced shortlist and screening rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search criteria, announcement links, project stage, relevant dates, amount units, and unknowns; API queries may consume provider credits.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
