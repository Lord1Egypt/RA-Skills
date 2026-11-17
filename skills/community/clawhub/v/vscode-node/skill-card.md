## Description:

Operate on code through a VS Code/Cursor IDE connected as an OpenClaw Node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to operate a connected VS Code or Cursor workspace through OpenClaw Node commands for file work, language navigation, git, tests, debugging, terminal actions, and Cursor Agent delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to control a connected VS Code or Cursor workspace, including file writes and other high-impact IDE actions.

Mitigation: Install it only for trusted workspaces, keep write confirmations enabled for untrusted projects, and keep Gateway command allowlists narrow.

Risk: Terminal commands are powerful when enabled through the connected IDE.

Mitigation: Leave terminal actions disabled unless they are specifically needed, and whitelist only the commands required for the task.

## Reference(s):

- [VS Code Node skill page](https://clawhub.ai/xiaoyaner0201/skills/vscode-node)
- [Publisher profile](https://clawhub.ai/user/xiaoyaner0201)
- [OpenClaw Node for VS Code extension](https://marketplace.visualstudio.com/items?itemName=xiaoyaner.openclaw-node-vscode)
- [cursor-ide-agent related skill](https://clawhub.ai/xiaoyaner0201/cursor-ide-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include OpenClaw node invocations, timeout settings, allowlist guidance, and workspace-relative file paths.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
