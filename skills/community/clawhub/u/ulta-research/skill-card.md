## Description:

Researches Ulta Beauty products, shades, customer feedback, categories, and nearby stores through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and product researchers use this skill to find Ulta Beauty products and shades, compare customer questions and reviews, browse categories, and locate nearby stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, product identifiers, and store-location inputs are sent to Crawlora.

Mitigation: Share only information needed for the lookup; use a city or ZIP code instead of a precise home address when sufficient.

Risk: Using the skill requires a Crawlora API key.

Mitigation: Keep the key in the environment and do not include it in prompts, URLs, or committed files.

## Reference(s):

- [Ulta Research on ClawHub](https://clawhub.ai/crawlora-org/skills/ulta-research)
- [Ulta endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON results or concise research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, category, question, and review results may be paginated.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
