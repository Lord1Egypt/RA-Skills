## Description:

Generates ready-to-run shell loop commands for Claude Code, Gemini CLI, or Grok CLI, customized by AI tool, model, shell, complexity, and loop controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walkamolee](https://clawhub.ai/user/walkamolee)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create copy-paste automation loop commands for Claude Code, Gemini CLI, or Grok CLI across PowerShell, Windows CMD, and Bash/Linux. It helps configure model choice, shell syntax, iteration counts, time limits, stop-file controls, delays, and generated command files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands may run unattended AI CLI loops and use approval-bypass flags.

Mitigation: Review generated commands before running them, avoid approval-bypass flags unless the workspace is disposable or tightly scoped, and do not run them with elevated privileges or sensitive credentials available.

Risk: Long-running loops may repeatedly modify files or continue beyond the user's intended scope.

Mitigation: Prefer finite iteration counts and time limits, use stop-file controls where appropriate, and keep files under version control before running generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/walkamolee/skills/ralph-loop-writer)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown file with shell-specific command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a timestamped ralphcommand-YYYY-MM-DD-HHMMSS.md file after interactive choices.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
