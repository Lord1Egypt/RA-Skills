## Description:

Research public X content, accounts, keywords, and performance data with SocQ, including endpoint selection, credit estimates, asynchronous tasks, pagination, and raw exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect and analyze public X posts, accounts, communities, trends, and engagement through SocQ while tracking costs and collection coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: X research requests and the SocQ API key are sent to an external service.

Mitigation: Use only for intended public X research, protect the key, and prefer a pinned or preinstalled SocQ CLI over ad hoc execution.

Risk: Credit-metered requests can incur unanticipated costs.

Mitigation: Estimate credits, obtain confirmation for large jobs, and set spending and rate limits on the API key.

Risk: Bulk profile or relationship collection can be misused.

Mitigation: Limit collection to a legitimate, policy-compliant purpose and the requested scope.

## Reference(s):

- [SocQ X API documentation](https://docs.socq.ai/api-manual/x)
- [SocQ MCP and CLI integration](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage](https://github.com/SocQAPI/socq-devtools)
- [Endpoint selection reference](references/platform.md)
- [Authentication reference](references/authentication.md)
- [Billing and cost control reference](references/billing.md)
- [Asynchronous tasks reference](references/async-tasks.md)
- [Pagination and files reference](references/pagination.md)
- [Error handling reference](references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown findings with optional raw JSONL export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes collection time, filters, task status, credit usage, result counts, and coverage limits when available.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
