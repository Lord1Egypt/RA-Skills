## Description:

Reads one or more WeChat public account article links from mp.weixin.qq.com, extracts cleaned text and optional image links, summarizes the articles in Chinese, and writes structured Markdown notes or daily digests to a user-chosen directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juneliu1999](https://clawhub.ai/user/juneliu1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn WeChat public account article URLs into Chinese summaries, single-article notes, or multi-article daily digest Markdown files for reading, archiving, or further editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL validation may allow fetching non-WeChat or internal URLs.

Mitigation: Validate the parsed URL scheme and hostname before fetching, and avoid running the skill on networks that can reach private services until that validation is fixed.

Risk: Article text is sent through the configured summarize tool.

Mitigation: Use the skill only for content that may be shared with the configured summarization provider, and review provider settings before processing sensitive articles.

Risk: Raw article files and generated Markdown are saved locally.

Mitigation: Choose an appropriate output directory, review generated files before sharing, and delete raw working files when they are no longer needed.

Risk: The workflow can load environment variables from an env file.

Mitigation: Use only trusted env files and avoid passing env files supplied by untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juneliu1999/skills/wechat-article-summarize)
- [ClawHub publisher profile](https://clawhub.ai/user/juneliu1999)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with Chinese summaries, article metadata, mindmap-style sections, and optional image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-article outputs are named YYYYMMDD-title.md; batch outputs are named YYYYMMDD-count-label.md.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
