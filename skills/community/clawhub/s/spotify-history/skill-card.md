## Description:

Access Spotify listening history, top artists/tracks, and get personalized recommendations via the Spotify Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braydoncoyer](https://clawhub.ai/user/braydoncoyer)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent fetch Spotify listening history, top artists, top tracks, and recommendation data after one-time OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants and stores Spotify account access broader than its music-history purpose requires.

Mitigation: Install only on a trusted machine, grant the minimum Spotify scopes needed, and treat the stored OAuth token as sensitive account access.

Risk: The raw JSON command can query arbitrary Spotify API endpoints available to the granted token.

Mitigation: Avoid the raw json endpoint unless the endpoint and data exposure are understood before use.

Risk: Spotify client credentials and tokens are stored on disk for setup and reuse.

Mitigation: Keep credential and token files private, preserve user-only file permissions, and rotate credentials if they are exposed.

## Reference(s):

- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- [Spotify History skill page](https://clawhub.ai/braydoncoyer/skills/spotify-history)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text summaries, JSON API responses, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Spotify OAuth credentials and stores an access token for future API calls.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
