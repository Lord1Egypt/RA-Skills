## Description:

statsfm helps agents query stats.fm data for public Spotify and Apple Music catalog information, global charts, and, with a stats.fm username, personal listening history, play counts, top items, monthly breakdowns, and currently playing tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space0mel](https://clawhub.ai/user/space0mel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for music listening analysis, artist and album deep dives, discovery timelines, personal stats.fm history, and public chart or catalog lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a stats.fm username, listening-history query parameters, and detected timezone to stats.fm.

Mitigation: Use it only when that disclosure is acceptable, avoid saving the username in shared environments, and request narrow queries when broad history analysis is not wanted.

Risk: The skill may make many stats.fm API queries during deep music-history analysis.

Mitigation: Constrain the requested date range, artist, album, or chart scope when minimizing data exposure or request volume matters.

## Reference(s):

- [stats.fm API Reference](references/api.md)
- [stats.fm API](https://api.stats.fm/api/v1)
- [ClawHub skill page](https://clawhub.ai/space0mel/skills/statsfm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown narrative with CLI command references and summarized stats.fm results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include personal listening-history statistics when a stats.fm username is supplied.]

## Skill Version(s):

2.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
