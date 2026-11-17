## Description:

Research public Google Ad Library ads and advertisers with SocQ, including endpoint selection, credit estimates, asynchronous collection, pagination, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, marketers, and developers use this skill to collect and analyze public Google Ad Library ads and advertisers through SocQ while tracking credit costs and collection completeness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public ad research queries and the SocQ API key are sent to a third-party service.

Mitigation: Confirm trust in SocQ before use; keep the API key in the environment and out of prompts, URLs, and saved commands.

Risk: Ad hoc CLI installation may run an unexpected package version.

Mitigation: Prefer a pinned or preinstalled @socq/cli version over ad hoc npx execution.

Risk: Large or multi-endpoint collections can incur substantial credits.

Mitigation: Estimate costs, set collection limits, and obtain confirmation before paid large-volume or multi-endpoint runs.

## Reference(s):

- [SocQ Google Ad Library API documentation](https://docs.socq.ai/api-manual/google-ad-library)
- [SocQ MCP and CLI integration guide](https://docs.socq.ai/integrations/overview)
- [SocQ devtools homepage](https://github.com/SocQAPI/socq-devtools)
- [Google Ad Library endpoint reference](references/platform.md)
- [Billing and cost control](references/billing.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown findings with optional raw export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, filters, credit usage, task status, result count, pagination, and coverage limits.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
