## Description:

Collect and analyze public Google Play app details, rankings, and reviews with SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and analysts use this skill to collect and compare public Google Play app details, rankings, and reviews, with credit estimates, task tracking, and pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SocQ API credentials or research queries may be exposed to unintended parties.

Mitigation: Trust SocQ before use; keep the API key in the environment and out of prompts, URLs, and retained commands.

Risk: Credit-metered tasks may incur unexpected charges, especially when retried or run at scale.

Mitigation: Estimate credits, set spending limits where available, obtain approval for large runs, and reuse task IDs or idempotency keys on retry.

Risk: Ad hoc CLI execution may introduce supply-chain exposure.

Mitigation: Prefer a pinned or preinstalled SocQ CLI over repeated ad hoc npx execution.

Risk: Incomplete pagination or provider failures can produce misleading conclusions.

Mitigation: Report collection time, pages read, unsupported filters, and incomplete coverage; do not claim completeness when collection stops early.

## Reference(s):

- [SocQ Google Play API documentation](https://docs.socq.ai/api-manual/google-play)
- [SocQ integrations overview](https://docs.socq.ai/integrations/overview)
- [SocQ devtools (listed homepage)](https://github.com/SocQAPI/socq-devtools)
- [Google Play endpoint reference](references/platform.md)
- [Billing and cost control](references/billing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown findings or a raw JSONL export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, filters, credit use, task status, result count, pagination, and incomplete coverage.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
