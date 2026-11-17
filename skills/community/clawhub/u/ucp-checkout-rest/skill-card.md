## Description:

Implement UCP Checkout over the REST binding for creating, retrieving, updating, completing, and canceling checkout sessions with proper headers, idempotency, status transitions, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichiorca](https://clawhub.ai/user/ichiorca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement REST-based UCP checkout endpoints or clients that follow the UCP session lifecycle, request headers, idempotency behavior, capability negotiation, and message handling patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated merchant-server implementations may fetch a client-provided UCP-Agent profile URL without adequate SSRF controls.

Mitigation: Accept only pre-registered trusted profile origins, reject private and metadata addresses, limit redirects, cap response sizes, set timeouts, and avoid exposing raw fetch errors or content.

Risk: Using stale checkout endpoint shapes, schemas, headers, or status codes can produce incompatible UCP clients or servers.

Mitigation: Check the current UCP checkout REST specification and reference data type documentation before writing production code.

## Reference(s):

- [UCP Reference Data Types](https://ucp.dev/specification/reference/)
- [ClawHub Skill Page](https://clawhub.ai/ichiorca/skills/ucp-checkout-rest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with implementation checklists and code-oriented recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires checking the current UCP specification before writing production code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
