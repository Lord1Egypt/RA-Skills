## Description:

MCP security gateway that wraps any MCP server with per-tool policies, Ed25519-signed decision receipts, human approval gates, shadow-mode logging, and enforce-mode policy application.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomjwxf](https://clawhub.ai/user/tomjwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run an MCP server behind a policy-enforcing gateway that can log tool calls, require approvals, rate-limit selected tools, and produce signed decision receipts for audit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm package execution may change the code an agent runs between installs.

Mitigation: Pin the protect-mcp package version, install it locally, and use a lockfile before deploying it with MCP traffic.

Risk: The gateway can observe broad MCP tool traffic, and shadow mode logs all actions without blocking.

Mitigation: Run the gateway in a constrained environment and decide log retention, access controls, and sensitive-data handling before enabling it on production or confidential MCP traffic.

Risk: Signed receipt integrity depends on how signing keys are generated, stored, and rotated.

Mitigation: Define signing-key storage and operational handling before using signed receipts as an audit control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomjwxf/skills/scopeblind-protect-mcp)
- [protect-mcp npm package](https://npmjs.com/package/protect-mcp)
- [ACTA signed receipts IETF draft](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)
- [ScopeBlind protect-mcp docs](https://scopeblind.com/docs/protect-mcp)
- [ScopeBlind OWASP mapping](https://scopeblind.com/docs/owasp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces install and runtime commands, policy examples, and receipt verification guidance for MCP gateway operation.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
