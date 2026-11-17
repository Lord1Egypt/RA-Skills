## Description:

Tool Enhancement adds 55+ OpenClaw tools for file operations, shell execution, Git workflows, web and API requests, sub-agent orchestration, memory, MCP access, and terminal UI output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntaffffff](https://clawhub.ai/user/ntaffffff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give OpenClaw agents a unified set of local tools for filesystem work, command execution, Git operations, HTTP/API access, memory handling, MCP interaction, sub-agent coordination, and terminal UI rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides broad local-machine authority, including command execution, file deletion, sudo execution, Git push, network/API requests, and persistent memory.

Mitigation: Install only when this authority is intended; run it in a sandboxed workspace with an unprivileged account and manually review high-risk operations before execution.

Risk: Credentials or sensitive data could be exposed through sudo prompts, API requests, shell commands, file operations, or memory persistence.

Mitigation: Avoid entering sudo passwords or API credentials through the skill, keep secrets out of tool inputs and memory, and review network/API requests before sending them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntaffffff/skills/tool-enhancement)
- [Skill source overview](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, terminal text, JSON-like tool results, code snippets, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify files, run local commands, call network APIs, update Git repositories, and persist memory entries depending on the invoked tool.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
