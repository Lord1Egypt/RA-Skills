## Description:

Look up a YouTube channel by @handle or ID and retrieve its latest or sorted uploads, playlists, or playlist videos through YTAPI for creator research and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytapi](https://clawhub.ai/user/ytapi)

### License/Terms of Use:

MIT-0

## Use Case:

People researching or monitoring YouTube creators can retrieve channel profiles, recent or sorted video uploads, playlists, and playlist contents. The results can support creator research or collection of videos for later summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may save the API key for use in future sessions without clearly defining its protection or access scope.

Mitigation: Choose a secrets store or session-only access before setup, and limit which sessions can use the key.

Risk: Account creation sends the user's email and verification code to YTAPI, and API requests consume service credits.

Mitigation: Use private temporary files for signup, and review credit costs and limits before making requests or paging through results.

## Reference(s):

- [YTAPI documentation](https://docs.ytapi.dev)
- [YTAPI batch API guide](https://docs.ytapi.dev/batch/run)
- [YTAPI website](https://ytapi.dev)
- [Skill release page](https://clawhub.ai/ytapi/skills/ytapi-youtube-channels)
- [Authentication setup reference](artifact/references/auth-setup.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON API response data with text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paged channel and playlist results; successful requests consume service credits. An API key is needed for REST requests unless YTAPI tools are available in the session.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
