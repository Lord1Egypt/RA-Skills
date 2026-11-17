## Description:

Create and refine Spotify playlists using the Spotify Web API, with support for track search, recent and top listening lookups, queueing selected tracks, and curated playlist generation from vibes, seed tracks, and listening history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachel-howell](https://clawhub.ai/user/rachel-howell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help agents create, revise, analyze, and queue Spotify playlists from natural language music requests, listening history, seed tracks, artists, genres, and existing playlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Spotify OAuth scopes that can read listening history and private playlists, create or modify playlists, and control playback queueing.

Mitigation: Install and authenticate only for Spotify accounts where those permissions are acceptable, and confirm destructive or user-visible playlist changes before applying them.

Risk: The skill stores Spotify tokens and taste preferences locally and calls third-party music services.

Mitigation: Keep the skill directory private, do not share or commit .env, spotify_tokens.json, or taste_profile.json, and consider tightening file permissions or pinning dependencies before use.

Risk: Recommendation quality depends on Spotify, ReccoBeats, and MusicBrainz behavior, so results may be incomplete or heuristic.

Mitigation: Review candidate tracks and the agent's rationale before creating or modifying playlists.

## Reference(s):

- [Spotify Playlist Curator on ClawHub](https://clawhub.ai/rachel-howell/skills/spotify-playlist-curator)
- [Setup](references/setup.md)
- [Implementation Notes](references/implementation-notes.md)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [ReccoBeats](https://reccobeats.com)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local Spotify CLI workflows that create or modify playlists, queue tracks, read listening history, and summarize scored recommendations.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
