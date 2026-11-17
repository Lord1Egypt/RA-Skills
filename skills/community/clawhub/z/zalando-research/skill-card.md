## Description:

Researches Zalando products, prices, brands, categories, and storefronts through the Crawlora API and returns structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, researchers, and developers use this skill to compare Zalando listings, check product details and prices, browse categories, and resolve country storefronts without scraping pages directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Crawlora as an intermediary for Zalando lookups.

Mitigation: Do not include sensitive personal data in lookup queries.

Risk: Exposure of the Crawlora API key could allow unauthorized use.

Mitigation: Keep the key in an environment variable; never hardcode, share, or commit it.

## Reference(s):

- [Zalando endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/zalando-research)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance and shell commands with JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Crawlora API key and a market code for product lookups; search and category results cover only the first page.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
