## Description:

YouTube transcripts, video details, comments, most replayed moments, search, channels and playlists through the YTAPI REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytapi](https://clawhub.ai/user/ytapi)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve and work with YouTube transcripts, video details, comments, search results, channel uploads, and playlist contents. It is useful when researching or summarizing YouTube content, including when local fetching is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may persist a reusable YTAPI API key across sessions, and signup may create temporary files containing sensitive data.

Mitigation: Use a protected secrets store scoped to this integration or session-only credentials, confirm which configuration files may be changed, protect temporary signup files, and never print the key.

Risk: YTAPI receives search terms and requested video identifiers; signup also sends the user's email, and API use can consume credits.

Mitigation: Avoid confidential search terms and monitor credit usage.

## Reference(s):

- [YTAPI documentation](https://docs.ytapi.dev)
- [YTAPI homepage](https://ytapi.dev)
- [Authentication setup instructions](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Subtitles]

**Output Format:** [API response data, including plain text, Markdown, structured JSON, SRT, and VTT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transcript segments and timestamps, video and channel details, search results, comments, replay heatmaps, and paginated playlist or channel data.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
