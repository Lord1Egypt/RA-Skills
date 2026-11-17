## Description:

Helps agents retrieve and summarize public social-media profiles, posts, comments, searches, and trends through ToolRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blakefolgado](https://clawhub.ai/user/blakefolgado)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and researchers use this skill to review public account activity, engagement metrics, comments, and trends across social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handles, URLs, search queries, and returned public social-media data are transmitted through ToolRouter.

Mitigation: Use only when comfortable sharing that information with ToolRouter; avoid sensitive personal-data collection.

Risk: Social-media collection could be misused against private accounts or for harassment and doxxing.

Mitigation: Restrict requests to public content and comply with platform terms; do not target private accounts or use the results for harassment or doxxing.

Risk: The optional npx connector can introduce package supply-chain risk.

Mitigation: Review or pin the MCP package before using the npx connector.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/blakefolgado/skills/social-media-scraper)
- [ToolRouter quickstart](https://toolrouter.com/docs/markdown/quickstart)
- [ToolRouter social-media content](https://toolrouter.com/tools/social-media-content)
- [ToolRouter social profiles](https://toolrouter.com/tools/social-profiles)
- [ToolRouter social-media search](https://toolrouter.com/tools/social-media-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown summaries and tables of public social-media results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post dates, captions, URLs, and engagement counts; availability depends on public platform coverage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
