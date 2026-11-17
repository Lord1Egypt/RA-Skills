## Description:

Queries Vipshop product, review-summary, and review-list APIs so an agent can summarize product pricing, customer sentiment, fit feedback, and purchase recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miketobusy](https://clawhub.ai/user/miketobusy)

### License/Terms of Use:

MIT-0

## Use Case:

Shopping assistants and consumer-facing agents use this skill to gather Vipshop product details and customer-review signals for a specific product ID, then present a concise purchase recommendation. It is most relevant for comparing price, satisfaction, fit, and representative reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes direct Vipshop API calls with embedded shared identifiers and fingerprint tokens.

Mitigation: Use only in environments where those identifiers are acceptable, and prefer a release that removes fixed tokens or uses a documented, user-controlled access method.

Risk: Product and review responses, including reviewer metadata, are written into the working directory.

Mitigation: Make raw-response saving opt-in, minimize reviewer fields before sharing reports, and document retention expectations for generated JSON files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miketobusy/skills/vipshop-product-consultant)
- [Publisher profile](https://clawhub.ai/user/miketobusy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown report with supporting JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an optional product ID; writes product, review-summary, and review-list JSON data in the working directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
