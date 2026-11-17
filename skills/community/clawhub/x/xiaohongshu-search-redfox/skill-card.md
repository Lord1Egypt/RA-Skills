## Description:

Searches Xiaohongshu for popular posts by keyword, ranks results by relevance, popularity, and recency, and can generate reports, scheduled subscriptions, and an Alipay recharge flow when API credits run low.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, and talent agencies use the skill to discover trending Xiaohongshu posts, research content opportunities, and plan recurring trend updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The low-credit flow can initiate payment setup and recharge, which may incur charges.

Mitigation: Require explicit approval before installing payment tools or starting a recharge; verify the merchant and exact amount.

Risk: Generated HTML reports may contain untrusted scripts.

Mitigation: Seek fixes for HTML escaping and review generated reports before sharing or opening them.

Risk: Search terms are sent to Redfox.

Mitigation: Do not submit confidential queries.

Risk: Calendar subscriptions can send recurring updates.

Mitigation: Enable recurring subscriptions only when wanted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/redfox-data/skills/xiaohongshu-search-redfox)
- [Xiaohongshu hot-article data format](references/xhs_hot_article_format.md)
- [Alipay recharge flow](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML files, Guidance]

**Output Format:** [Text or JSON results, with an optional generated HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results can include ranking scores and related search suggestions; recurring calendar updates are optional.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
