## Description: <br>
Connects an agent to Teambition MCP services to query and manage projects, tasks, members, comments, workflows, custom fields, templates, files, and related project-management data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeandoom](https://clawhub.ai/user/jeandoom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to connect an agent to a Teambition MCP server, configure local account settings, and carry out project-management queries and updates in Teambition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, archive, delete, and change membership or permissions for Teambition project-management data. <br>
Mitigation: Require explicit user confirmation before create, update, archive, delete, member, or permission operations. <br>
Risk: The skill stores local account configuration and may use an optional authentication token in .teambition and .teambition-token files. <br>
Mitigation: Use least-privilege credentials and keep .teambition and .teambition-token out of shared or synced folders. <br>
Risk: Broad activation wording may cause the skill to engage whenever Teambition or project-management topics are mentioned. <br>
Mitigation: Confirm intent before performing write operations and review existing configuration before allowing file writes. <br>


## Reference(s): <br>
- [ClawHub Teambition Skill Page](https://clawhub.ai/jeandoom/tb) <br>
- [Teambition MCP Configuration Page](https://open.teambition.com/user-mcp) <br>
- [Teambition Open Platform Documentation](https://open.teambition.com/docs/documents/639982966b99d5002b510f0b) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands and Teambition MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and local Teambition configuration files for MCP server URL, user ID, and optional authentication token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
