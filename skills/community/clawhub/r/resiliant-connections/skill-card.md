## Description: <br>
Patterns for building resilient API clients and real-time connections with retry logic, circuit breakers, and graceful degradation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when building production API clients or real-time connections that need retries, circuit breakers, reconnect behavior, fallback handling, and clear degraded-state behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retry examples can be unsafe if copied directly for non-idempotent requests or unsuitable failure classes. <br>
Mitigation: Review request idempotency, retryable status codes, backoff limits, and user-visible degraded states before using the snippets in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/resiliant-connections) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with TypeScript examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes resilience patterns and cautions for retries, circuit breakers, reconnecting WebSockets, and graceful degradation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
