## Description: <br>
ZERO Trading guides an agent through Hyperliquid market evaluation, ZERO MCP setup, session lifecycle management, risk controls, and operator communications using ZERO's trading engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squaeragent](https://clawhub.ai/user/squaeragent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading operators use this skill to connect an agent to ZERO, evaluate crypto markets, choose strategies, manage paper or explicitly approved live sessions, and receive concise trading updates with risk context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects the agent to a remote trading MCP service with trading-session authority. <br>
Mitigation: Install only when the operator accepts that authority, verify the ZERO MCP endpoint after installation, and keep live mode disabled unless the operator explicitly opts in. <br>
Risk: The setup flow can persist a ZERO MCP connection in local agent configuration. <br>
Mitigation: Review the MCP configuration after installation and remove or change the ZERO server entry if the endpoint or permissions are not acceptable. <br>
Risk: Trading and session history may be shared with ZERO and used for personalized recommendations. <br>
Mitigation: Use paper mode by default and continue only if the operator is comfortable with ZERO receiving trading and session data. <br>
Risk: Weak consent boundaries could allow unwanted session activity if confirmations are skipped. <br>
Mitigation: Require explicit operator confirmation before deployment, show risk parameters first, and require a second confirmation before live trading. <br>


## Reference(s): <br>
- [ZERO homepage](https://getzero.dev) <br>
- [ClawHub skill page](https://clawhub.ai/squaeragent/zero-trading) <br>
- [Layer details](artifact/references/layer-details.md) <br>
- [Strategies](artifact/references/strategies.md) <br>
- [Output templates](artifact/references/output-templates.md) <br>
- [Error codes](artifact/references/error-codes.md) <br>
- [Voice guide](artifact/references/voice-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown and text responses with inline shell commands, JSON MCP configuration snippets, trading-session captions, and operator decision prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can direct agent calls to ZERO MCP tools and requires operator confirmation before session deployment.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
