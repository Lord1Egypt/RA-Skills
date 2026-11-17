## Description:

Terminal Killer detects OpenClaw user inputs that look like shell commands and routes them for direct local execution, with cross-platform command detection for macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosperypf](https://clawhub.ai/user/cosperypf)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to route concise command-like input directly to local shell execution while leaving natural-language tasks for the LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically run broad local shell commands with the user's account authority.

Mitigation: Install only when direct local command execution is intended; require explicit command-mode invocation and route every execution path through one approval policy before deployment.

Risk: Execution paths and command detection may allow unsafe commands or safety bypasses.

Mitigation: Remove the raw executor, replace shell-string PATH checks with safe argument-vector calls, and require approval or blocking for network, interpreter, destructive, git-push/reset, sudo, and package-install commands.

Risk: Sourcing shell profiles and inheriting environment variables can expose local secrets or alter command behavior.

Mitigation: Stop sourcing shell profiles during detection and restrict inherited environment variables to the minimum needed for command execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosperypf/skills/terminal-killer)
- [README.md](README.md)
- [Terminal Killer skill definition](SKILL.md)
- [Usage examples](references/EXAMPLES.md)
- [Testing guide](references/TESTING.md)
- [Linux builtin command list](references/builtins/linux.txt)
- [macOS builtin command list](references/builtins/macos.txt)
- [Windows builtin command list](references/builtins/windows.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell command output, Configuration guidance]

**Output Format:** [Plain text or Markdown status messages with raw shell command output when execution succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return execute, ask, llm, interactive, long_output, open_terminal, or declined action states.]

## Skill Version(s):

1.2.0 (source: server release metadata, clawhub.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
