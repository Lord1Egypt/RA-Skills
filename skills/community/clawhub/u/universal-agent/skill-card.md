## Description:

Universal Agent helps an agent interpret a natural language task, generate a shell command or Python script, execute it, retry after errors, and summarize the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to delegate end-to-end local tasks that require command generation, Python scripting, execution, basic recovery, and human-readable result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run AI-generated shell commands or Python code with the user's machine permissions.

Mitigation: Use it only in a disposable sandbox or restricted workspace, avoid confidential files and credentials, and review each generated command or script before execution.

Risk: Optional dangerous mode can reduce the value of built-in confirmation checks for high-risk actions.

Mitigation: Keep dangerous mode disabled for normal use and require explicit human approval before destructive or privileged operations.

Risk: Standalone mode requires LLM API credentials and includes setup patterns that can expose secrets or install remote software.

Mitigation: Provide credentials through controlled environment settings, do not commit real keys, and independently verify installers or remote setup commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/universal-agent)
- [Skill usage reference](references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON status text with inline shell commands, Python code, configuration snippets, and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute generated commands or scripts and return captured output, error details, retry status, and summaries.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
