## Description:

Uses a local WeChat Official Accounts crawler to identify an account from an article link and batch-fetch recent posts as Markdown, HTML, and articles.json for corpus building, style analysis, fact checking, and archiving.

This skill is for research and development only.

## Publisher:

[dazhuangjammy](https://clawhub.ai/user/dazhuangjammy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to run a local CLI workflow that logs into WeChat Official Accounts, fetches recent articles for a target public account, and stores the results for downstream analysis or local archiving. It is framed by the source documentation as learning, research, and local automation use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires local shell, network, browser-profile, and WeChat session access.

Mitigation: Install it only in an environment where that access is acceptable, and use a dedicated low-privilege WeChat Official Accounts account.

Risk: Login state, QR artifacts, cookies, or browser profile data could expose account access if shared or synced.

Mitigation: Keep the skill directory out of shared or synced folders, do not share QR or login artifacts, and clear local login state before handing the project to someone else.

Risk: Dependencies, browser automation, and URL-handling paths need review before installation.

Mitigation: Pin and review dependencies before first run, and review proposed shell commands before executing them.

Risk: The clear-login path may delete unintended data when WECHAT_FETCHER_PROFILE_DIR or WECHAT_FETCHER_LOGIN_ARTIFACTS_DIR point to custom locations.

Mitigation: Avoid clear-login when those environment variables are set unless the target paths have been checked.

## Reference(s):

- [Skill README](artifact/README.md)
- [公众号抓取龙虾](artifact/references/抓取器说明.md)
- [ClawHub skill page](https://clawhub.ai/dazhuangjammy/skills/wechat-articles-crawler)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; crawler output includes Markdown, HTML, and articles.json files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime workflow can return JSON status and result summaries, including account name, downloaded count, failed count, output directory, and index file path.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
