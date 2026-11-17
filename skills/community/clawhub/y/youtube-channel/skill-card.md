## Description:

Helps agents list and update YouTube channel information through the yutu CLI, with setup guidance for OAuth credentials and cached tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect YouTube channel details and propose channel metadata updates from an agent workflow. It is useful when authenticated YouTube Data API access is already configured through yutu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets and cached YouTube tokens can expose account access if committed, logged, or shared.

Mitigation: Keep client_secret.json and youtube.token.json private and out of source control; use environment variables or private local files for yutu configuration.

Risk: Channel update commands can change live public YouTube channel metadata.

Mitigation: Confirm the channel ID, requested fields, and intended values before running or approving any yutu channel update command.

Risk: The skill depends on the external yutu CLI package for YouTube API behavior.

Mitigation: Install yutu only from a trusted source and prefer a pinned or verified release.

## Reference(s):

- [Channel List](references/channel-list.md)
- [Channel Update](references/channel-update.md)
- [Yutu Setup Guide](references/setup.md)
- [yutu project homepage](https://github.com/eat-pray-ai/yutu)
- [yutu releases](https://github.com/eat-pray-ai/yutu/releases/latest)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference yutu CLI flags, OAuth credential files, cached token files, and YouTube channel identifiers.]

## Skill Version(s):

0.10.7-dev (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
