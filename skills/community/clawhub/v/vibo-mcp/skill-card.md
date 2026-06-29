## Description: <br>
Access Vibo event music planning through an MCP server so an agent can read event details, manage timelines and song requests, update playlists, join events, and export music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Vibo users use this skill to let an agent access Vibo event music planning data and perform approved updates to songs, sections, guests, playlists, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration uses Vibo account credentials or tokens and may persist session data locally. <br>
Mitigation: Treat VIBO_PASSWORD, VIBO_ACCESS_TOKEN, VIBO_REFRESH_TOKEN, and ~/.vibo-mcp/session.json as secrets; install only when the user trusts the vibo-mcp package. <br>
Risk: Approved write operations can change event music data, guests, playlists, exports, and related planning content. <br>
Mitigation: Review each dry-run preview and approve confirm:true only for intended changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/vibo-mcp) <br>
- [Vibo](https://vibodj.com) <br>
- [vibo-mcp npm package](https://www.npmjs.com/package/vibo-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with configuration snippets and tool-use guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents through authenticated MCP read and confirm-gated write operations.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
