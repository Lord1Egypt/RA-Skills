## Description:

Provides a Node.js API client pattern for OpenAI-compatible endpoints with endpoint failover, key rotation, rate limiting, retries, connection pooling, and circuit breakers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danihe001](https://clawhub.ai/user/danihe001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as guidance and source code for building resilient Node.js API clients that route requests across multiple endpoints and API keys while applying rate limits, retries, and circuit breakers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing authentication headers may be sent to unintended destinations if untrusted request paths or cross-origin absolute URLs are used.

Mitigation: Use only trusted HTTPS endpoints, avoid user-controlled request paths, and patch the client to reject cross-origin absolute URLs or strip credentials when the destination differs from the configured endpoint.

Risk: The server security verdict is suspicious, so using the skill directly with real API keys could expose sensitive credentials or route requests unexpectedly.

Mitigation: Review the source before installation, test with non-production credentials first, and deploy only after confirming endpoint and authentication handling are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danihe001/skills/reliable-api-client)
- [Publisher profile](https://clawhub.ai/user/danihe001)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Markdown with JavaScript code examples and configuration options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable Node.js client code patterns for HTTP requests, endpoint selection, authentication headers, and operational resilience controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
