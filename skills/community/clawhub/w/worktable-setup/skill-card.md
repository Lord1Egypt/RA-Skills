## Description:

Set up Worktable for a user or connect their agent to an existing workspace. Use for installation, connection, and optional skills setup; preserve existing workspaces and unrelated client configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worktable](https://clawhub.ai/user/worktable)

### License/Terms of Use:

MIT

## Use Case:

Worktable users and developers use this skill to install Worktable when needed, connect an agent to the intended existing or new workspace, add optional skills, and verify the connection while preserving unrelated client configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install software, persist connection settings, or add optional skills.

Mitigation: Review the installer's dry-run preview and confirm the intended workspace, client, run mode, and skills destination before proceeding.

Risk: External installer packages and releases have not been audited in this assessment.

Mitigation: Use the linked official Worktable documentation and treat external installation results as unverified until checked on the intended host.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/worktable/skills/worktable-setup)
- [CLI install](https://docs.worktable.dev/start/install/)
- [Desktop setup](https://docs.worktable.dev/start/desktop/)
- [Cloud setup](https://docs.worktable.dev/guides/worktable-cloud/)
- [Installer options](https://docs.worktable.dev/reference/installer/)
- [Agent connections](https://docs.worktable.dev/agents/connections/)
- [Skills installation](https://docs.worktable.dev/agents/skills/#installation)
- [Skills management](https://docs.worktable.dev/agents/skills/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
