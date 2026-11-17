## Description:

公众号运营：发文到草稿、样式与封面、评论与用户管理、数据统计等。当用户说：把这篇 Markdown 发到公众号草稿、看下昨天阅读量统计，或类似公众号后台操作时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing WeChat Official Accounts use this skill to prepare article drafts, manage draft publication, moderate comments, administer users, and retrieve account statistics through the WeChat MP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses powerful WeChat account credentials and can perform publishing, deletion, blacklist, comment moderation, and multi-account clone actions.

Mitigation: Run only in an isolated environment with narrowly scoped credentials and require human review before account-changing actions.

Risk: WECHAT_MP_COOKIE can be sent when fetching user-provided html_url, cover_url, style_url, or page-derived og:image sources.

Mitigation: Avoid setting WECHAT_MP_COOKIE globally and process only trusted URLs when cookie-based fetching is needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jisuapi/skills/wechat-mp)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/subscription/api/)
- [WeChat freepublish submit documentation](https://developers.weixin.qq.com/doc/subscription/api/public/api_freepublish_submit.html)
- [WeChat batch unblacklist documentation](https://developers.weixin.qq.com/doc/subscription/api/usermanage/userinfo/api_batchunblacklist.html)
- [Related ClawHub skill: jisu-wechat-article](https://clawhub.ai/jisuapi/jisu-wechat-article)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request examples; scripts return JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and WeChat MP credentials in environment variables.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
