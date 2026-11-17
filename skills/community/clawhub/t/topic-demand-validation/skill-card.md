## Description:

Validate broad topic, problem, audience, or content demand by comparing autocomplete, Google Trends, search results, and sampled discussion. For a physical product launch hypothesis that needs marketplace listings, prices, and review evidence, use consumer-product-opportunity; use brand-mention-research for a known entity's mentions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and product teams use this skill to build a compact evidence brief about search phrasing, search trends, ranked results, and sampled public discussion when deciding whether to explore a topic or content idea. The brief keeps these signals separate and does not claim to validate sales or market size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may expose confidential plans or personal details to Crawlora and its search sources.

Mitigation: Use only topics appropriate to share with those services; remove confidential plans and personal details from queries.

Risk: Successful collection requests consume API credits.

Mitigation: Set a collection budget and keep the initial research pass bounded; agree a wider budget before expanding searches or paging deeply.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [Topic Demand Validation on ClawHub](https://clawhub.ai/crawlora-org/skills/topic-demand-validation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Compact Markdown evidence brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates autocomplete, Trends, search-result, and discussion signals; includes scope and sampling limits; does not estimate sales, market size, or future growth.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
