## Description:

Searches WeChat Channels videos by keyword and presents results with engagement metrics, sorted by relevance, recency, likes, or favorites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Users exploring WeChat Channels content use this skill to discover popular videos on a topic and compare engagement metrics such as likes, comments, shares, and favorites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recharge installs payment software and handles payment details unsafely.

Mitigation: Require separate approval for software installation and the exact payment; pin the payment package and correct payment-field validation and shell handling.

Risk: Search terms are sent to RedFox.

Mitigation: Avoid confidential queries.

Risk: Daily subscriptions continue until removed.

Mitigation: Review and remove daily subscriptions when they are no longer needed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/redfox-data/skills/wechat-channels-crawler)
- [Alipay recharge workflow](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown tables and structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include video details and engagement metrics.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
