## Description:

Guides agents through collecting and analyzing public Douyin content, accounts, and performance data with SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to discover, collect, and compare public Douyin videos, accounts, comments, live rooms, and products through SocQ, with cost estimates and coverage reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SocQ requests transmit requested public Douyin inputs and results through an external service.

Mitigation: Use only public data, follow platform rules and privacy expectations, and install the SocQ CLI from a trusted or pinned source.

Risk: Exposed API keys or unconstrained paid requests can cause unauthorized use or unexpected credit charges.

Mitigation: Keep SOCQ_API_KEY in the environment, set billing and rate limits, estimate costs, and confirm large paid runs before execution.

Risk: Failed tasks, unsupported filters, or early pagination can leave findings incomplete.

Mitigation: Check terminal task status, preserve cursors and task IDs, and report coverage gaps rather than claiming completeness.

## Reference(s):

- [SocQ Douyin API documentation](https://docs.socq.ai/api-manual/douyin)
- [SocQ integration documentation](https://docs.socq.ai/integrations/overview)
- [SocQ CLI homepage](https://github.com/SocQAPI/socq-devtools)
- [Douyin endpoint reference](references/platform.md)
- [Billing and cost control](references/billing.md)
- [Authentication](references/authentication.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with optional shell commands and export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, inputs, task status, credit use, result count, pagination, and coverage limits when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
