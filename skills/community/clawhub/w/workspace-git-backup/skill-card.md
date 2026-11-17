## Description:

Set up automatic scheduled backups to GitHub or GitLab for an OpenClaw workspace or other directories, with support for GitHub CLI repository setup, macOS launchd, and Linux cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperun](https://clawhub.ai/user/cooperun)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure recurring Git-based backups for local workspaces or selected directories. It helps set up the remote repository, local configuration, scheduled task, and backup management commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled backups may push sensitive, private, or unintended files from a broad local directory to a remote Git repository.

Mitigation: Choose a narrow backup folder, review it for secrets and private data, add exclusions such as .gitignore, and confirm the exact private remote repository before installing the schedule.

Risk: The installed cron or launchd job keeps pushing changes automatically after setup.

Mitigation: Make sure the backup cadence is intended, monitor logs and repository contents after installation, and use the provided uninstall flow when scheduled backups are no longer wanted.

Risk: Editable or untrusted schedule values may create unsafe recurring jobs because schedule validation is not established in the evidence.

Mitigation: Use only reviewed schedule values and avoid accepting schedule strings from untrusted input until validation is added.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and management instructions for scheduled Git backups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
