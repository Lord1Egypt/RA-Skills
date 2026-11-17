## Description:

TikTok News Briefing searches public TikTok videos by keyword, retrieves creators’ public posts and video comments, and returns structured results for trend and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok creators, marketing teams, researchers, and AI agents can use the skill to search public videos, review a creator’s public posts, or collect comments for trend, competitor, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and TikTok links are sent to the GUAIKEI service, and the service itself was not audited.

Mitigation: Use a dedicated token, avoid confidential query terms, and confirm the provider's charges and data handling before use.

Risk: Optional file logging retains queries and results locally.

Mitigation: Enable logging only when retention is needed and protect the resulting files.

Risk: Public comments and creator details may contain personal information.

Mitigation: Review applicable permissions and redact usernames or other personal details before external publication or commercial use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-news-brief)
- [GUAIKEI service and token access](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [Release changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON response envelope containing search results, creator posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a GUAIKEI_API_TOKEN; result fields depend on the selected operation.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
