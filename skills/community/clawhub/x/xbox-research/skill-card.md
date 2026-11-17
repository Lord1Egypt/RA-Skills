## Description:

Research Xbox game listings, regional prices, compatibility, accessibility features, collections, subscriptions, and reviews through Crawlora to build game shortlists without making purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Players and game researchers use this skill to shortlist Xbox or PC games and compare editions, regional prices, compatibility, accessibility, subscription inclusion, and review samples using public catalog evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xbox research queries and the Crawlora API key are sent to Crawlora, and API calls may use credits.

Mitigation: Use a key scoped to this service, limit requests to the needed scope, and monitor credit use.

Risk: Store prices, availability, and subscription inclusion can change or differ by region and do not prove ownership.

Mitigation: Record locale, source URL, and collection time; verify current offers and subscription eligibility before relying on them.

## Reference(s):

- [Xbox research endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/xbox-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown game shortlist with supporting catalog evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product IDs, locale and currency, compatibility and subscription evidence, source URLs, and collection times when available.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
