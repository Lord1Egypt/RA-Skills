## Description:

微博转文字 / 微博视频文案提取 / 微博 API：一条微博链接读成文字——正文、作者和时间、转发评论点赞数、每张图的描述和图上的字、视频口播逐字稿和画面文字、话题、前几条热评、逐字核对的要点。用户发来 weibo.com、m.weibo.cn 链接，要提取微博内容、扒视频文案、整理热评、做舆情或竞品资料时使用。不用申请微博开放平台，不用微博账号或 Cookie。图文 1 积分起，1 分钟视频 2 积分；注册送 10 积分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can turn public Weibo post links into usable text for content review, research, or reference work. The skill extracts available post details, image and video text, visible top comments, and key points with supporting quotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The complete supplied link or share text is sent to LinkDigest for processing; provider retention practices and extraction accuracy have not been independently verified.

Mitigation: Use the skill only for content you are comfortable sending to LinkDigest, review the provider's privacy terms, and check returned quotations against the source.

Risk: Full extraction and optional features can consume credits.

Mitigation: Set --max-credits to cap spending for a request and choose only the output depth you need.

## Reference(s):

- [LinkDigest Weibo API](https://linkdigest.dev/zh/weibo-api?ref=skill-weibo-to-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown by default, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes available post details, extracted image or video text, visible comments, key points with supporting quotations, and coverage notes; results depend on public access and media content. Some options use credits.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
