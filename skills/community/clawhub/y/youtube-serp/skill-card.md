## Description:

Search YouTube videos, channels, rankings, and trends through AIsa for YouTube research, competitor scouting, and content discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content researchers use this skill to run AIsa-backed YouTube SERP queries, identify top-ranking videos, review competitor presence, and discover content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube queries and the AIsa API key are sent to AIsa's API.

Mitigation: Avoid sensitive query text, keep the API key in environment variables or approved secret storage, and disclose the third-party API call before use.

Risk: SERP-derived rankings and trends may be incomplete, stale, or mistaken for dedicated YouTube channel or trends API data.

Mitigation: Label outputs as AIsa YouTube SERP results, ground summaries in returned records, and state clearly when the upstream returns no results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/youtube-serp)
- [AIsa API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from the bundled CLI plus Markdown summaries or guidance from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; YouTube query terms and the API key are sent to AIsa's API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
