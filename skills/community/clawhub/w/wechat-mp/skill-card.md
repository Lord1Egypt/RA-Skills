## Description: <br>
Wechat MP Article Stats Comments Suite helps operators create WeChat public-account drafts, style and cover articles, manage drafts, comments, and users, and retrieve account statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WeChat public-account operators and automation agents use this skill to prepare and submit article drafts, synchronize drafts across configured accounts, moderate comments, manage follower blacklist operations, and query article or user statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform account-changing actions such as publishing drafts, deleting drafts or comments, cloning drafts, and changing blacklist status. <br>
Mitigation: Review each JSON request body, selected subcommand, account name, media ID, comment ID, and openid list before execution, especially when multiple accounts are configured. <br>
Risk: WECHAT_MP_APP_SECRET, WECHAT_MP_ACCOUNTS, and WECHAT_MP_COOKIE can expose account credentials or authenticated sessions. <br>
Mitigation: Keep these values out of shared environments, logs, screenshots, and repositories; prefer isolated shells and per-command configuration for sensitive operations. <br>
Risk: Cookie-backed URL fetching can send an authenticated cookie to requested article, style, or cover URLs. <br>
Mitigation: Avoid setting WECHAT_MP_COOKIE globally and only fetch trusted URLs when any cookie is present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/wechat-mp) <br>
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/subscription/api/) <br>
- [WeChat freepublish submit API](https://developers.weixin.qq.com/doc/subscription/api/public/api_freepublish_submit.html) <br>
- [WeChat batch unblacklist API](https://developers.weixin.qq.com/doc/subscription/api/usermanage/userinfo/api_batchunblacklist.html) <br>
- [Related jisu-wechat-article skill](https://clawhub.ai/jisuapi/jisu-wechat-article) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and WeChat MP credentials via WECHAT_MP_APP_ID and WECHAT_MP_APP_SECRET or WECHAT_MP_ACCOUNTS; supported commands can create, publish, delete, clone, moderate, blacklist, and query WeChat public-account resources.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
