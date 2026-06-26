## Description: <br>
Create, read, update, and delete memos on a Memos instance using openclaw-memos-mcp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinhong2011](https://clawhub.ai/user/sinhong2011) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to manage notes in a self-hosted Memos instance, including creating, searching, updating, and deleting memos through an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an access token for a Memos server. <br>
Mitigation: Use a least-privileged token when available and connect only to a trusted Memos instance. <br>
Risk: Creating public memos can expose note content to unintended readers. <br>
Mitigation: Keep the default PRIVATE visibility unless the user explicitly requests public visibility. <br>
Risk: Deleting a memo is irreversible. <br>
Mitigation: Review and confirm every delete request before calling the delete tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinhong2011/usememos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and MCP tool-use instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to call Memos MCP tools that create, read, update, or delete notes.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
