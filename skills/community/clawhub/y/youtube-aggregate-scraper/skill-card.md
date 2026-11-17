## Description:

A bilingual YouTube data assistant that uses MaxHub read-only APIs to retrieve video, channel, search, comment, subtitle, playlist, Shorts, and community-post data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, and analysts use this skill to search YouTube and collect channel, video, comment, caption, playlist, Shorts, and community-post data through MaxHub read-only APIs for competitive research, SEO analysis, and feedback reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a MaxHub API key and sends YouTube data requests to a third-party API provider.

Mitigation: Keep MAXHUB_API_KEY private and scoped, and install only if comfortable using MaxHub as the third-party provider.

Risk: Stream URL and comment-data features may have platform or policy implications depending on use.

Mitigation: Use outputs only for authorized, policy-compliant analysis and review downstream use before acting.

Risk: Third-party API data may be incomplete, cached, or inaccurate.

Mitigation: Treat results as reference data and validate important conclusions against primary sources before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/youtube-aggregate-scraper)
- [MaxHub API Service](https://www.aconfig.cn)
- [Channel Data API](artifact/references/api-channel.md)
- [Search & Comments API](artifact/references/api-search.md)
- [Video Data API](artifact/references/api-video.md)
- [Parameter Mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, bullet points, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese/English responses matching the user's language; API key values should not be emitted.]

## Skill Version(s):

3.6.1 (source: server evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
