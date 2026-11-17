## Description:

Backup and restore your OpenClaw workspace to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickconstantinou](https://clawhub.ai/user/nickconstantinou)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to back up and restore workspace files through a GitHub repository while configuring required environment variables and credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill can upload more local workspace data than promised.

Mitigation: Use only a private, dedicated GitHub repository and inspect staged files before any push.

Risk: The security summary says secrets and GitHub credentials are handled unsafely in failure paths.

Mitigation: Use a fine-grained token limited to the backup repository, and avoid running the skill on workspaces containing secrets or private data.

Risk: The security guidance says users should not rely on the documented exclusions or secret scanner.

Mitigation: Review the copied backup contents independently before syncing or restoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickconstantinou/skills/publish)
- [Publisher profile](https://clawhub.ai/user/nickconstantinou)
- [ShellCheck](https://www.shellcheck.net/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BACKUP_REPO, OPENCLAW_WORKSPACE, and optionally GITHUB_TOKEN.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
