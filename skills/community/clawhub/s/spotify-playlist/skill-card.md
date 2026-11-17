## Description:

Build and manage Spotify playlists from natural language requests, including music search, playlist creation, track management, listening history, and profile lookup through the Spotify Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeaholicman](https://clawhub.ai/user/codeaholicman)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to authenticate with Spotify, search for tracks, artists, and albums, curate playlists, and personalize playlist choices with recent and top listening history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store reusable Spotify OAuth credentials locally.

Mitigation: Review local credential handling before installation and prefer safer secret storage or PKCE where available.

Risk: The skill can read Spotify profile data, listening history, and playlist information.

Mitigation: Review requested Spotify scopes and remove unused scopes before authorizing an account.

Risk: The skill can create playlists and add or remove playlist tracks.

Mitigation: Confirm account-changing playlist actions before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeaholicman/skills/spotify-playlist)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [Spotify Accounts authorization endpoint](https://accounts.spotify.com/authorize)
- [Spotify Accounts token endpoint](https://accounts.spotify.com/api/token)
- [Spotify Web API](https://api.spotify.com/v1)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from scripts plus Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Spotify playlists and stores reusable Spotify OAuth credentials locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
