## Description: <br>
tick-md helps agents coordinate multi-agent work by creating, claiming, tracking, and syncing tasks in Git-backed TICK.md Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gianni-dalerta](https://clawhub.ai/user/gianni-dalerta) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let AI agents maintain a shared project task ledger, coordinate work ownership, record progress, and inspect task dependencies through CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify project task files such as TICK.md. <br>
Mitigation: Keep task files under version control, review changes, and use validation/status commands before syncing. <br>
Risk: Task comments or history may accidentally include sensitive information. <br>
Mitigation: Avoid putting secrets, credentials, or private data in task comments and review task history before sharing. <br>
Risk: MCP configuration edits can change what tools an agent may run. <br>
Mitigation: Require explicit user approval before editing editor MCP configuration files and back up existing config first. <br>
Risk: Remote push commands can publish local task history to a git remote. <br>
Mitigation: Run pull/status workflows by default and require explicit user approval before tick sync --push or git push. <br>
Risk: Delete, force delete, direct edit, import, and non-dry-run undo operations can remove or rewrite task state. <br>
Mitigation: Preview destructive or bulk operations when possible and ask for confirmation before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gianni-dalerta/tick-md) <br>
- [MCP tools reference](artifact/mcp-reference.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [tick-md npm package](https://npmjs.com/package/tick-md) <br>
- [tick-mcp-server npm package](https://npmjs.com/package/tick-mcp-server) <br>
- [tick-md documentation](https://tick-md.dev/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP tool examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local TICK.md task files and suggest MCP configuration changes when the user approves those actions.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata, artifact skill.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
