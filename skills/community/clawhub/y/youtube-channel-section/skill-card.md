## Description:

Manage YouTube channel sections by guiding an agent to list or delete sections with the yutu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and channel operators use this skill to have an agent list YouTube channel sections or prepare yutu CLI commands to delete selected channel section IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires YouTube OAuth client credentials and a cached token.

Mitigation: Keep client_secret.json and youtube.token.json out of shared folders and source control, and prefer protected secret storage over raw JSON environment variables.

Risk: The delete operation can remove YouTube channel sections.

Mitigation: Require explicit confirmation before running yutu channelSection delete and use pinned, verified yutu versions where possible.

## Reference(s):

- [Channel Section Delete](references/channelSection-delete.md)
- [Channel Section List](references/channelSection-list.md)
- [Yutu Setup Guide](references/setup.md)
- [yutu GitHub Homepage](https://github.com/eat-pray-ai/yutu)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)
- [ClawHub Skill Page](https://clawhub.ai/openwaygate/skills/youtube-channel-section)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yutu, YouTube OAuth credentials, and a cached token; destructive delete commands should be confirmed before execution.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
