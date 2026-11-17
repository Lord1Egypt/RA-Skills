## Description:

Automates TikTok Shop operations across product management, order handling, analytics, video publishing, and Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External shop operators and developers use this skill to configure and run TikTok Shop workflows for listings, inventory, order fulfillment, sales reporting, and Feishu integrations.

### Deployment Geography for Use:

United States, United Kingdom, Southeast Asia, and Indonesia

## Known Risks and Mitigations:

Risk: The skill can affect live commerce workflows such as product publishing, inventory updates, order fulfillment, and refunds.

Mitigation: Use mock or sandbox data first, and require dry-run or explicit confirmation before enabling live actions or automatic modes.

Risk: The skill handles TikTok cookies, API secrets, and Feishu webhook or app tokens.

Mitigation: Store secrets in a managed secret store or locked-down credentials file, and rotate any TikTok or Feishu credentials already saved by this version.

Risk: Order synchronization can export customer names and emails to Feishu or other targets.

Mitigation: Minimize exported customer fields, restrict destination access, and document personal-data handling before syncing real orders.

Risk: Feishu synchronization and notifications may run without enough per-command intent checks.

Mitigation: Keep Feishu sync opt-in per command and verify the destination app, table, and webhook before sending records or notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/tiktok-shop-automation)
- [ClawHub TikTok Shop documentation](https://docs.clawhub.com/tiktok-shop)
- [TikTok Shop Partner documentation](https://partner.tiktokshop.com/)
- [TikTok Marketing API documentation](https://business-api.tiktok.com/)
- [Feishu Open Platform documentation](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with CLI commands, configuration snippets, and command-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local TikTok Shop and Feishu configuration or credential files when executed.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact clawhub.json, artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
