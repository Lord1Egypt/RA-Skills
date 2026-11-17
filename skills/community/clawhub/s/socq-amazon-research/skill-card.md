## Description:

Guides agents through public Amazon product, review, bestseller, and seller research using SocQ's credit-metered tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect and analyze public Amazon product, review, bestseller, and seller data while tracking credit costs and collection coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon research inputs are sent to SocQ's external service.

Mitigation: Send only public data and review inputs before submitting requests.

Risk: An exposed API key could permit unauthorized billable requests.

Mitigation: Keep SOCQ_API_KEY in the environment, never share it in prompts or URLs, and set key credit limits.

Risk: Large or repeated collections may incur unexpected credits.

Mitigation: Estimate costs, set collection caps, request confirmation for large runs, and avoid blind retries.

Risk: Ad hoc npx installation may use an unreviewed CLI version.

Mitigation: Use a vetted or pinned @socq/cli version in sensitive environments.

## Reference(s):

- [Amazon endpoint selection](references/platform.md)
- [Authentication](references/authentication.md)
- [Billing and cost control](references/billing.md)
- [Asynchronous tasks](references/async-tasks.md)
- [Pagination and files](references/pagination.md)
- [Errors and recovery](references/errors.md)
- [SocQ Amazon API documentation](https://docs.socq.ai/api-manual/amazon)
- [SocQ MCP and CLI integration](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools](https://github.com/SocQAPI/socq-devtools)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, JSON]

**Output Format:** [Markdown with structured results and optional raw JSONL export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, credit usage, task status, pagination, and incomplete coverage.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
