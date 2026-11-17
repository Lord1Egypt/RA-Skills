## Description:

Search and manage Spotify playlists, tracks, albums, artists, playback, and library state through the Spotify Web API using ClawLink-hosted OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a Spotify account, discover available Spotify tools, search music content, manage playlists and library items, and control playback from an agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ClawLink with Spotify OAuth access, so actions are limited by the scopes the user grants and the connected Spotify account.

Mitigation: Review the scopes shown during Spotify authorization and revoke or uninstall the connection when access is no longer needed.

Risk: Playlist edits, library changes, follows, cover uploads, and playback control can modify the user's Spotify account or listening session.

Mitigation: Preview and explicitly confirm write actions before execution, especially destructive or bulk changes.

Risk: Playback control may fail when the account lacks Spotify Premium or has no active playback device.

Mitigation: Confirm Spotify Premium status and an active Spotify device before attempting playback-control operations.

## Reference(s):

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [Spotify Developer Console](https://developer.spotify.com/console/)
- [Spotify OAuth Guide](https://developer.spotify.com/documentation/general/guides/authorization/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=spotify-audio)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClawLink tool names, Spotify identifiers, preview guidance, and user confirmation steps for write operations.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
