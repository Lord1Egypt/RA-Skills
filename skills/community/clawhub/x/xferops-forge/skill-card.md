## Description: <br>
Manage projects and tasks with the Forge project management API via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parker-xferops](https://clawhub.ai/user/parker-xferops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to configure Forge MCP access, manage Forge boards and team membership, and move development tickets through the daily workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures an npm-based Forge MCP adapter that can act on project data. <br>
Mitigation: Install it only from a trusted environment after confirming trust in the Forge service, @xferops/forge-mcp package, and publisher. <br>
Risk: Forge API tokens can authorize changes to tasks, boards, columns, and team membership. <br>
Mitigation: Use a scoped, revocable token and store it only in trusted local configuration or a secret manager. <br>
Risk: Some documented operations are destructive, including deleting projects, deleting columns, and changing team membership. <br>
Mitigation: Require explicit confirmation before destructive actions and move or back up relevant project data before deletion. <br>


## Reference(s): <br>
- [Forge service](https://forge.xferops.dev) <br>
- [XferOps Forge on ClawHub](https://clawhub.ai/parker-xferops/xferops-forge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Forge MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
