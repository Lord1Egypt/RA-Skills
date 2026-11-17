## Description:

Read, manage, share, upload, and download OneDrive files via the Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Microsoft OneDrive and SharePoint document libraries through Microsoft Graph shell tooling, including file operations, sharing, permissions, drive targeting, and token management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad Microsoft Graph access for OneDrive and SharePoint read, write, delete, and sharing operations.

Mitigation: Use reduced Microsoft Graph scopes where possible, prefer a dedicated account, and review commands before running actions that modify or share files.

Risk: Access tokens, refresh tokens, and client secrets are handled by shell commands and local credential files.

Mitigation: Keep credential files private, avoid printing or passing live tokens in logged shells, and do not set live tokens through unsafe environment or command history patterns.

Risk: The bootstrap path performs host setup while handling live credentials.

Mitigation: Avoid the bootstrap script on shared or production hosts; run setup in an isolated environment and review host changes before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/trendex-onedrive)
- [Microsoft Graph OneDrive overview](https://learn.microsoft.com/en-us/graph/api/resources/onedrive)
- [DriveItem resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [Large file upload](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession)
- [Sharing concepts](https://learn.microsoft.com/en-us/graph/api/resources/sharing)
- [API reference](references/api-reference.md)
- [Permissions](references/permissions.md)
- [Setup guide](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands perform Microsoft Graph requests using configured OAuth tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
