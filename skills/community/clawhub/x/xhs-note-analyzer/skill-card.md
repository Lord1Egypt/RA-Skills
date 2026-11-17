## Description:

Queries public Xiaohongshu note details by note ID or full note URL, then helps an agent produce creator-focused Markdown analysis with engagement, author, media, tag, cover-image, and optimization insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brand operators, MCN teams, and content planners use this skill to retrieve public Xiaohongshu note data and analyze content performance, positioning, visual appeal, engagement quality, and optimization opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cover-image workflow downloads an API-supplied image URL to a fixed local path with a shell command.

Mitigation: Review or disable cover-image downloading unless the returned URL is trusted; validate URLs and write to a unique temporary path before visual analysis.

Risk: The skill requires a REDFOX_API_KEY and makes outbound requests to RedFoxHub.

Mitigation: Store the key only in environment or secret configuration, verify its scope and revocation path, and avoid logging or embedding the key.

Risk: Xiaohongshu engagement data may be estimated or represent only a point-in-time snapshot.

Mitigation: Label estimates clearly and use results as directional guidance rather than precise decision data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-note-analyzer)
- [Core workflow](references/core_workflow.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with JSON-backed note details and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch queries may return a JSON array before the agent summarizes each note in Markdown.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
