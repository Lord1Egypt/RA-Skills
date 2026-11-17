## Description:

A universal MCP-compatible skill that lets an agent delegate code refactoring, large-scale code generation, debugging, tests, shell commands, and local file changes to the Anthropic Claude Code CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bighit1](https://clawhub.ai/user/bighit1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to invoke local Claude Code for project-scale code changes, debugging, running tests, and shell work in a target workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated Claude CLI execution can run commands and edit files while permission prompts are disabled.

Mitigation: Use a disposable or tightly scoped workspace, review resulting changes, and run the skill only when broad local coding delegation is intended.

Risk: Sensitive environment variables may be available to the delegated CLI process.

Mitigation: Run without sensitive environment variables or secrets in scope.

Risk: Project paths and command strings require careful handling, especially for PowerShell execution.

Mitigation: Prefer a version that validates project paths and avoids PowerShell command-string execution before production use.

## Reference(s):

- [ClawHub use-claudecode release page](https://clawhub.ai/bighit1/skills/use-claudecode)
- [Anthropic Claude Code documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text terminal output with command results, diagnostics, and generated code or guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run for up to 600 seconds and may modify files in the provided project path through the delegated Claude CLI.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
