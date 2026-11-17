## Description:

Publishes Markdown articles to WeChat Official Accounts, with draft management, themes, image handling, and cover image support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to create drafts, publish Markdown articles, manage WeChat Official Account content, and apply WeChat-oriented article themes from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a WeChat public account and local article files, and misuse could affect published account content.

Mitigation: Use a test or least-privileged account first and install only after reviewing the security guidance.

Risk: AppSecret handling can expose production credentials through shell history, process lists, logs, or local configuration.

Mitigation: Prefer environment variables, keep AppSecret out of command arguments and logs, protect the local configuration directory, and reset credentials if exposure is suspected.

Risk: Automated publish flows can make incorrect or noncompliant content immediately visible to followers.

Mitigation: Prefer draft creation with manual review, and require explicit confirmation before publish create or publish submit.

Risk: Remote themes may send article content to a third-party endpoint outside the default WeChat API data boundary.

Mitigation: Use built-in or local themes by default, and enable remote themes only for trusted and reviewed endpoints.

Risk: The skill depends on the underlying wechat-md-publisher npm package for publishing and credential handling.

Mitigation: Audit wechat-md-publisher@1.0.7 before production use and keep the exact version pin unless a newer version is separately reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipingme/skills/wechat-md-publisher-skill)
- [WeChat Publisher project](https://github.com/sipingme/wechat-md-publisher)
- [WeChat Publisher CLI entry audit file](https://github.com/sipingme/wechat-md-publisher/blob/main/src/index.ts)
- [WeChat Publisher credential handling audit file](https://github.com/sipingme/wechat-md-publisher/blob/main/src/services/account.ts)
- [WeChat Publisher API documentation](https://github.com/sipingme/wechat-md-publisher/blob/main/docs/API.md)
- [WeChat Official Account documentation](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [Quick start guide](artifact/references/quick-start.md)
- [IP whitelist guide](artifact/references/ip-whitelist-guide.md)
- [Theme guide](artifact/references/themes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and operational status text from the WeChat publishing CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may create or publish WeChat drafts/articles and may write local account configuration through the underlying CLI.]

## Skill Version(s):

1.0.11 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
