## Description:

Give OpenClaw the ability to access social media content. It can search across TikTok, Instagram, and YouTube for videos, watch TikTok/Reels/YouTube, retrieve metadata, get creator profiles, and extract insights from video content across platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veedcrawl](https://clawhub.ai/user/veedcrawl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Veed Crawl to search public social video content, inspect creator profiles, retrieve metadata and transcripts, and extract structured insights for research notes, creator briefs, comparisons, and evidence tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional VEEDCRAWL_BASE_URL setting can send the Veedcrawl API key to an arbitrary server.

Mitigation: Leave VEEDCRAWL_BASE_URL unset unless the endpoint is controlled and trusted; prefer the default https://api.veedcrawl.com and rotate the API key if it may have been sent to an untrusted URL.

## Reference(s):

- [Veedcrawl documentation](https://docs.veedcrawl.com)
- [Veedcrawl OpenAPI specification](https://veedcrawl.com/openapi.json)
- [Veed Crawl on ClawHub](https://clawhub.ai/veedcrawl/skills/veedcrawl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash/curl command examples, plus structured tables or JSON for comparisons when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and VEEDCRAWL_API_KEY. VEEDCRAWL_BASE_URL is optional and should normally remain unset.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
