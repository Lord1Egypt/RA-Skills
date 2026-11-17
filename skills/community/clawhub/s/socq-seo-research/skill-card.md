## Description:

Helps agents collect and analyze public SEO data, including keywords, search results, and site rankings, through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

SEO researchers, marketers, and developers use this skill to investigate public keyword demand, search intent, organic results, and website rankings while managing paid SocQ requests and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SocQ API key is required for authenticated requests.

Mitigation: Keep SOCQ_API_KEY in the environment and out of prompts, URLs, and saved commands.

Risk: Large or repeated requests can incur unexpected credit charges.

Mitigation: Review credit estimates, set spending limits where available, and confirm large paid runs before submission.

Risk: Installing the CLI through a package manager introduces supply-chain exposure.

Mitigation: Prefer a pinned or preinstalled @socq/cli for stricter supply-chain control.

## Reference(s):

- [SocQ SEO API documentation](https://docs.socq.ai/api-manual/seo)
- [SocQ MCP and CLI integrations](https://docs.socq.ai/integrations/overview)
- [SocQ devtools (metadata homepage)](https://github.com/SocQAPI/socq-devtools)
- [SEO endpoint reference](references/platform.md)
- [Billing and cost control](references/billing.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, JSON exports]

**Output Format:** [Markdown findings with optional commands or raw JSONL export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, credit usage, task status, result count, coverage, and collection time.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
