## Description: <br>
Signed access control for OpenClaw agents that wraps MCP tool calls through protect-mcp to add per-tool policies, signed receipts, trust tiers, and local activity digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomjwxf](https://clawhub.ai/user/tomjwxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to wrap OpenClaw MCP servers with local access-control policies, signed receipts, and audit summaries. It supports compliance-oriented review of agent actions and optional enforcement policies for higher-risk tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local signing keys, gateway configuration, and receipt logs may expose sensitive agent activity or integrity material if synced or committed. <br>
Mitigation: Protect keys/gateway.json, protect-mcp configuration, and receipt files from source control and cloud sync as recommended by the security guidance. <br>
Risk: Unpinned npm package installation can change the behavior of the local MCP gateway or verifier over time. <br>
Mitigation: Pin or verify the protect-mcp, @scopeblind/passport, and verifier packages before serious use. <br>
Risk: Shadow mode records activity but does not block risky tool calls. <br>
Mitigation: Enable enforce mode with a narrow policy when blocking or approvals are required. <br>
Risk: Passport, digest, and receipt outputs can disclose local tool-use history. <br>
Mitigation: Use explicit user requests before showing passport, digest, or receipt data. <br>


## Reference(s): <br>
- [ScopeBlind Passport on ClawHub](https://clawhub.ai/tomjwxf/scopeblind-passport) <br>
- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp) <br>
- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify) <br>
- [ScopeBlind documentation](https://www.scopeblind.com/docs) <br>
- [ScopeBlind receipt verifier](https://www.scopeblind.com/verify) <br>
- [protect-mcp GitHub project](https://github.com/scopeblind/protect-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local receipt, digest, policy, approval, and signing-key files created by protect-mcp.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
