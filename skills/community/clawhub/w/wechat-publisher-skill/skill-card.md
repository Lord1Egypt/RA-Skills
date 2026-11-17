## Description:

Automatically collects AI news, generates HTML newsletter content, and creates draft posts for WeChat official accounts with configurable templates and scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WeChat official account operators use this skill to collect AI news, format it as HTML newsletter content, and create scheduled WeChat drafts for editorial review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat AppSecret values and access tokens can be exposed if stored in shared configuration/cache files or passed on command lines.

Mitigation: Prefer environment variables or locked-down local config files, restrict permissions on config/cache paths, avoid command-line secrets, and rotate credentials if example patterns were copied.

Risk: Install guidance includes privileged shell and npm commands that can execute installers with elevated permissions.

Mitigation: Review installer sources and commands before privileged execution, use least-privilege installation where possible, and avoid curl-to-sudo setup paths.

Risk: Automated draft creation can publish incorrect, stale, duplicated, or insufficiently sourced news if the draft is not reviewed.

Mitigation: Treat generated WeChat drafts as review-required output and verify story accuracy, source links, deduplication, and formatting before publication.

Risk: The artifact includes fixed author/footer branding and paid trial or activation flows that may not match the installing account's needs.

Mitigation: Replace hard-coded branding, contact details, and licensing prompts before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/403914291/skills/wechat-publisher-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/403914291)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [Skill overview](artifact/skill.md)
- [Installation guide](artifact/docs/install-guide.md)
- [User guide](artifact/docs/user_guide.md)
- [Publishing rules](artifact/docs/publish-rules.md)
- [Template documentation](artifact/docs/templates.md)
- [Troubleshooting guide](artifact/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated HTML content, and WeChat draft/status identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates WeChat official account drafts through configured API credentials and may write local status, token cache, usage, log, and result files.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
