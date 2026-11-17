## Description:

Helps agents collect and analyze public Facebook Ad Library ads, advertisers, creatives, and campaign activity through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and marketing teams use this skill to investigate public Facebook Ad Library activity, estimate SocQ credits, and collect paginated results or raw exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facebook Ad Library queries, supplied page IDs or URLs, and authenticated requests are sent to SocQ.

Mitigation: Use only when the user intends to share those inputs with SocQ; keep the API key in the environment.

Risk: The CLI fallback may install an unpinned package.

Mitigation: Prefer a pinned or preinstalled socq CLI.

Risk: Large or multi-endpoint requests may incur substantial credits.

Mitigation: Review estimated credits, set API-key credit limits, and obtain user confirmation before large runs.

## Reference(s):

- [SocQ Facebook Ad Library API documentation](https://docs.socq.ai/api-manual/facebook-ad-library)
- [SocQ MCP and CLI documentation](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage (release metadata)](https://github.com/SocQAPI/socq-devtools)
- [Endpoint selection and examples](artifact/references/platform.md)
- [Billing and cost control](artifact/references/billing.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with optional commands and export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports collection scope, task status, result count, credit usage, and incomplete coverage.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
