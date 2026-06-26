## Description: <br>
Access Telegram data via MCP using the telebiz-tt browser client. Lists chats, reads messages, searches, manages folders, and sends messages through an authenticated Telegram session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acastellana](https://clawhub.ai/user/acastellana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Telegram chats, search and read messages, manage folders, and send or forward messages through an authenticated Telebiz browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes logged-in Telegram actions through unauthenticated local services on ports 9716, 9717, and 9718. <br>
Mitigation: Install only where those ports are inaccessible to other users, websites, containers, and the network; prefer a version that binds to 127.0.0.1 or a protected Unix socket, requires a random auth token, and restricts CORS/origins. <br>
Risk: Agents can invoke destructive or bulk Telegram actions such as deleting chats, deleting messages, archiving chats, sending messages, and batch operations. <br>
Mitigation: Review every destructive or bulk action before execution and disable or scope destructive and batch tools when the deployment does not require them. <br>
Risk: The browser holds an authenticated Telegram session used by the MCP executor. <br>
Mitigation: Keep the browser session secure, monitor health/status output, and stop the relay or HTTP server when agent access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acastellana/telebiz-mcp-skill) <br>
- [Publisher profile](https://clawhub.ai/user/acastellana) <br>
- [Telebiz](https://telebiz.io) <br>
- [Local MCP endpoint](http://localhost:9718/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Telegram chat metadata, message content, folder state, health status, and tool-call results returned by the MCP bridge.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
