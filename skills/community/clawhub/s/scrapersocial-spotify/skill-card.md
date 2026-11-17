## Description:

Retrieves public Spotify catalogue data through ScraperSocial, including tracks, albums, artists, playlists, top tracks, and search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up public Spotify catalogue metadata and search results through ScraperSocial without Spotify OAuth. It does not provide audio, private libraries, or playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spotify lookup inputs and the API key are sent to ScraperSocial.

Mitigation: Use only with approval for this third-party provider; protect the API key and avoid sensitive lookup inputs.

Risk: Requests may consume API credits, including credits per result for search and top tracks.

Mitigation: Set a suitable result limit and review expected costs before making large or repeated queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/scrapersocial-spotify)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns catalogue data and a request ID; paginated results may include a cursor. Requests may consume API credits.]

## Skill Version(s):

1.0.4 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
