## Description:

Retrieves public TikTok video search results, creator posts, and video comments as structured JSON for trend and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External marketers, researchers, and social media teams use this skill to retrieve public TikTok videos, creator posts, and comments for market research, content discovery, competitor monitoring, and audience sentiment summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests share search terms or TikTok targets with Guaikei and may incur charges; provider collection, retention, and billing practices were not independently verified.

Mitigation: Use a dedicated API token, consider charges, and avoid sending sensitive search terms or targets until the provider’s terms are reviewed.

Risk: When optional logging is enabled, queries and results are retained in local temporary-directory logs.

Mitigation: Keep logging disabled unless needed, and review or remove local logs when finished.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-market-insight)
- [Guaikei service and token access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON containing TikTok video, creator, or comment data, with concise text summaries when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are returned as JSON; successful searches, post lookups, and comment lookups return arrays.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, changelog dated 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
