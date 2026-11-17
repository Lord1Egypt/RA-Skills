## Description:

Provides guidance and commands for installing, authenticating, troubleshooting, and managing Viam robotics platform resources through the Viam CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexbabe](https://clawhub.ai/user/hexbabe)

### License/Terms of Use:


## Use Case:

Developers and robotics operators use this skill to work with Viam CLI workflows for fleet, machine, module, data, dataset, pipeline, and ML operations. It is suited for agent-assisted command selection, setup guidance, and troubleshooting against the user's installed Viam CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Viam CLI authority could allow an agent to modify robotics fleet, machine, data, credential, deployment, or remote-shell state beyond the intended task.

Mitigation: Use Viam accounts and machine parts scoped to the task, and require explicit user approval before API key creation, remote shell, file copy, module reload/upload, database-user changes, data export, or deletion.

Risk: Installing or upgrading the Viam CLI through Homebrew changes the local toolchain used by the agent.

Mitigation: Verify the Homebrew source and Viam CLI version before approving installation or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexbabe/skills/viam-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for explicit user approval before installation, upgrades, destructive operations, API key creation, remote shell, file copy, module reload/upload, database-user changes, or data export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
