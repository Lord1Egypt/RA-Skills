## Description: <br>
Place phone calls, send SMS, search contacts, and run agent dispatches via Voxrn from OpenClaw-bridged chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robit-man](https://clawhub.ai/user/robit-man) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users install this skill to let agents place outbound calls, send SMS messages, search or update contacts, monitor active calls, and check Voxrn balance from bridged chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound calls and send SMS messages, which may contact unintended recipients or incur charges. <br>
Mitigation: Verify recipients, message bodies, call tasks, and expected cost before sending texts or placing calls. <br>
Risk: The Voxrn API key is a sensitive credential required for the MCP server. <br>
Mitigation: Store the API key in the OpenClaw secrets manager and never echo it into prompts or chat messages. <br>
Risk: Changing VOXRN_BASE_URL can route authenticated requests to an alternate endpoint. <br>
Mitigation: Use the default Voxrn production endpoint unless the alternate endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/robit-man/voxrn) <br>
- [Voxrn home](https://voxrn.com) <br>
- [Voxrn OpenClaw integration docs](https://voxrn.com/docs/integrations/openclaw) <br>
- [Voxrn MCP overview](https://voxrn.com/docs/agents/mcp) <br>
- [Voxrn API reference](https://voxrn.com/docs/mcp) <br>
- [OpenClaw outbound MCP servers](https://docs.openclaw.ai/cli/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Voxrn telephony actions through an authenticated OpenClaw MCP server.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
