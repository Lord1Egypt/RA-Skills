## Description: <br>
RustChain MCP gives AI agents access to RustChain blockchain wallets and token operations, BoTTube video platform actions, and Beacon agent-to-agent communication through a unified MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Scottcjn](https://clawhub.ai/user/Scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect MCP-compatible agents to RustChain wallet and balance tools, BoTTube publishing and engagement actions, and Beacon discovery, registration, messaging, gas, and contract workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate financial and token-related actions, including signed transfers and Beacon gas deposits. <br>
Mitigation: Require explicit human approval before transfers or gas deposits, and verify wallet addresses, amounts, signatures, and authorization keys before execution. <br>
Risk: The skill can publish or modify public content through uploads, comments, votes, and outbound Beacon messages. <br>
Mitigation: Review content, recipients, and platform actions before allowing public posting or agent-to-agent messaging. <br>
Risk: The security evidence states that TLS certificate verification is disabled while the code handles credentials and signed transaction data. <br>
Mitigation: Avoid sending secrets, relay tokens, API keys, private content, or signed transaction material through the skill until TLS verification is fixed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Scottcjn/rustchain-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/Scottcjn) <br>
- [RustChain website](https://rustchain.org) <br>
- [BoTTube platform](https://bottube.ai) <br>
- [Beacon protocol](https://rustchain.org/beacon) <br>
- [PyPI package](https://pypi.org/project/rustchain-mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [JSON tool responses, Markdown guidance, shell commands, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated network actions for token transfers, uploads, comments, votes, registration, gas deposits, and outbound agent messages.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
