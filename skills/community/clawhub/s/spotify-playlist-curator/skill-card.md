## Description: <br>
Create and refine Spotify playlists using the Spotify Web API, with support for track search, recent and top listening lookups, queueing selected tracks, and curated playlist generation from vibes, seed tracks, and listening history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachel-howell](https://clawhub.ai/user/rachel-howell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Music listeners and agent users use this skill to create, refine, analyze, and queue Spotify playlists from moods, seed tracks, artists, existing playlists, and listening history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Spotify permissions that can read private playlists and listening history, queue playback, and create or modify playlists. <br>
Mitigation: Install only when those permissions are acceptable, authenticate intentionally, and review playlist changes before allowing modification of existing playlists. <br>
Risk: Saved Spotify tokens, environment credentials, and taste-profile data are sensitive local files. <br>
Mitigation: Keep .env, spotify_tokens.json, and taste_profile.json out of shared or backed-up folders, use SPOTIFY_TOKENS_PATH for a private location when appropriate, and delete saved taste notes that should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rachel-howell/spotify-playlist-curator) <br>
- [Setup guide](references/setup.md) <br>
- [Implementation notes](references/implementation-notes.md) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [ReccoBeats](https://reccobeats.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Spotify playlists, queue tracks, and store local OAuth tokens and taste-profile data when authorized.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
