## Description:

Guides agents in collecting and analyzing public Twitch profiles and recorded videos through SocQ's credit-metered service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect public Twitch channel profiles and recorded-video inventories, estimate request costs, and report findings with pagination and coverage limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitch research queries and the SocQ API key are sent to SocQ's service.

Mitigation: Confirm trust in SocQ before use and keep the API key out of prompts, URLs, and shared files.

Risk: Unpinned CLI execution can retrieve a different package version.

Mitigation: Prefer a preinstalled or pinned @socq/cli version over unpinned npx.

Risk: Requests can consume paid credits, especially across multiple endpoints or pages.

Mitigation: Keep API-key credit limits enabled, check estimated costs, and confirm large-volume requests before submission.

## Reference(s):

- [SocQ Twitch API documentation](https://docs.socq.ai/api-manual/twitch)
- [SocQ MCP and CLI integrations](https://docs.socq.ai/integrations/overview)
- [SocQ devtools homepage](https://github.com/SocQAPI/socq-devtools)
- [Twitch endpoint reference](references/platform.md)
- [Billing and cost control](references/billing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown or text with optional CLI commands and raw export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, credit usage, task status, collection time, page count, and coverage caveats when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
