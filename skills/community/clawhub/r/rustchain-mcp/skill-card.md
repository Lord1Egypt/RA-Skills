## Description:

Access RustChain blockchain wallets and tokens, BoTTube AI video platform features, and Beacon agent communication tools via a unified MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect MCP-capable agents to RustChain, BoTTube, and Beacon. It supports blockchain queries, wallet and token actions, video platform actions, and agent-to-agent communication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle sensitive API keys, relay tokens, admin keys, and wallet signatures.

Mitigation: Provide credentials only in reviewed environments, restrict scopes, rotate exposed tokens, and inspect proposed tool calls before using authenticated or signed actions.

Risk: Security evidence reports insecure network settings.

Mitigation: Prefer a version that enables TLS verification, and use only trusted endpoints when providing credentials or signatures.

Risk: The skill includes state-changing actions that can post publicly, upload content, send messages, transfer RTC, or spend RTC gas.

Mitigation: Require explicit approval and clear spending or posting limits before enabling write, transfer, deposit, or messaging tools.

Risk: Security evidence identifies an under-disclosed promotional outreach script.

Mitigation: Remove, disable, or separately review the outreach script before deployment; use dry-run behavior when evaluating it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scottcjn/skills/rustchain-mcp)
- [RustChain](https://rustchain.org)
- [BoTTube](https://bottube.ai)
- [Beacon Atlas](https://rustchain.org/beacon)
- [PyPI: rustchain-mcp](https://pypi.org/project/rustchain-mcp/)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON tool results and inline shell or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results may include wallet, token, video, or agent messaging data. Some tools can perform state-changing actions such as uploads, comments, votes, token transfers, gas deposits, or outbound messages.]

## Skill Version(s):

0.3.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
