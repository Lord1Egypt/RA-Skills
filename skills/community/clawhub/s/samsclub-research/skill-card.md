## Description:

Researches Sam's Club departments, categories, products, related items, and curated pages through the Crawlora API, returning structured catalog data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can browse Sam's Club departments and categories, inspect product pricing, availability, and ratings, and explore related products or curated pages using Crawlora's public-catalog lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public catalog requests are sent to the third-party Crawlora service.

Mitigation: Use only if comfortable with that service, and avoid private or unnecessary query data.

Risk: The Crawlora API key is a credential required for lookups.

Mitigation: Keep the key in the environment; do not hardcode it or include it in query parameters.

## Reference(s):

- [Sam's Club research endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/samsclub-research)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON catalog responses, with optional text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Category results support pagination; product and content lookups use IDs. No free-text search endpoint.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
