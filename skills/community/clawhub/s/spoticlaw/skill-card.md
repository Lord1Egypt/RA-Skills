## Description:

SpotiClaw is a Spotify Web API client for Nyx agents that supports search, playback, playlists, library operations, and media metadata workflows with Spotify OAuth credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ledzgio](https://clawhub.ai/user/ledzgio)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use SpotiClaw to let Nyx agents interact with Spotify accounts, including searching catalog data, controlling playback, managing playlists, and reading or updating library state. It is intended for authenticated Spotify automation where the operator has configured the required Spotify app credentials and local OAuth token cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make account-changing Spotify actions, including playback control, playlist changes, library changes, and public-content changes.

Mitigation: Require explicit user confirmation before playlist, library, playback, or public-content changes, and install only where that level of account control is acceptable.

Risk: The skill relies on reusable plaintext Spotify credentials and token cache files.

Mitigation: Keep .spotify_cache and .env out of shared folders and source control, restrict filesystem permissions, and rotate or recreate tokens if they may have been exposed.

Risk: The requested Spotify scopes include private playlist reads, listening history, top-artist or top-track data, and library modification.

Mitigation: Use a dedicated Spotify app with the minimum scopes needed for the intended workflow and review scope grants before authorizing.

## Reference(s):

- [ClawHub SpotiClaw skill page](https://clawhub.ai/ledzgio/skills/spoticlaw)
- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api)
- [Spotify authorization code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets and shell commands; runtime primitives return Spotify Web API JSON objects and perform authenticated Spotify account actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, and a local .spotify_cache OAuth token file.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
