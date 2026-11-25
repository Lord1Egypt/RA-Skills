## Description:

Discover winning game and app ad creatives from Denote's weekly Trending, Rising, and New Ads charts. Use for creative research, weekly ad inspiration, free account setup, or a closer look at a ranked ad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denote-developer](https://clawhub.ai/user/denote-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, user acquisition teams, and app developers use the weekly charts to discover popular, rising, and newly spotted game or utility app ads, then review available details to inform creative research and campaign tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Denote authorization key for network requests, and the security review notes that its tool scope is not declared.

Mitigation: Use a key limited to the top_ads:read permission, keep it in the agent host's secret settings, and review the skill's network access before enabling it.

Risk: Static analysis did not cover the bundled JPG images, leaving their contents outside the security review.

Mitigation: Review the bundled image assets separately before deployment if their contents affect your use of the skill.

## Reference(s):

- [Denote Top Ads](https://denote.net/top-ads)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML report, Guidance]

**Output Format:** [Localized chat summary with a generated HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly Trending, Rising, and New charts with available creative media and detail sections.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
