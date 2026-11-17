## Description:

ScopeBlind Passport wraps OpenClaw MCP tool calls through protect-mcp to add per-tool policies, signed receipts, trust tiers, and local activity reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomjwxf](https://clawhub.ai/user/tomjwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to wrap OpenClaw MCP servers so tool calls are logged, policy-checked, rate-limited, and recorded with independently verifiable receipts. It is suited for audit, compliance, approval, and daily activity review workflows around agent tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm execution and unpinned package references can change the code executed during installation or runtime.

Mitigation: Pin and lock protect-mcp and @scopeblind/passport package versions before deployment.

Risk: Some policy packs allow unknown tools by default, which may leave sensitive MCP servers exposed if tool names are not explicitly covered.

Mitigation: Review the generated MCP configuration, verify every exposed tool name is covered, and use strict or default-deny policies for sensitive servers.

Risk: Session-scoped approvals can allow trusted tools for longer than a single request.

Mitigation: Prefer one-time approvals for sensitive actions and reserve 24-hour approvals for tools that are intentionally trusted.

## Reference(s):

- [ScopeBlind Passport on ClawHub](https://clawhub.ai/tomjwxf/skills/scopeblind-passport)
- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp)
- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- [ScopeBlind documentation](https://www.scopeblind.com/docs)
- [ScopeBlind receipt verifier](https://www.scopeblind.com/verify)
- [protect-mcp GitHub project](https://github.com/scopeblind/protect-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP wrapping instructions, policy pack selection guidance, approval flow commands, and receipt status or digest commands.]

## Skill Version(s):

0.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
