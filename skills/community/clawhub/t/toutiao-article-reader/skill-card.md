## Description:

使用浏览器自动化阅读今日头条、微信公众号、知乎等平台文章，自动提取标题、作者、发布时间和正文内容，并支持内容清洗和摘要生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[brainpower168](https://clawhub.ai/user/brainpower168)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to read trusted public article URLs from Toutiao, WeChat Official Accounts, Zhihu, Xueqiu, and similar content platforms. It extracts article metadata and body text, cleans the content, generates a concise summary, and can export results for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Chromium without its sandbox while visiting user-provided article URLs.

Mitigation: Run the skill in an isolated environment and only open trusted public article URLs.

Risk: Article URLs and fetched article content are cached locally.

Mitigation: Avoid private, internal, signed, token-bearing, localhost, or metadata-service URLs, and clear the cache when stored content should not persist.

Risk: Browser automation against arbitrary pages can expose the runtime to untrusted web content.

Mitigation: Review URLs before execution and keep usage limited to public content platforms that are appropriate for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brainpower168/skills/toutiao-article-reader)
- [Publisher profile](https://clawhub.ai/user/brainpower168)
- [Artifact README](README.md)
- [Artifact skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands]

**Output Format:** [Console text or structured JSON, with optional Markdown, TXT, JSON, or HTML export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include title, author, publish time, platform, original URL, extracted content, word count, estimated reading time, cache status, and heuristic summary fields.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md metadata, package.json; artifact CHANGELOG also contains a later v1.1.0 entry for review)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
