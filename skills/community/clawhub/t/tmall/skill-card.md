## Description:

Tmall helps agents summarize and compare public Tmall flagship store and product page information such as prices, sales volumes, reviews, promotions, and product attributes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to manually trigger lightweight research on public Tmall pages, including product list summaries, product detail extraction, and same-category comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be used beyond its intended scope for account actions, purchases, or attempts to bypass platform controls.

Mitigation: Use it only for explicit public product, store, or comparison research tasks; do not use it for account activity, purchasing, interface reverse engineering, or security bypass.

Risk: Large or repeated collection from Tmall pages could violate platform rules or trigger anti-abuse controls.

Mitigation: Keep collection small, manually triggered, and rate limited, and follow Tmall platform rules.

Risk: Prices, promotions, sales counts, and review counts can change after collection.

Mitigation: Include the collection time when reporting volatile product and promotion data.

## Reference(s):

- [Tmall homepage](https://www.tmall.com/)
- [Tmall product search](https://list.tmall.com/)
- [ClawHub skill page](https://clawhub.ai/codenova58/skills/tmall)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise text or Markdown summaries with product links, extracted fields, and comparison tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should include collection time for volatile price and promotion data and avoid account actions, purchases, security bypass, or batch scraping.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
