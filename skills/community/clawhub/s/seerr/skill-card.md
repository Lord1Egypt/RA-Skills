## Description:

Search for movies and TV shows through a Seerr instance and request them for download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ximga](https://clawhub.ai/user/ximga)

### License/Terms of Use:


## Use Case:

External users and media server operators use this skill to search Seerr for movies or TV shows, inspect availability, and queue requests through Seerr-backed Radarr and Sonarr workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit media requests after broad search-like prompts without explicit confirmation of the exact item.

Mitigation: Require the agent to show the exact title, year, TMDB ID, media type, and requested seasons before it sends any request.

Risk: The required Seerr API key may allow the agent to create media requests.

Mitigation: Use HTTPS for non-local Seerr URLs, store the key only in the agent environment, and prefer a limited API key if Seerr deployment policy supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ximga/skills/seerr)
- [Publisher profile](https://clawhub.ai/user/ximga)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Plain text or Markdown responses with Seerr API calls, curl examples, and Discord message payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEERR_URL and SEERR_API_KEY; may include poster image URLs in Discord media fields.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
