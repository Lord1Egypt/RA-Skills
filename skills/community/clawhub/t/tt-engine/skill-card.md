## Description:

TikTok视频分析数据源（只读）：关键词搜视频、博主作品、视频评论，输出 JSON，不登录不发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and researchers use the skill to retrieve public TikTok videos, creator posts, and comments for topic research, competitor reviews, and audience sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence; 12 of 34 components received only partial inspection, including several scripts.

Mitigation: If the coverage gap matters, wait for a more complete scan before installing.

Risk: Search keywords and TikTok links are sent to the Guaikei service to retrieve data.

Mitigation: Submit only public TikTok queries and links you are comfortable sharing with the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-engine)
- [Guaikei service](https://www.guaikei.com)
- [Options and output fields](artifact/references/options.md)
- [FAQ and configuration](artifact/references/faq.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Structured data]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results contain public TikTok video, creator-post, or comment data; an empty result is possible.]

## Skill Version(s):

1.1.3 (source: frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
