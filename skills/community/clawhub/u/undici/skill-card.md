## Description:

Use undici for HTTP requests, fetch, connection pooling, proxies, Mock testing, interceptors, caching. Note that undici's fetch differs from built-in fetch (no CORS, must consume body).

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a quick reference for making HTTP requests with undici in Node.js, including fetch, request, streaming, pooling, proxies, mocks, and interceptors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy examples can expose credentials if copied with hardcoded authentication tokens or sent through unprotected proxy endpoints.

Mitigation: Use protected secret storage, avoid hardcoding proxy credentials, and prefer TLS-protected proxy endpoints for authenticated proxies.

Risk: Setting a global dispatcher changes process-wide HTTP behavior.

Mitigation: Prefer per-request dispatchers unless process-wide behavior is intentional and reviewed.

Risk: Leaving response bodies unconsumed can leak connections.

Mitigation: Always consume or dump response bodies, or use HEAD requests when only headers are needed.

## Reference(s):

- [Connection Management: Agent / Pool / Client](references/connection.md)
- [Dispatcher: Low-Level API](references/dispatcher.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no bundled executable behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
