## Description:

Helps agents troubleshoot common Xiaohongshu MCP deployment failures by suggesting repair scripts for port conflicts, cookie paths, Chrome download waits, service status checks, and localhost MCP connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when a Xiaohongshu MCP deployment fails due to common local setup issues. It provides command-oriented repair guidance for port conflicts, missing cookies, browser download delays, service startup, and connection checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles session cookies in locations such as /tmp, which can expose credentials on shared or poorly isolated systems.

Mitigation: Use a private configuration directory with restrictive permissions and avoid placing cookies in /tmp.

Risk: The repair guidance can stop any process bound to port 18060 without confirming the process identity.

Mitigation: Inspect the process owner and command before stopping anything on port 18060.

Risk: The one-click flow starts a local binary from /tmp, which can execute unverified code.

Mitigation: Verify the binary source and checksum before execution and prefer a managed service path over nohup background execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/xiaohongshu-mcp-patch)
- [Xiaohongshu MCP project](https://github.com/xpzouying/xiaohongshu-mcp)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown containing Bash command snippets and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may stop local processes, copy cookie files, start a local binary, and test a localhost MCP endpoint.]

## Skill Version(s):

1.0.0 (source: evidence release version and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
