## Description:

Securely copy files between local and remote hosts over SSH. Use for file transfers, remote backups, and deployment tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and run SCP transfers for deployments, backups, and moving files between local and remote hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SCP transfers can send local data to another machine or overwrite destination files when the source path, destination host, account, or remote path is wrong.

Mitigation: Confirm the exact source path, destination host, account, and remote path before execution, and run only transfers the user explicitly intends.

## Reference(s):

- [Scp Tool on ClawHub](https://clawhub.ai/dinghaibin/skills/scp-tool)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
