## Description:

Spotify Player helps agents control Spotify playback on headless Linux servers through the spogo CLI using cookie-based authentication without a local OAuth callback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaharsha](https://clawhub.ai/user/shaharsha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and configure spogo, then issue terminal commands for Spotify search, playback control, device selection, and status checks on remote Linux hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spotify session cookies are stored locally and can grant account access if exposed.

Mitigation: Treat sp_dc and sp_t as secrets, create config and cookie files with restrictive permissions, avoid logging or syncing cookie values, and refresh or revoke the Spotify session if files may have been exposed.

Risk: The installation command fetches the latest external spogo CLI version, so behavior may change after review.

Mitigation: Pin spogo to a reviewed version instead of `@latest` for controlled deployments.

## Reference(s):

- [ClawHub Spotify Player skill page](https://clawhub.ai/shaharsha/skills/spotify-linux)
- [spogo GitHub repository](https://github.com/steipete/spogo)
- [Go downloads](https://go.dev/dl/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and TOML/JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cookie-handling guidance and commands that require a Spotify Premium account, Go, and spogo.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
