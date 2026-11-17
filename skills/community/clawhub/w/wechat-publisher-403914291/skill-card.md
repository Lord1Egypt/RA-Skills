## Description:

Automates collection and formatting of AI news into HTML drafts for a WeChat Official Account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account operators use this skill to prepare scheduled AI-news posts, generate WeChat-compatible HTML, and create drafts in a WeChat Official Account for review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe install and credential-handling guidance may expose the WeChat AppSecret or encourage risky setup steps.

Mitigation: Review the skill before installing, avoid the sudo curl pipeline, keep AppSecret values out of command lines and documentation, and store credentials with owner-only permissions or a secret manager.

Risk: The publishing workflow writes access tokens and usage data to local files.

Mitigation: Use a test WeChat account first and restrict local token, status, and configuration files to the account owner.

Risk: Drafts include hardcoded author and footer branding from the third-party publisher.

Mitigation: Replace or remove the hardcoded author and footer branding before using the skill with a production WeChat account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/403914291/skills/wechat-publisher-403914291)
- [Publisher profile](https://clawhub.ai/user/403914291)
- [Skill overview](artifact/skill.md)
- [Installation guide](artifact/docs/install-guide.md)
- [User guide](artifact/docs/user-guide.md)
- [Template guide](artifact/docs/templates.md)
- [Block layout specification](artifact/docs/block-layout.md)
- [Troubleshooting guide](artifact/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, Python code, and HTML templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat draft content and status artifacts through the included publishing workflow.]

## Skill Version(s):

2.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
