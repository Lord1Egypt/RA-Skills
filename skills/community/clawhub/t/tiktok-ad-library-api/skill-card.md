## Description:

Search ads running on TikTok by keyword and/or industry, pull the top-performing ads with a performance highlight, and open one ad in full with its objective, engagement, the countries it ran in, its landing page and a playable video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, paid-social, and competitive research teams use this skill to search TikTok ads, inspect top-performing creative, and retrieve detailed ad metadata through Scavio's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends TikTok ad search terms, industries, countries, objectives, or ad IDs to Scavio as a third-party service.

Mitigation: Review the query terms and ad identifiers before use and install the skill only when Scavio is an approved service for the intended ad research workflow.

Risk: SCAVIO_API_KEY is required for API calls and could expose account access if committed or shared.

Mitigation: Store SCAVIO_API_KEY in an environment variable or secret store and keep it out of source control and logs.

Risk: Each API call consumes credits and exhausted balances can interrupt the workflow.

Mitigation: Confirm credit availability before large searches and handle 402 billing responses without changing the key.

Risk: Playable video and cover URLs returned by the API have short expirations.

Mitigation: Fetch needed media promptly and do not treat returned media URLs as durable references.

## Reference(s):

- [Scavio TikTok Ad Library API documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-ad-library-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-ad-library-api)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/tiktok-ad-library-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and curl examples; API responses use structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY. Each TikTok Ads endpoint uses 1 credit, and playable video or cover URLs may expire quickly.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
