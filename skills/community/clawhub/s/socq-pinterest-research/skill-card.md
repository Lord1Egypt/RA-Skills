## Description:

Helps agents research public Pinterest pins, profiles, and search results through SocQ, including endpoint selection, cost estimates, task polling, pagination, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, marketers, and developers use this skill to collect and analyze public Pinterest content and accounts through SocQ, with cost-aware requests and clear reporting of incomplete results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Pinterest queries, supplied URLs or usernames, and authenticated requests are sent to SocQ.

Mitigation: Use the integration only when sharing those inputs with SocQ is acceptable; keep the API key in the environment and out of prompts or URLs.

Risk: Large or multi-endpoint jobs may consume substantial credits.

Mitigation: Estimate costs, set spending and rate limits on the API key, and confirm large paid jobs before submission.

Risk: Ad hoc npx execution may fetch an unpinned CLI release.

Mitigation: Prefer a pinned or already-installed SocQ CLI.

## Reference(s):

- [SocQ Pinterest API documentation](https://docs.socq.ai/api-manual/pinterest)
- [SocQ integration overview](https://docs.socq.ai/integrations/overview)
- [SocQ Agent Skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ CLI project homepage](https://github.com/SocQAPI/socq-devtools)
- [Pinterest endpoint selection](references/platform.md)
- [Billing and cost control](references/billing.md)
- [Asynchronous tasks](references/async-tasks.md)
- [Pagination and files](references/pagination.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with result summaries and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports selected endpoint, estimated and reported credits, task status, result coverage, and export location when available.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
