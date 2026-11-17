## Description:

Wechat Mp Auto automates WeChat Official Account article workflows from topic research and Markdown writing through image handling, content review, WeChat-ready HTML conversion, and draft or publication-related account operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzhaojin](https://clawhub.ai/user/wzhaojin)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators use this skill to prepare WeChat Official Account posts, research topics, convert Markdown into themed HTML, upload media, review content, and create drafts for account publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a real WeChat account by uploading media, creating drafts, publishing content, reading account data, or using messaging and analytics capabilities.

Mitigation: Use a narrowly scoped account and API keys, review generated drafts before release, and enable only the WeChat permissions needed for the intended workflow.

Risk: Credential handling relies on local files and environment variables.

Mitigation: Store credentials in restricted local files or managed secrets, limit file permissions, and rotate WeChat and third-party API keys regularly.

Risk: Research, review, and image workflows can fetch remote URLs or send content to third-party services.

Mitigation: Avoid untrusted image URLs, use approved research and image providers, and confirm that article content is appropriate to share with configured third-party services.

Risk: Drafts may include a default source URL or attribution that does not match the publisher's intended article source.

Mitigation: Review and change the source URL before creating or publishing drafts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzhaojin/skills/wechat-mp-auto)
- [Publisher profile](https://clawhub.ai/user/wzhaojin)
- [Homepage URL from artifact metadata](https://github.com/wzhaojin/wechat-mp-auto)
- [Pexels API](https://www.pexels.com/api/)
- [Unsplash Developers](https://unsplash.com/developers)
- [Tavily](https://tavily.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, WeChat-ready HTML, JSON-like tool results, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration and cache paths plus external API credentials for WeChat, optional image providers, and optional research or review services.]

## Skill Version(s):

0.1.2 (source: evidence.json release.version, artifact/CHANGELOG.md, artifact/pyproject.toml, artifact/metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
