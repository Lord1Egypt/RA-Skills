## Description:

UDeals helps an agent query and compare membership benefits across platforms such as Meituan, Taobao, JD, Heytea, and UnionPay using keyword, platform, tag, and benefit-type filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawngoethe](https://clawhub.ai/user/shawngoethe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current membership benefits, coupons, lounges, birthday gifts, and related perks, then filter or compare results by platform, tag, keyword, or free/paid type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benefit search terms and selected filters are sent to the third-party UDeals API host.

Mitigation: Avoid sending sensitive personal information in queries and review the returned benefit data before relying on it.

Risk: The skill depends on a public unauthenticated API for current benefit information.

Mitigation: Treat unavailable, stale, or incomplete API responses as a service reliability issue and verify important benefits with the platform before acting.

## Reference(s):

- [UDeals ClawHub listing](https://clawhub.ai/shawngoethe/skills/udeals)
- [UDeals API endpoint](https://udeals.utools.icu)
- [Publisher profile](https://clawhub.ai/user/shawngoethe)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise text summaries with referenced API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filtered benefit names, benefit types, descriptions, redemption timing, and platform comparisons.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
