## Description:

小红书 AI 宣传图、图文笔记和视频发布技能 - 根据用户提示词生成单张或多张宣传图，并支持将用户提供的本地 MP4 视频发布为视频笔记；仅在用户明确要求发布到小红书时才执行发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to turn a short brief into Xiaohongshu promotional images, carousel-note copy, tags, and publish-ready files. When explicitly requested, the skill can publish image notes or a user-supplied local MP4 video to Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish immediately using a full Xiaohongshu session cookie.

Mitigation: Use --dry-run first, review titles, descriptions, images, and videos before invoking publish_xhs.py, and prefer a dedicated low-risk Xiaohongshu account.

Risk: A full Xiaohongshu session cookie gives account-level access if exposed.

Mitigation: Store XHS_COOKIE only in a controlled environment, never commit it to source control, rotate it regularly, and log out of the browser session when access is no longer needed.

Risk: Prompts, generated content, and API credentials may be sent to OpenAI or Volcengine Ark services, and Ark can use a caller-selected base URL.

Mitigation: Avoid sensitive or confidential content in prompts, confirm the selected provider's data handling terms, avoid --ark-base-url unless the endpoint is fully trusted, and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youteacher/skills/xiaohongshu-ai)
- [Xiaohongshu](https://www.xiaohongshu.com)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include manifest.json, PNG images, and optional publish result JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image notes use cover.png and optional card_*.png files up to 9 images; video publishing accepts one local MP4 with an optional cover image.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
