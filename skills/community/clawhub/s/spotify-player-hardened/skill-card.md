## Description:

Terminal Spotify playback/search via spogo (preferred) or spotify_player.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control Spotify playback and search from a terminal through spogo, with spotify_player as a fallback. It is intended for local Spotify Premium workflows that need clear confirmation around authentication and account-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on third-party Spotify command-line tools that may handle Spotify session cookies during authentication.

Mitigation: Install and pin dependencies through a trusted package workflow, confirm authentication imports, and select the browser explicitly before importing a session.

Risk: Spotify credentials or client identifiers could be exposed in chat, logs, or terminal output.

Mitigation: Do not share, print, log, or return Spotify tokens, cookies, client IDs, or refresh tokens.

Risk: Spotify account state can be changed by destructive actions such as deleting playlists, removing saved tracks, or unfollowing artists.

Mitigation: Require explicit user confirmation before destructive or credential-related commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/spotify-player-hardened)
- [Spotify](https://www.spotify.com)
- [Faberlens safety evaluation](https://faberlens.ai/explore/spotify-player)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Spotify Premium and either spogo or spotify_player.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
