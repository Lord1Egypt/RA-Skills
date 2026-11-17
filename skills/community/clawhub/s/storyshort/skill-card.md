## Description:

Create, render and publish AI videos (faceless, UGC ads, movie maker, podcast, music video...) with StoryShort -- plus standalone AI images and clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelrondot](https://clawhub.ai/user/samuelrondot)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent operators use this skill to create, render, and publish short-form videos, images, and clips through the StoryShort API. It supports option discovery, credit estimation, asynchronous media polling, and user-confirmed publishing to connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, scripts, media URLs, and the StoryShort API key are sent to StoryShort's API.

Mitigation: Install only when this data sharing is acceptable for the intended workflow, and keep STORYSHORT_API_KEY in the user's environment rather than embedding it in prompts or files.

Risk: Video generation can spend StoryShort credits.

Mitigation: Check account balance and quote estimated credit cost to the user before creating media, especially for expensive video configurations.

Risk: Publish and schedule actions can post to real connected TikTok, YouTube, or Instagram accounts.

Mitigation: Require explicit user approval before publishing or scheduling, and use private or self-only visibility for tests when the platform supports it.

## Reference(s):

- [StoryShort Skill on ClawHub](https://clawhub.ai/samuelrondot/skills/storyshort)
- [StoryShort MCP Documentation](https://storyshort.ai/mcp)
- [StoryShort REST API Documentation](https://storyshort.ai/api-docs)
- [StoryShort Support](https://storyshort.ai/contact)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON API arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STORYSHORT_API_KEY and sends prompts, scripts, media URLs, and publishing requests to StoryShort's API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
