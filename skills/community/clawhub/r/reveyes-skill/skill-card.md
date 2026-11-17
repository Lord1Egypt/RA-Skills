## Description:

Fetches Amazon product reviews through the Reveyes API across 20 marketplaces and guides an agent to produce e-commerce operations analysis focused on negative reviews and listing improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuojiuya](https://clawhub.ai/user/zhuojiuya)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace operators and e-commerce analysts use this skill to retrieve reviews by ASIN, inspect rating and review fields, and generate actionable recommendations for product quality, logistics, listing accuracy, customer service, and competitive positioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested ASIN and review-fetch parameters to Reveyes using a Reveyes API key.

Mitigation: Install only when this data sharing is acceptable, store the API key in a scoped secret store, and avoid exposing the key in logs, screenshots, repositories, or synced dotfiles.

Risk: Raw review exports can contain reviewer names, profile URLs, review text, media links, and other fields that should be treated as data to minimize.

Mitigation: Share exported review data only with appropriate recipients, redact unnecessary reviewer fields when possible, and avoid retaining raw exports longer than needed.

## Reference(s):

- [Amazon Review Analyzer on ClawHub](https://clawhub.ai/zhuojiuya/skills/reveyes-skill)
- [Reveyes official site](https://www.reveyes.cn)
- [Reveyes Python SDK on PyPI](https://pypi.org/project/reveyes/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Analysis, Guidance]

**Output Format:** [JSON review data followed by Markdown analysis and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVEYES_API_KEY; exported review data may include reviewer names, profile URLs, review media links, ratings, variants, and review text.]

## Skill Version(s):

1.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
