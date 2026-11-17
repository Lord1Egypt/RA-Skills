## Description:

Install and use solanaprox-mcp 2.0.0, the MCP server for SolanaProx (solanaprox.com): AI models paid per call from a prepaid USDC balance on Solana, for Claude Desktop, Cursor, Claude Code and other MCP clients. Auth is a signed-in solx_ token, never a wallet address. No tool sends funds. Use it when the user wants SolanaProx as MCP tools and agrees to pay for model calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Desktop, Cursor, Claude Code, or another MCP client use this skill to connect to SolanaProx, discover available models and prices, and make model requests or check account and deposit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports an unpinned MCP launch command and incomplete reference resolution, so scan coverage is incomplete.

Mitigation: Review the install command and its package/version against the SolanaProx documentation before installing.

Risk: Model requests send prompts and conversation content to SolanaProx and its selected model provider; ask_ai uses prepaid USDC, and the access token is a bearer credential.

Mitigation: Do not include secrets or personal data, keep the token out of prompts and logs, use a low daily spend cap, and confirm the model and price with the user before a paid request.

## Reference(s):

- [SolanaProx documentation](https://solanaprox.com/docs)
- [SolanaProx service](https://solanaprox.com)
- [MCP server repository (metadata homepage)](https://github.com/solanaprox/mcp-server)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, MCP tool calls]

**Output Format:** [Markdown guidance, shell commands, JSON configuration, and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model requests can incur prepaid USDC charges; available models and prices are retrieved live.]

## Skill Version(s):

4.0.1 (source: server-resolved release metadata, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
