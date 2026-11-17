## Description:

Helps agents research public LinkedIn accounts, posts, companies, and jobs through SocQ with endpoint selection, credit estimates, pagination, and results reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect and analyze public LinkedIn data via SocQ, estimate credit costs, and report findings or raw export locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkedIn queries, results, and the billing API key are entrusted to an external service.

Mitigation: Use SocQ only when trusted with the submitted data; keep SOCQ_API_KEY in the environment and out of prompts, URLs, and committed files.

Risk: Installing an unpinned CLI version can introduce supply-chain changes.

Mitigation: Prefer a pinned or preinstalled @socq/cli version.

Risk: Large or multi-endpoint runs can incur unexpected credit charges.

Mitigation: Check expected credit costs and obtain confirmation before paid large-volume or multi-endpoint requests.

## Reference(s):

- [SocQ LinkedIn API documentation](https://docs.socq.ai/api-manual/linkedin)
- [SocQ agent skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ CLI and MCP integrations](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools (skill metadata link)](https://github.com/SocQAPI/socq-devtools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with research findings, execution details, and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, filters, credit usage, task status, result coverage, and raw export location when available.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
