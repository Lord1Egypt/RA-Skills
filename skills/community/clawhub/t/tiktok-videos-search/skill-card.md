## Description:

检索 TikTok 关键词热门视频、公开创作者作品和视频评论，并以结构化 JSON 返回结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External creators, brands, and marketing teams use the skill to explore TikTok trends, review public creator posts, and summarize video comments for content research and competitor monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, but only 20 of 32 components were fully scanned and static tool-misuse analysis was degraded, leaving incomplete coverage.

Mitigation: Review and scan the skill before installation, with particular attention to scripts that were not fully inspected.

Risk: The skill requires a GUAIKEI_API_TOKEN, and API requests may incur usage-based charges.

Mitigation: Keep the token private and use request limits appropriate to the account plan.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/tiktok-videos-search)
- [GuaiKei service](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON result envelope with video, creator-post, or comment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty; omitted fields do not necessarily mean a value is zero or absent. No video detail lookup or download is provided.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
