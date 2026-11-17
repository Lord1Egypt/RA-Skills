## Description:

Searches German supermarket flyers for product deals from Aldi, Lidl, REWE, EDEKA, Kaufland, and similar retailers via Marktguru, ranking results by price per litre.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benmillerat](https://clawhub.ai/user/benmillerat)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search German supermarket flyer offers by product query and postal code, filter by preferred stores, and summarize the best-value current deals.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: The skill sends each product query and German postal code to Marktguru.

Mitigation: Avoid sensitive searches and use only postal codes you are comfortable sharing with Marktguru.

Risk: The skill extracts and caches Marktguru API/client keys from Marktguru's homepage under ~/.supermarket-deals.

Mitigation: Review the authentication approach before deployment and prefer an approved or documented API path where available.

Risk: Stored default ZIP code, store preferences, and cached keys may remain on the local machine.

Mitigation: Review and remove ~/.supermarket-deals/config.json and ~/.supermarket-deals/keys.json when they are no longer needed.

## Reference(s):

- [Marktguru](https://www.marktguru.de)
- [Marktguru offer search endpoint](https://api.marktguru.de/api/v1/offers/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands; deal results are returned as a text table or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include product details, store, size, price, EUR/L ranking, validity dates, source query, and Marktguru offer URL when available.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
