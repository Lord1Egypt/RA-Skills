## Description:

Helps agents research public social-platform content and SEO data through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and marketing teams use this skill to collect and compare public social content, accounts, and SEO search metrics across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned SocQ tooling can run with an API key.

Mitigation: Use a vetted or pinned CLI/MCP version and keep SOCQ_API_KEY out of prompts, URLs, and saved commands.

Risk: Large or cross-platform research jobs can incur unexpected credits.

Mitigation: Estimate costs, limit scope, and confirm paid or bulk runs before submitting.

Risk: Broad public-data collection can include unnecessary people-focused information.

Mitigation: Limit requests to the user's research purpose and avoid unnecessary collection about individuals.

Risk: Incomplete or mismatched platform results can distort comparisons.

Mitigation: Report failed tasks, pagination limits, and differences in dates, filters, and coverage.

## Reference(s):

- [SocQ skill listing](https://clawhub.ai/socq/skills/socq-social-research)
- [SocQ API documentation](https://docs.socq.ai/api-manual)
- [SocQ MCP and CLI integrations](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage](https://github.com/SocQAPI/socq-devtools)
- [Capability catalog](references/catalog.md)
- [SEO endpoint guide](references/platforms/seo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Research summaries with structured results and optional raw export links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scope, task status, credit usage, result counts, and collection gaps when available.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
