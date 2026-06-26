## Description: <br>
Operate on code through a VS Code/Cursor IDE connected as an OpenClaw Node, with commands for file operations, language intelligence, git, testing, debugging, and Cursor Agent CLI integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to operate a connected VS Code/Cursor workspace through OpenClaw Node for reading, editing, navigating, testing, debugging, git operations, and delegating supported tasks to Cursor Agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable powerful IDE workspace actions, including file writes, git operations, testing, debugging, and optional terminal execution. <br>
Mitigation: Install only with a trusted VS Code/Cursor extension and Gateway setup, keep the command allowlist narrow, and leave terminal execution disabled by default. <br>
Risk: Write, commit, or destructive file operations could affect the user's workspace if enabled without review. <br>
Mitigation: Keep write confirmation and read-only protections enabled unless needed, and review diffs before allowing commits or destructive operations. <br>


## Reference(s): <br>
- [OpenClaw Node for VS Code Extension](https://marketplace.visualstudio.com/items?itemName=xiaoyaner.openclaw-node-vscode) <br>
- [cursor-ide-agent Skill](https://clawhub.ai/xiaoyaner0201/cursor-ide-agent) <br>
- [OpenClaw VS Code Project](https://github.com/xiaoyaner-home/openclaw-vscode) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with nodes invoke shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw Node connection, Gateway command allowlist, and paired invokeTimeoutMs/timeoutMs values for longer operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
