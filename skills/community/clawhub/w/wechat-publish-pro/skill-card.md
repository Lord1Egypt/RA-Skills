## Description:

Converts Markdown into WeChat Official Account styled HTML and publishes articles to WeChat draft storage with theme, image, and account-management support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuesf](https://clawhub.ai/user/yuesf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agents use this skill to prepare Markdown articles for WeChat Official Accounts, generate styled HTML, manage publishing credentials, upload images, test connectivity, and create WeChat draft articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution paths may allow unintended command execution during publishing.

Mitigation: Remove eval from scripts/publish.sh and pass validated command arguments directly before installing or running the skill.

Risk: Loading ~/.openclaw/.env as shell code can execute more than the required WeChat credential variables.

Mitigation: Load only the required WECHAT_APP_ID and WECHAT_APP_SECRET values with a safe parser instead of sourcing the file.

Risk: WeChat AppSecret handling may expose publishing credentials if stored or shared without access controls.

Mitigation: Store AppSecret with restrictive file permissions or in a secret store, and avoid using the skill with sensitive drafts until credential handling is reviewed.

Risk: Remote image or CSS fetching can pull untrusted network content into the publishing flow.

Mitigation: Restrict remote fetches to trusted sources and review article assets before uploading or publishing.

Risk: Automated publish actions can create WeChat drafts without an explicit operator checkpoint.

Mitigation: Require confirmation before publishing and pin the installation source for repeatable releases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuesf/skills/wechat-publish-pro)
- [WeChat Developers Platform](https://developers.weixin.qq.com/)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, generated HTML files, and WeChat draft or media identifiers when publishing succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeChat AppID and AppSecret credentials and a WeChat Official Account IP allowlist entry for publishing operations.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
