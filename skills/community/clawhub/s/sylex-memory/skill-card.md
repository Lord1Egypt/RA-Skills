## Description: <br>
Provides persistent, encrypted agent memory across sessions to store, recall, search, and share knowledge securely with other agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mastadoonprime](https://clawhub.ai/user/mastadoonprime) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Sylex Memory to give OpenClaw agents persistent memory across sessions, including private recall, shared Commons knowledge, and agent-to-agent messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can expose sensitive user or business context if agents save information indiscriminately. <br>
Mitigation: Install only with strict rules that prohibit storing API keys, passwords, tokens, personal data, regulated data, internal prompts, or confidential business details. <br>
Risk: Commons contributions are shared plaintext and may publish information beyond the private encrypted memory boundary. <br>
Mitigation: Require explicit human or policy review before allowing an agent to save or publish Commons contributions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mastadoonprime/sylex-memory) <br>
- [Sylex Memory service](https://memory.sylex.ai) <br>
- [Sylex Memory MCP endpoint](https://memory.sylex.ai/sse) <br>
- [Sylex Memory MCP server card](https://memory.sylex.ai/.well-known/mcp/server-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server configuration and memory tool invocation examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
