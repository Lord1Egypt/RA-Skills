## Description: <br>
MCP security gateway that wraps MCP servers with per-tool policies, Ed25519-signed decision receipts, human approval gates, shadow-mode logging, and enforce-mode policy decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomjwxf](https://clawhub.ai/user/tomjwxf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate protect-mcp as a security gateway around MCP servers, applying per-tool policies, approval gates, rate limits, and signed audit receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shadow-mode logs may contain sensitive tool arguments, prompt text, or other workspace data. <br>
Mitigation: Confirm log destinations and retention before installation, restrict log access, and configure redaction or avoid broad shadow logging in workspaces that handle secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomjwxf/scopeblind-protect-mcp) <br>
- [npm package: protect-mcp](https://npmjs.com/package/protect-mcp) <br>
- [protect-mcp documentation](https://scopeblind.com/docs/protect-mcp) <br>
- [OWASP MCP mapping](https://scopeblind.com/docs/owasp) <br>
- [ACTA signed receipts IETF draft](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe CLI installation, policy configuration, shadow or enforce mode operation, approval gates, rate limits, and offline receipt verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
