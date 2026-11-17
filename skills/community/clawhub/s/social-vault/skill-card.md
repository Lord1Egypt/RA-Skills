## Description:

SocialVault helps agents manage social platform account credentials by importing sessions, storing them encrypted, checking login health, and refreshing sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2019-02-18](https://clawhub.ai/user/2019-02-18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use SocialVault to add, verify, list, update, and remove social platform account sessions for agent workflows. It supports built-in adapters for Xiaohongshu, Bilibili, Zhihu, and Baidu Tieba, plus custom adapter creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live social-platform session cookies that may authorize account actions.

Mitigation: Use a dedicated, low-risk account where possible and only provide credentials for accounts the user intends the agent to operate.

Risk: Cookie paste and command-line workflows can expose secrets if users paste credentials into general chat, shell history, or logs.

Mitigation: Paste credentials only into the skill's requested flow, avoid unrelated terminals or chats, and verify that displayed values remain redacted.

Risk: Scheduled health checks and refresh tasks create persistent account-use authority.

Mitigation: Review the scheduled tasks before enabling them and disable or remove managed accounts when ongoing access is no longer needed.

Risk: Long-lived or cross-service cookies, including BDUSS, can increase account impact if mishandled.

Mitigation: Prefer narrowly scoped or short-lived sessions when available and rotate or revoke cookies after sensitive work.

## Reference(s):

- [ClawHub SocialVault release page](https://clawhub.ai/2019-02-18/skills/social-vault)
- [README.md](README.md)
- [clawhub.json](clawhub.json)
- [Platform adapter specification](adapters/_spec.md)
- [Bilibili cookie export guide](guides/cookie-export-bilibili.md)
- [Xiaohongshu cookie export guide](guides/cookie-export-xiaohongshu.md)
- [Zhihu cookie export guide](guides/cookie-export-zhihu.md)
- [Tieba cookie export guide](guides/cookie-export-tieba.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, tables, prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts full credential values in user-facing output and persists runtime credential material in local encrypted vault files.]

## Skill Version(s):

0.1.7 (source: server release evidence; artifact SKILL.md, package.json, and clawhub.json show 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
