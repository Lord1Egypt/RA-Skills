## Description:

Guides agents in collecting and analyzing public Bluesky content, accounts, keywords, and performance data through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to select SocQ endpoints, estimate costs, collect public Bluesky data, and report findings or raw export locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback CLI may fetch and run an unpinned external package.

Mitigation: Use a reviewed, preinstalled or version-pinned SocQ CLI rather than an unpinned npx invocation.

Risk: Research requests and the SocQ authorization token are sent to SocQ.

Mitigation: Use only public data, keep the API key in the environment, and apply key restrictions where appropriate.

Risk: Large or repeated collections may incur unexpected credit charges.

Mitigation: Check current pricing and spending limits, and confirm large paid jobs before submission.

Risk: Bundled endpoint examples and agent configuration target Facebook Ad Library rather than Bluesky.

Mitigation: Verify Bluesky endpoints and MCP configuration against current SocQ documentation before running requests.

## Reference(s):

- [SocQ Bluesky API documentation](https://docs.socq.ai/api-manual/bluesky)
- [SocQ integration overview](https://docs.socq.ai/integrations/overview)
- [SocQ Agent Skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ devtools homepage (release metadata)](https://github.com/SocQAPI/socq-devtools)
- [Authentication](references/authentication.md)
- [Billing and cost control](references/billing.md)
- [Asynchronous tasks](references/async-tasks.md)
- [Pagination and files](references/pagination.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with findings, task details, commands, and raw export links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SocQ API key; collection is asynchronous and credit-metered.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
