## Description:

Guides agents through collecting and analyzing public Threads posts and profiles with SocQ, including endpoint selection, credit estimates, asynchronous tasks, pagination, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect public Threads posts and profiles through SocQ, manage credit-metered tasks, and summarize or export results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SocQ API key is required for authenticated requests to SocQ services.

Mitigation: Provide SOCQ_API_KEY only through the environment; do not put it in prompts, URLs, or saved commands.

Risk: Ad hoc npx execution can fetch an unpinned CLI version.

Mitigation: Prefer a pinned or preinstalled @socq/cli version.

Risk: Large or multi-endpoint collections can consume paid credits.

Mitigation: Estimate costs and obtain confirmation before large paid runs.

Risk: Partial pagination or provider failures can make results incomplete.

Mitigation: Report pages read, collection limits, and failures; do not claim complete coverage when collection stops early.

## Reference(s):

- [SocQ Threads API documentation](https://docs.socq.ai/api-manual/threads)
- [SocQ integration documentation](https://docs.socq.ai/integrations/overview)
- [SocQ devtools homepage](https://github.com/SocQAPI/socq-devtools)
- [Threads endpoint selection](references/platform.md)
- [Billing and cost control](references/billing.md)
- [Authentication](references/authentication.md)
- [Asynchronous tasks](references/async-tasks.md)
- [Pagination and files](references/pagination.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with research summaries, task details, and export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credit usage, pagination coverage, failures, and incomplete results when available.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
