## Description:

Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and secure secret read, inject, or run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlecrabzzz-alt](https://clawhub.ai/user/littlecrabzzz-alt)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and authenticate 1Password CLI, verify account access, and run secret-related commands through tmux with guardrails that reduce accidental secret exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps an agent operate 1Password CLI workflows that can access sensitive secrets.

Mitigation: Do not allow secret values to be printed or pasted into chat, logs, or files; prefer `op run` or `op inject` as recommended by the skill and security guidance.

Risk: 1Password commands can fail or repeatedly prompt when authentication state is not preserved.

Mitigation: Run `op` commands inside a fresh dedicated tmux session, unlock or authorize 1Password, and verify access with `op whoami` before reading secrets.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [ClawHub skill page](https://clawhub.ai/littlecrabzzz-alt/skills/test-skill2123)
- [Publisher profile](https://clawhub.ai/user/littlecrabzzz-alt)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume the 1Password CLI binary `op` is installed and authenticated through a dedicated tmux session.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
