## Description:

按主题生成小红书或抖音赛道日报、热门内容对比和贴合用户口吻的发布草稿，并通过邮件与分享链接交付；不登录平台或代为发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和运营者可订阅小红书或抖音主题日报、比较热门笔记并生成符合个人口吻的草稿，也可一次性分析主题或检查自己的笔记。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API destination could receive the LinkDigest API key and submitted data.

Mitigation: Keep LINKDIGEST_BASE_URL pointed at a destination you trust, and never paste the API key into chat or submitted content.

Risk: The security review says disclosure is unclear about sending writing samples and account-post URLs to LinkDigest.

Mitigation: Review any --voice samples and checkup URLs before sending them; submit only material you are comfortable sharing with LinkDigest.

Risk: The security review is incomplete, so its assessment may not cover every component or instruction path.

Mitigation: Review the skill and its destination before providing credentials or personal content.

## Reference(s):

- [LinkDigest 文档](https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-daily-draft)
- [LinkDigest 价格](https://linkdigest.dev/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Daily brief and publish-ready draft text, with JSON status and metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked post metrics, a comparison, draft titles and body, hashtags, cover text, and a share link.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
