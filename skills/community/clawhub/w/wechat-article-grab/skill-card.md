## Description:

抓取微信公众号文章、搜索公众号、文章列表、爆款查询与分析。触发场景：mp.weixin.qq.com 链接、微信公众号文章、公众号文章分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[one2agi](https://clawhub.ai/user/one2agi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to fetch WeChat Official Account article text, search accounts and article lists, compare accounts or URLs, and inspect trending article metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require sensitive WeChat session cookies for fallback paths.

Mitigation: Prefer the mptext API path with a fresh, low-privilege, short-lived API key; avoid pasting full browser cookie exports into an agent or storing them in the skill directory unless the session exposure is acceptable.

Risk: A packaged API key is present in the artifact configuration file.

Mitigation: Remove the packaged key before use and replace it with a user-controlled short-lived key.

Risk: Unsafe network handling could expose credentials or reach unintended hosts.

Mitigation: Restrict fetches to trusted WeChat-related hosts and avoid the trends path until TLS verification is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/one2agi/skills/wechat-article-grab)
- [Environment guide](env-guide.md)
- [Priority and fallback reference](references/priority.md)
- [mptext API dashboard](https://wechat.faiz-world.com/dashboard/api)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [Sogou WeChat search](https://weixin.sogou.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown command output, with article content, account metadata, article lists, comparisons, and trend summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use API keys or WeChat cookies and may return partial article text when upstream anti-crawling or validation limits extraction.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
