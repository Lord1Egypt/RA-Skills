## Description:

输入研究主题，自动采集 Reddit 讨论，提炼爆款角度，产出 X 推文、小红书笔记、公众号文章三平台成品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbule](https://clawhub.ai/user/wbule)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and research-focused agents use this skill to turn Reddit discussions on a topic into Chinese-language content angles and finished drafts for X, Xiaohongshu, and WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reddit posts and comments can influence generated drafts, including through misleading, biased, or adversarial source content.

Mitigation: Review generated content and source attributions before publishing or reusing the drafts.

Risk: The workflow contacts Reddit and may use optional Reddit API credentials from environment variables.

Mitigation: Install and run it only when Reddit network access is expected, and keep Reddit credentials in environment variables rather than generated files.

Risk: The skill depends on Python package installation for requests.

Mitigation: Use a pinned virtual environment for dependencies before running the collection scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wbule/skills/reddit-topic-insight)
- [10 article types](reference/article-types.md)
- [X tweet template](reference/x-tweet-template.md)
- [Xiaohongshu note template](reference/xiaohongshu-template.md)
- [WeChat article template](reference/wechat-template.md)
- [Reddit search JSON endpoint](https://www.reddit.com/search.json)
- [Reddit OAuth token endpoint](https://www.reddit.com/api/v1/access_token)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local run artifacts under runs/<slug>/, including keywords.json, posts_raw.json, posts_detail.json, angles.json, piece Markdown files, and merged content.md.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
