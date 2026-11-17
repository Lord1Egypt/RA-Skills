## Description:

Guides agents in collecting and analyzing public Google Maps places and reviews through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to find public Google Maps places, collect place details and reviews, and summarize results through SocQ's paid data services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SocQ requests transmit an API key to external SocQ services.

Mitigation: Use a scoped SOCQ_API_KEY in the environment, never expose it in prompts or URLs, and set rate and spend limits.

Risk: Large or repeated collections can incur unexpected credit charges.

Mitigation: Check live pricing, confirm the scope of large paid jobs, and avoid blindly resubmitting failed tasks.

Risk: Ad hoc npx execution can fetch a newer CLI package than expected.

Mitigation: Prefer a pinned or preinstalled @socq/cli version.

## Reference(s):

- [Google Maps endpoint guide](artifact/references/platform.md)
- [SocQ Google Maps API documentation](https://docs.socq.ai/api-manual/google-maps)
- [SocQ MCP and CLI integration guide](https://docs.socq.ai/integrations/overview)
- [SocQ CLI tooling](https://github.com/SocQAPI/socq-devtools)
- [SocQ billing and cost guidance](artifact/references/billing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown summaries with optional command examples and links to normalized results or raw JSONL exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status, result count, credit usage, and incomplete coverage when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
