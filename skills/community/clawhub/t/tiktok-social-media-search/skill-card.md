## Description:

Searches public TikTok videos, creator posts, and comments to support social media analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, researchers, and content teams use this skill to find public TikTok videos, review creator activity, and summarize audience comments for market and content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and TikTok search terms or target URLs are sent to Guaikei.

Mitigation: Confirm the third-party data transfer is acceptable before using the skill; keep the API token confidential.

Risk: Fetched public results, including usernames and comment text, are saved in system temporary logs.

Mitigation: Apply your retention policy to those logs and delete them when no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-social-media-search)
- [Skill parameter reference](references/options.md)
- [Guaikei API and token information](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Markdown summaries informed by structured JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public video, creator, and comment data; requires a Guaikei API token.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
