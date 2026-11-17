## Description:

Super Api is a documentation-only REST API reference covering authentication patterns, endpoints, rate limits, pagination, webhooks, and common pitfalls across 147 third-party services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to look up third-party REST API authentication, endpoints, pagination, rate limits, webhook behavior, and common implementation pitfalls before writing integration code or command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may copy examples in ways that expose credentials or place secrets in URLs, logs, or shared shell history.

Mitigation: Use scoped and revocable environment variables, prefer header-based authentication, and avoid real credentials in URLs or shared command history.

Risk: Some examples describe requests that can create, modify, delete, charge, post, or otherwise affect third-party account data.

Mitigation: Confirm intent before running mutating requests and use sandbox or test credentials when available.

Risk: Incorrect handling of rate limits, pagination, retries, or webhook delivery can produce duplicate, incomplete, or misleading integration behavior.

Mitigation: Apply documented backoff, idempotency keys, pagination checks, and webhook signature and idempotency validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-api)
- [Skill overview](artifact/SKILL.md)
- [Setup guidance](artifact/setup.md)
- [Authentication guidance](artifact/auth.md)
- [Credential naming guidance](artifact/credentials.md)
- [Pagination guidance](artifact/pagination.md)
- [Resilience guidance](artifact/resilience.md)
- [Webhook guidance](artifact/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API reference text, curl examples, endpoint tables, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; command examples may require curl and jq and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
