## Description:

Researches Zappos brands and products through the Crawlora API, returning catalog search and product details as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and retail researchers use this skill to find Zappos brands and products and compare prices, ratings, fit feedback, and color options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zappos lookup queries and the Crawlora API key are sent to an external service.

Mitigation: Use only if this data sharing is acceptable; keep CRAWLORA_API_KEY private and review Crawlora's terms if query privacy matters.

## Reference(s):

- [Zappos endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/zappos-research)
- [Crawlora API key and service](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON catalog results or a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and brand results are paginated; product details include up to two featured reviews.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
