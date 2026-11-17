## Description:

Control Spotify playback, search music, manage playlists, generate discovery playlists, and analyze listening habits via the Spotify Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent control Spotify playback, search music, manage playlists, create discovery playlists, and inspect listening data through Spotify's Web API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Spotify account access and can modify playback, playlists, saved tracks, and followed artists.

Mitigation: Review agent requests before execution and limit use to Spotify accounts where these account changes are acceptable.

Risk: Reusable Spotify tokens and app credentials are stored in local config.json without strong protection.

Mitigation: Keep config.json private, exclude it from version control, restrict local file permissions, and use a dedicated Spotify app credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cdmichaelb/skills/spotify-agent)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [Spotify Web API](https://api.spotify.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change Spotify account state, including playback, saved tracks, playlists, queue, and followed artists.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
