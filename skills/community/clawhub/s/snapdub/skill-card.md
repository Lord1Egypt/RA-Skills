## Description:

Turn a long video (stream, podcast, interview, gameplay VOD) into short vertical clips with captions using SnapDub, then pick the best ones, schedule them to TikTok, YouTube or Instagram, and find live paid clipping campaigns to submit them to. Use when someone wants clips from a YouTube, Twitch, Kick, Rumble or Zoom link, wants to run a clipping page or clip for Whop/Content Rewards campaigns, or asks which of their SnapDub clips to post first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aheront](https://clawhub.ai/user/aheront)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn eligible long-form video into short vertical clips, review and rank the clips, and find paid clipping campaigns. It can also schedule a selected clip to a connected social account after the user explicitly approves it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video content is processed by SnapDub, and its implementation and data retention were not verified.

Mitigation: Send only content the user is comfortable sharing with SnapDub; check the service's data-handling terms when needed.

Risk: The REST route uses a bearer API key.

Mitigation: Protect SNAPDUB_API_KEY and avoid exposing it in conversation or generated output.

Risk: Video processing and paid clipping campaigns can involve credit costs and campaign-specific rules.

Mitigation: Check available credits and estimate the cost before starting work; review campaign requirements before recommending a submission.

Risk: Scheduling a clip creates an external social media action.

Mitigation: Get the user's explicit approval for the specific clip and destination before scheduling it.

## Reference(s):

- [SnapDub MCP server](https://snapdub.ai/mcp-server)
- [SnapDub API documentation](https://snapdub.ai/developers/api)
- [SnapDub REST API reference](artifact/references/rest-api.md)
- [SnapDub OpenAPI specification](https://snapdub.ai/api/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Markdown summaries of clip details, campaign information, and scheduling results, with structured data returned by SnapDub]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clip titles, descriptions, hashtags, ranking scores, and expiring download links; scheduling requires explicit user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
