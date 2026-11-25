## Description:

TikTok 公开视频数据只读技能：搜索视频、获取博主作品和视频评论，并以结构化 JSON 返回，不登录或发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External content strategists and researchers can review public TikTok search results, creator posts, and video comments for topic research, competitor monitoring, KOL screening, and comment sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security inspection was incomplete: 22 of 34 components were fully inspected and 12 were marked partial, leaving some behavior uncertain.

Mitigation: Review the skill's required access and relevant source files before installation.

Risk: Search terms or TikTok links are sent to guaikei.com, and requests require an API token.

Mitigation: Send only queries you intend to share with the service and keep GUAIKEI_API_TOKEN private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-voc)
- [API service and token information](https://www.guaikei.com)
- [Parameter and output reference](references/options.md)
- [FAQ and environment setup](references/faq.md)

## Skill Output:

**Output Type(s):** [Structured JSON]

**Output Format:** [JSON result envelopes containing video, creator-post, or comment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields depend on the selected command; request limits depend on the API plan. Results are not saved by default.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
