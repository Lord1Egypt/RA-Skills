## Description:

Helps agents conserve tokens, context, requests, retries, and time by using batching, context compression, cache reuse, backoff, circuit breakers, and provider failover during timeouts, rate limits, and network or provider errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to guide resource-aware execution, including context minimization, duplicate request avoidance, retry budgeting, backoff, failover, and graceful degradation. It is most relevant when an agent must stay stable under constrained context, rate limits, timeouts, or unreliable providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes under-scoped guidance to rotate or revoke API keys, regenerate credentials, block connections, and perform audits beyond its core resource-saving purpose.

Mitigation: Treat those steps as recommendations only unless the user explicitly authorizes the credential or connection action and defines the scope.

Risk: Retry, failover, and provider-routing guidance can increase external requests or change providers if applied without limits.

Mitigation: Require bounded retry counts, backoff with jitter, circuit-breaker thresholds, and a compatibility check before provider failover.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/token-connection-guard)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with checklists, decision rules, and occasional command-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces operational guidance; it does not define executable tools or required binaries.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
