## Description: <br>
Google Workspace CLI for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and Workspace APIs, with MCP server mode for agents that need to manage Workspace services through CLI commands or structured tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and configure Google Workspace CLI access, then let an agent work with selected Workspace services through shell commands or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent use can affect live Google Workspace data such as mail, files, calendars, chats, and admin resources. <br>
Mitigation: Use a dedicated or low-privilege account where possible, scope OAuth permissions to the needed services, and require explicit approval before sending messages, changing sharing, editing or deleting data, or performing admin actions. <br>
Risk: Running MCP mode with broad services can expose more Workspace actions to an agent than a task requires. <br>
Mitigation: Prefer service-limited MCP mode and compact tool mode, enabling only the Workspace services needed for the current workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-gws) <br>
- [Google Workspace CLI repository](https://github.com/googleworkspace/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and manual OAuth or service-account setup before live Workspace operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
