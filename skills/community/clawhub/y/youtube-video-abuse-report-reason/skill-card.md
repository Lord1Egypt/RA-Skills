## Description:

Manage YouTube video abuse report reasons by helping an agent list available abuse report reasons with the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to inspect available YouTube video abuse report reasons through the yutu CLI. It supports setup guidance for OAuth credentials and the list operation for video abuse report reason data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on OAuth client and token files that can expose YouTube account access if shared or committed.

Mitigation: Keep client_secret.json and youtube.token.json outside shared or committed directories, restrict file permissions, and rotate or revoke OAuth access if exposure is suspected.

Risk: The skill relies on an unpinned third-party yutu CLI release.

Mitigation: Install a pinned, trusted yutu version where possible and review the CLI source or release before using it with account credentials.

Risk: Environment variables may contain raw JSON secrets.

Mitigation: Prefer file paths for credential variables when possible and avoid placing raw JSON secrets in shell history, logs, or shared environment files.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [Video Abuse Report Reason List](references/videoAbuseReportReason-list.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [yutu latest releases](https://github.com/eat-pray-ai/yutu/releases/latest)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash command examples and setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of yutu output formats such as json, yaml, or table.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
