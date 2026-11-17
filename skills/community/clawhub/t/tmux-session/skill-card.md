## Description:

Claude终端复用工具 is an instruction-only tmux helper that guides agents through local session and window management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to manage local tmux sessions and windows for project work, task tracking, and collaborative terminal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command and write authority for tmux-related work.

Mitigation: Review proposed commands before execution and require confirmation before closing, changing, or writing to active sessions and windows.

Risk: The security scan reports vague and inconsistent instructions despite finding no hidden scripts.

Mitigation: Use the skill only for tmux tasks and review its guidance carefully before installation or operational use.

Risk: The artifact discusses API keys without clearly identifying the provider or need.

Mitigation: Do not provide API keys unless the provider, purpose, and storage approach are confirmed for the deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only Markdown skill; no bundled executable scripts were present in the artifact.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
