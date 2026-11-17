## Description:

公众号文章写作全流程助手（通用版），支持多账号管理、热门选题推荐、文章创作、可选企业微信文档存档，以及持续风格学习。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophiayuan1984-jpg](https://clawhub.ai/user/sophiayuan1984-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and editorial teams use this skill to manage WeChat public-account writing profiles, generate timely topic options, draft articles in an account-specific style, and optionally archive finished work to WeCom Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account profiles, style notes, active account state, and article indexes may contain sensitive editorial or business information stored in the local workspace.

Mitigation: Review generated reference files before sharing the workspace, and delete or redact profiles, style notes, and article index entries that should not be retained.

Risk: Optional archiving can send completed article content to WeCom Docs.

Mitigation: Only confirm WeCom Docs archiving for content that is approved for that service; otherwise keep the article local.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sophiayuan1984-jpg/skills/wechat-writer-kit)
- [README.md](README.md)
- [通用写作规范](references/writing-rules.md)
- [公众号画像模板](references/profile-template.md)
- [文章存档索引](references/article-index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown conversational guidance and article drafts, with workspace reference files for profiles, active account state, and article index entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use web search for timely topic discovery and may archive completed articles to WeCom Docs only after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
