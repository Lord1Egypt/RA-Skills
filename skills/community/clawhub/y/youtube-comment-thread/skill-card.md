## Description:

Manage YouTube comment threads by helping agents list threads and insert new top-level comments with the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and channel operators use this skill to prepare YouTube comment thread workflows, including listing existing threads and inserting top-level comments after OAuth credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party yutu CLI that handles YouTube account access.

Mitigation: Install yutu only from a trusted distribution source and pin or verify the CLI version where possible.

Risk: OAuth client and cached token files can expose YouTube account access if stored in shared workspaces or repositories.

Mitigation: Keep client_secret.json and youtube.token.json out of shared workspaces and repositories, and restrict file access to the agent runtime that needs them.

Risk: Insert commands can publish public YouTube comments.

Mitigation: Require approval of the exact video, channel, and comment text before running any insert command.

## Reference(s):

- [Yutu Setup Guide](references/setup.md)
- [Comment Thread Insert](references/commentThread-insert.md)
- [Comment Thread List](references/commentThread-list.md)
- [yutu homepage](https://github.com/eat-pray-ai/yutu)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI flag tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yutu command invocations and JSON, YAML, or table output options from the CLI.]

## Skill Version(s):

0.10.7-dev (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
