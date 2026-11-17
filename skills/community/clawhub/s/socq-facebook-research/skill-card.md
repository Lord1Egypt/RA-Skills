## Description:

Research public Facebook content, accounts, keywords, and performance data with SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to collect and analyze public Facebook data through SocQ, including endpoint selection, cost estimates, and asynchronous result retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime installation of an unpinned CLI can execute unreviewed code while the SocQ API key is available.

Mitigation: Prefer a configured hosted MCP server or a preinstalled, pinned CLI; only install if you trust SocQ and keep the API key in the environment.

Risk: Broad or repeated Facebook collection can incur unexpected credit charges.

Mitigation: Review expected credit costs and confirm large-volume or multi-endpoint jobs before submitting.

## Reference(s):

- [SocQ Facebook API documentation](https://docs.socq.ai/api-manual/facebook)
- [SocQ CLI and MCP integration guide](https://docs.socq.ai/integrations/overview)
- [SocQ agent skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ devtools homepage (skill metadata)](https://github.com/SocQAPI/socq-devtools)
- [Facebook endpoint reference](references/platform.md)
- [Authentication](references/authentication.md)
- [Billing and cost control](references/billing.md)
- [Asynchronous tasks](references/async-tasks.md)
- [Pagination and files](references/pagination.md)
- [Errors and recovery](references/errors.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Files]

**Output Format:** [Markdown findings or raw export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status, credit usage, result counts, and incomplete coverage where available.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
