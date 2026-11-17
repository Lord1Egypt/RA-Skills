## Description:

Helps agents research public Facebook Marketplace listings, sellers, prices, and product details through SocQ, including endpoint selection, credit estimates, task polling, pagination, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect and analyze public Facebook Marketplace listings through SocQ, with cost-aware task execution and transparent reporting of coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SocQ API key is needed for requests and may be exposed if included in prompts or URLs.

Mitigation: Keep SOCQ_API_KEY in the environment, never include it in prompts or URLs, and use rate, credit, and IP limits when available.

Risk: Large or repeated queries may consume paid credits.

Mitigation: Review expected costs, cap the scope, and obtain confirmation before large-volume or multi-endpoint runs.

Risk: Async failures, unsupported filters, or partial pagination can leave research incomplete.

Mitigation: Track task status and pages read, preserve task IDs for recovery, and disclose gaps rather than claim complete coverage.

## Reference(s):

- [SocQ Facebook Marketplace API documentation](https://docs.socq.ai/api-manual/facebook-marketplace)
- [SocQ MCP and CLI integration documentation](https://docs.socq.ai/integrations/overview)
- [SocQ devtools (metadata homepage)](https://github.com/SocQAPI/socq-devtools)
- [Facebook Marketplace endpoint guidance](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [Research summaries, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with findings, task status, credit use, and optional export locations or commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, filters, collection time, result count, pagination, and incomplete coverage when applicable.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
