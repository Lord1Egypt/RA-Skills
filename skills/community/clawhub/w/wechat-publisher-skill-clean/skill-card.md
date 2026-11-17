## Description:

Automatically collects AI news, formats it as HTML, and creates draft posts in a WeChat Official Account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators of WeChat Official Accounts use this skill to collect AI-news items, generate formatted HTML articles, and create WeChat drafts for review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat Official Account credentials and access tokens can grant draft-publishing access.

Mitigation: Use a test account first, provide secrets through environment variables or protected configuration, avoid command-line secrets and committed JSON files, and rotate secrets after evaluation.

Risk: Generated draft content may include inaccurate, stale, or unsuitable news items.

Mitigation: Review each generated WeChat draft and verify sources before publishing.

Risk: Installation guidance includes privileged or global installation patterns.

Mitigation: Use a least-privilege, pinned installation path and review dependencies before installing.

Risk: The artifact includes fixed author and branding values.

Mitigation: Remove or change fixed author and branding before using the skill for another account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/403914291/skills/wechat-publisher-skill-clean)
- [User guide](artifact/docs/user_guide.md)
- [README](artifact/readme.md)
- [Changelog](artifact/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration]

**Output Format:** [HTML article content, Markdown reports, command-line status messages, and JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates WeChat draft records and local status/report files during execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
