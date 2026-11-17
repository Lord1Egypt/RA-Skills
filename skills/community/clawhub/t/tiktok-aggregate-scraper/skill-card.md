## Description:

Helps agents query TikTok video, user, search, ads, creator, shop, and analytics data through MaxHub APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent retrieve and summarize TikTok public data, creator signals, search results, ads, shop/product information, comments, and analytics through the MaxHub API. It is intended for data analysis workflows that require a configured MaxHub API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some flows can send TikTok session cookies and possible login passwords to the third-party MaxHub/aconfig.cn API.

Mitigation: Use the skill only if you trust MaxHub/aconfig.cn, avoid primary TikTok accounts, do not provide TikTok passwords, and revoke or rotate TikTok cookies after use.

Risk: TikTok session cookies are full account credentials when provided to third-party services.

Mitigation: Use a separate test account for cookie-required requests and remove cookies from prompts, samples, and client-side contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/tiktok-aggregate-scraper)
- [Publisher profile](https://clawhub.ai/user/new-ironman)
- [MaxHub API service](https://www.aconfig.cn)
- [Video & Content API](references/api-video.md)
- [User Data API](references/api-user.md)
- [Search API](references/api-search.md)
- [Ads & Analytics API](references/api-ads-analytics.md)
- [Parameter Mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, concise summaries, and inline shell commands or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; API responses are used to produce user-facing summaries and analysis.]

## Skill Version(s):

3.7.1 (source: evidence.json release.version, parsed metadata.version, and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
