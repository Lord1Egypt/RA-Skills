## Description:

Prevent 429 retry loops and wasted tokens. Use before expensive API calls or after hitting rate limits. Enforces preflight checks, backoff, and context shrinking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before expensive API calls or after rate-limit failures to decide whether to proceed, enter recovery mode, or pause while reducing retries, concurrency, and context size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may slow or pause work by reducing concurrency, shrinking context, or backing off after rate-limit errors.

Mitigation: Treat those actions as expected rate-limit recovery behavior and resume normal throughput after a successful minimal probe or when limits reset.

## Reference(s):

- [ClawHub Rate Limit Guard release](https://clawhub.ai/dodge1218/skills/rate-limit-guard)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown guidance with a concise next-action recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend proceeding, entering recovery mode, pausing, reducing parallelism, shrinking context, probing minimally, or applying exponential backoff.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
