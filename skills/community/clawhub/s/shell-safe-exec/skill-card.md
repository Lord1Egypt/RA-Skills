## Description:

Safely run project-local build, test, lint, format, type-check, and dependency-install commands with strict restrictions to prevent destructive or system-wide effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent run repo-local verification, formatting, build, dependency installation, and status commands while avoiding destructive or privileged operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps an agent run limited project-local commands, including dependency installation and workspace-modifying checks.

Mitigation: Review commands before execution, especially when they install dependencies or modify the workspace.

Risk: Unsafe shell input handling can turn user-provided paths or parameters into command injection risk.

Mitigation: Pass user-provided paths and parameters literally and prefer existing repository commands over ad hoc shell pipelines.

Risk: Unexpected retries or broader follow-up commands could exceed the skill's intended safety boundary after a failure.

Mitigation: Stop on first failure and return the real error instead of attempting privileged, destructive, or system-wide recovery commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sf0799/skills/shell-safe-exec)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text status summaries with shell commands and key error output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state the command run, whether it succeeded or failed, and the key error information when a command fails.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
