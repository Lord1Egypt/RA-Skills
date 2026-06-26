## Description: <br>
Publishes Markdown content to WeChat Official Accounts with draft management, themes, image handling, and cover image support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and automation agents use this skill to create WeChat Official Account drafts, manage accounts and themes, upload local article images, and publish Markdown articles after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may publish public WeChat posts before the user reviews the rendered article. <br>
Mitigation: Default to draft creation, report title, theme, cover and image handling, and require explicit user confirmation before publish or delete actions. <br>
Risk: WeChat AppSecret exposure could occur through chat logs, shell history, process lists, CI logs, or local configuration backups. <br>
Mitigation: Prefer environment variables, avoid command-line secrets, keep credentials out of logs, protect the local config directory, and reset the AppSecret if exposure is suspected. <br>
Risk: Remote themes can send article content, titles, or image URLs to a third-party endpoint. <br>
Mitigation: Use built-in or local themes by default and enable remote themes only after the user explicitly trusts the endpoint. <br>
Risk: The skill delegates execution and credential storage to the pinned npm package. <br>
Mitigation: Install only the exact pinned package version, audit the referenced upstream files before real credentials are added, and run first with a test or least-privileged account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sipingme/wechat-md-publisher-skill) <br>
- [wechat-md-publisher repository](https://github.com/sipingme/wechat-md-publisher) <br>
- [CLI entry audit reference](https://github.com/sipingme/wechat-md-publisher/blob/main/src/index.ts) <br>
- [Credential storage audit reference](https://github.com/sipingme/wechat-md-publisher/blob/main/src/services/account.ts) <br>
- [quick-start.md](references/quick-start.md) <br>
- [ip-whitelist-guide.md](references/ip-whitelist-guide.md) <br>
- [themes.md](references/themes.md) <br>
- [WeChat Official Account getting started](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and WeChat publishing workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown files, WeChat drafts, published articles, uploaded media, account configuration, and theme or wrapper settings when the user authorizes those actions.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence; artifact frontmatter reports 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
