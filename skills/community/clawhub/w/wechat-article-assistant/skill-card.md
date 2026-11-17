## Description:

微信公众号文章同步与详情抓取助手，支持公众号后台登录、账号管理、文章同步、文章详情和图片下载、代理配置以及 Markdown 汇总报告导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryczq](https://clawhub.ai/user/henryczq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage WeChat public accounts, synchronize article lists, fetch article details and images, and export recent-article Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores WeChat MP login session data and fetched article content in local persistent storage.

Mitigation: Keep the configured data directory private, restrict filesystem access, and clear or rotate login sessions when no longer needed.

Risk: Diagnostics or login-status output may expose sensitive session details if copied into shared logs or tickets.

Mitigation: Redact doctor, login-info, and debug JSON before sharing, especially cookie, token, QR-code, target, and account fields.

Risk: User-configured gateway or proxy URLs can relay authenticated WeChat requests through third-party infrastructure.

Mitigation: Use only trusted private gateways for authenticated sync and article fetching; avoid public or untrusted proxy endpoints.

Risk: QR-code and sync-status notifications can reveal login flow or account activity to the wrong recipient.

Mitigation: Disable notifications unless needed, or send them only to a private trusted channel and target.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henryczq/skills/wechat-article-assistant)
- [henryczq publisher profile](https://clawhub.ai/user/henryczq)
- [operations.md](references/operations.md)
- [interface-reference.md](references/interface-reference.md)
- [sqlite-schema.md](references/sqlite-schema.md)
- [design.md](references/design.md)
- [account-classification-summary-design.md](references/account-classification-summary-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON command output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite state, downloaded article images, article Markdown files, reports, QR-code images, and logs in the configured data directory.]

## Skill Version(s):

0.3.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
