## Description: <br>
Bridges XiaoZhi AI devices to OpenClaw or OpenAI-compatible backends through MCP so agents can call an openclaw_query(message) tool for short spoken responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and XiaoZhi AI integrators use this skill to add OpenClaw or OpenAI-compatible assistant capability to XiaoZhi devices without modifying XiaoZhi source code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice prompts, MCP tool traffic, and backend requests may be sent to external services. <br>
Mitigation: Install only when you intentionally want this routing, configure MCP_ENDPOINT, OPENAI_BASE, and OPENAI_KEY explicitly, and use service providers you trust. <br>
Risk: Secrets or tokenized MCP endpoint URLs may be exposed if configuration files or logs are shared. <br>
Mitigation: Do not publish real .env files or logs that include secrets, and avoid routing sensitive voice content unless the configured providers are acceptable for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joe12801/xiaozhi-mcp-openclaw-official) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses and Markdown setup guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The MCP tool returns concise Chinese text intended for voice playback.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
